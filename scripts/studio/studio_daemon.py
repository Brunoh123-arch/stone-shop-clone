import concurrent.futures
import hashlib
import html as html_lib
import io
import json
import os
import queue
import re
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOCAL_STATE_DIR = os.path.join(os.environ.get("LOCALAPPDATA") or ROOT, "stone-studio")
STUDIO_PROFILE_DIR = os.path.join(LOCAL_STATE_DIR, "chrome-profile")
FFMPEG_BIN = shutil.which("ffmpeg") or r"C:\Users\Dell\AppData\Local\Microsoft\WinGet\Links\ffmpeg.exe"

COMMERCIAL_HANDLE_RE = re.compile(
    r"(shop|store|loja|oficial|official|ofertas|achadinhos|outlet|magazine|brasil|brazil|tech|importad|atacad)",
    re.IGNORECASE,
)

BANNED_REVIEW_RE = re.compile(
    r"(moedas|shopee|aliexpress|shein|mercado\s*livre|qualidade do produto\s*:|parecido com o? ?an[uú]ncio\s*:)",
    re.IGNORECASE,
)

CAPTCHA_URL_RE = re.compile(r"(/gz/account-verification|/security-check|captcha|challenge)", re.IGNORECASE)
CAPTCHA_HTML_RE = re.compile(
    r"(verify you are human|confirme que voc[eê] [eé] humano|g-recaptcha|h-captcha|cf-turnstile|waf-captcha-verify)",
    re.IGNORECASE,
)

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
)
DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def resolve_and_classify_url(url: str, follow_redirects: bool = True) -> tuple[str, str]:
    raw = str(url or "").strip()
    if not raw:
        return ("", "unknown")
    if not re.match(r"^https?://", raw, re.IGNORECASE):
        raw = "https://" + raw

    canonical = raw
    is_short = bool(
        re.search(
            r"(vt\.tiktok\.com|vm\.tiktok\.com|mercadolivre\.com(?:\.br)?/sec/|meli\.la/)",
            raw,
            re.IGNORECASE,
        )
    )
    if follow_redirects and is_short:
        try:
            req = urllib.request.Request(raw, headers={"User-Agent": MOBILE_UA})
            with urllib.request.urlopen(req, timeout=8) as resp:
                canonical = resp.geturl() or raw
        except urllib.error.HTTPError as he:
            canonical = he.geturl() or raw
        except Exception:
            canonical = raw

    low = canonical.lower()
    if "mercadolivre.com" in low or "mercadolibre.com" in low or "meli.la" in low:
        return (canonical, "mercadolivre")
    # Check /video/ BEFORE product so video URLs with ?product=... are never opened in Playwright!
    if "tiktok.com/" in low and ("/video/" in low or "/photo/" in low):
        return (canonical, "tiktok_video")
    if "shop.tiktok.com" in low or "/pdp/" in low or ("product" in low and "tiktok.com" in low):
        return (canonical, "tiktok_shop")
    if "vm.tiktok.com" in low or "vt.tiktok.com" in low:
        return (canonical, "tiktok_video")
    if "tiktok.com/@" in low:
        return (canonical, "tiktok_video")
    if "tiktok.com" in low:
        return (canonical, "tiktok_shop")
    return (canonical, "unknown")


def detect_captcha_or_verification(url: str, html_text: str) -> bool:
    u = str(url or "")
    if CAPTCHA_URL_RE.search(u):
        return True
    sample = str(html_text or "")[:25000]
    if len(sample) < 4000 and CAPTCHA_HTML_RE.search(sample):
        return True
    if CAPTCHA_HTML_RE.search(sample) and "<h1" not in sample.lower():
        return True
    return False


def clean_review_text(text: str) -> str | None:
    if not text:
        return None
    s = html_lib.unescape(str(text))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"R\$\s*[\d.,]+", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) < 8:
        return None
    if BANNED_REVIEW_RE.search(s):
        return None
    return s


def is_person_creator_handle(username: str, nickname: str) -> bool:
    u = str(username or "").strip().lstrip("@")
    n = str(nickname or "").strip()
    if len(u) < 3:
        return False
    if COMMERCIAL_HANDLE_RE.search(f"{u} {n}"):
        return False
    return True


def mask_buyer_name(raw_name: str, idx: int = 0) -> str:
    fallbacks = [
        "M**a S**a", "A**a C**a", "J**a O**a", "F**a L**a", "B**a R**s",
        "C**a M**s", "P**a G**s", "L**a F**a", "R**a A**s", "V**a D**s",
        "T**a P**a", "D**a B**s", "G**a N**s", "N**a V**a", "E**a M**o",
    ]
    parts = [p for p in re.split(r"\s+", str(raw_name or "").strip()) if len(p) >= 2]
    if not parts:
        return fallbacks[idx % len(fallbacks)]
    if "*" in raw_name:
        return raw_name.strip()[:18]
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else "Silva"
    return f"{first[0]}**{first[-1]} {last[0]}**{last[-1]}"


def pad_image_1to1_webp(src_bytes: bytes, out_path: str, size: int = 1000) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with Image.open(io.BytesIO(src_bytes)) as im:
        if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
            rgba = im.convert("RGBA")
            bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
            im_rgb = Image.alpha_composite(bg, rgba).convert("RGB")
        else:
            im_rgb = im.convert("RGB")

        w, h = im_rgb.size
        ratio = (w / h) if h else 1.0
        if 0.94 <= ratio <= 1.06:
            canvas = im_rgb.resize((size, size), Image.Resampling.LANCZOS)
        else:
            im_rgb.thumbnail((size, size), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (size, size), (255, 255, 255))
            ox = (size - im_rgb.size[0]) // 2
            oy = (size - im_rgb.size[1]) // 2
            canvas.paste(im_rgb, (ox, oy))

        canvas.save(out_path, format="WEBP", quality=88, method=4)
    return out_path


def download_bytes(url: str, timeout: int = 12) -> bytes | None:
    if not url or not url.startswith("http"):
        return None
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": DESKTOP_UA,
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            return data if len(data) > 512 else None
    except Exception:
        return None


def post_node_studio(endpoint: str, payload: dict):
    port = os.environ.get("STUDIO_PORT", "3333")
    token = os.environ.get("STUDIO_TOKEN", "")
    url = f"http://127.0.0.1:{port}{endpoint}"
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "x-studio-key": token},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=6).read()
    except Exception as e:
        print(f"[StudioDaemon] post_node_studio err ({endpoint}): {e}", flush=True)


def notify_node_studio(draft_id: str, event_name: str, payload: dict | None = None):
    post_node_studio("/api/studio/internal/notify", {"draftId": draft_id, "event": event_name, "payload": payload or {}})


def patch_node_draft(draft_id: str, op: str, event_name: str | None = None, **fields):
    body = {"draftId": draft_id, "op": op, **fields}
    if event_name:
        body["event"] = event_name
    post_node_studio("/api/studio/internal/patch", body)


_CATBOX_POOL = concurrent.futures.ThreadPoolExecutor(max_workers=4)


class WarmPlaywrightWorker:
    """Single-thread warm Playwright controller: muted, minimized, zero media playback, self-healing."""

    def __init__(self):
        self.tasks = queue.Queue()
        self.is_warm = False
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def submit(self, fn, *args, timeout=50):
        res_q = queue.Queue(maxsize=1)
        self.tasks.put((fn, args, res_q))
        ok, val = res_q.get(timeout=timeout)
        if not ok:
            raise RuntimeError(val)
        return val

    def _loop(self):
        pw = None
        ctx = None
        page = None
        while True:
            fn, args, res_q = self.tasks.get()
            try:
                if page is not None:
                    try:
                        if page.is_closed():
                            page = None
                            ctx = None
                    except Exception:
                        page = None
                        ctx = None

                if ctx is None:
                    from playwright.sync_api import sync_playwright

                    os.makedirs(STUDIO_PROFILE_DIR, exist_ok=True)
                    if pw is None:
                        pw = sync_playwright().start()
                    ctx = pw.chromium.launch_persistent_context(
                        STUDIO_PROFILE_DIR,
                        headless=False,
                        args=[
                            "--mute-audio",
                            "--disable-audio-output",
                            "--autoplay-policy=user-gesture-required",
                            "--window-position=-2400,-2400",
                            "--window-size=1280,860",
                        ],
                        locale="pt-BR",
                    )
                    page = ctx.pages[0] if ctx.pages else ctx.new_page()
                    try:
                        cdp = ctx.new_cdp_session(page)
                        win = cdp.send("Browser.getWindowForTarget")
                        cdp.send(
                            "Browser.setWindowBounds",
                            {"windowId": win["windowId"], "bounds": {"windowState": "minimized"}},
                        )
                    except Exception:
                        pass

                    def _block_media(route):
                        if route.request.resource_type in ("media", "font"):
                            route.abort()
                        else:
                            route.continue_()

                    page.route("**/*", _block_media)
                    self.is_warm = True

                out = fn(page, *args)
                try:
                    page.goto("about:blank", timeout=4000)
                except Exception:
                    pass
                res_q.put((True, out))
            except Exception as e:
                if "Target page, context or browser has been closed" in str(e):
                    ctx = None
                    page = None
                try:
                    if page:
                        page.goto("about:blank", timeout=3000)
                except Exception:
                    pass
                res_q.put((False, str(e)))


_BROWSER = WarmPlaywrightWorker()


def upgrade_ml_img(url: str) -> str:
    if not url:
        return ""
    u = str(url).strip()
    return re.sub(r"-[A-Z](\.(?:webp|jpg|jpeg|png))(\?.*)?$", r"-O\1", u, flags=re.IGNORECASE)


def parse_ml_html_fast(url: str) -> dict | None:
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": DESKTOP_UA,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "pt-BR,pt;q=0.9",
            },
        )
        with urllib.request.urlopen(req, timeout=9) as resp:
            final_url = resp.geturl() or url
            raw_html = resp.read().decode("utf-8", "ignore")
    except Exception:
        return None

    if detect_captcha_or_verification(final_url, raw_html):
        return {"captcha": True, "url": final_url}

    title = ""
    m_h1 = re.search(r'<h1[^>]*class="[^"]*ui-pdp-title[^"]*"[^>]*>(.*?)</h1>', raw_html, re.S)
    if m_h1:
        title = html_lib.unescape(re.sub(r"<[^>]+>", "", m_h1.group(1))).strip()

    price_orig = 0.0
    for ld in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', raw_html, re.S):
        try:
            obj = json.loads(ld.strip())
            if isinstance(obj, dict) and obj.get("@type") == "Product":
                title = title or str(obj.get("name") or "").strip()
                offers = obj.get("offers") or {}
                if isinstance(offers, list) and offers:
                    offers = offers[0]
                price_orig = float(offers.get("price") or 0)
        except Exception:
            pass

    imgs = []
    seen_imgs = set()
    for m in re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[A-Za-z0-9_-]+-[A-Z]\.(?:webp|jpg)', raw_html):
        hd = upgrade_ml_img(m)
        key = re.sub(r"-[A-Z]\.(webp|jpg)$", "", hd)
        if key not in seen_imgs:
            seen_imgs.add(key)
            imgs.append(hd)
        if len(imgs) >= 8:
            break

    desc = ""
    m_desc = re.search(r'<p[^>]*class="[^"]*ui-pdp-description__content[^"]*"[^>]*>(.*?)</p>', raw_html, re.S)
    if m_desc:
        txt = html_lib.unescape(re.sub(r"<br\s*/?>", "\n", m_desc.group(1)))
        txt = re.sub(r"<[^>]+>", "", txt).strip()
        paras = [f"<p>{html_lib.escape(p.strip())}</p>" for p in txt.split("\n") if len(p.strip()) > 20][:6]
        desc = "\n".join(paras)

    if not title and not imgs:
        return None
    return {
        "captcha": False,
        "title": title,
        "price_original": price_orig,
        "slides": imgs[:8],
        "description_html": desc,
    }


def _scrape_dom_in_playwright(page, url: str, kind: str) -> dict:
    page.goto(url, wait_until="domcontentloaded", timeout=24000)
    page.wait_for_timeout(1500)
    cur_url = page.url

    # Hard safety guard: NEVER stay on a TikTok /video/ page in Playwright!
    if "tiktok.com" in cur_url.lower() and "/video/" in cur_url.lower():
        page.goto("about:blank", timeout=3000)
        return {"redirected_video": cur_url}

    content_head = page.content()[:20000]
    if detect_captcha_or_verification(cur_url, content_head):
        return {"captcha": True, "url": cur_url}

    for frac in (0.4, 0.7, 0.9):
        try:
            page.evaluate(f"window.scrollTo(0, document.body.scrollHeight * {frac})")
            page.wait_for_timeout(700)
        except Exception:
            pass

    if kind == "mercadolivre":
        # Open ML full opinions modal/drawer if available and scroll to overfetch 40+ reviews & 15+ unboxings
        try:
            btn = page.locator('button[data-testid="see-more"], .ui-review-capability__action button').first
            if btn.count() > 0 and btn.is_visible():
                btn.click(timeout=2500)
                page.wait_for_timeout(1400)
                for _ in range(5):
                    page.evaluate(
                        """() => {
                        const scrollers = document.querySelectorAll('[class*="andes-modal__scroll"], [class*="ui-review-capability"], [role="dialog"] div');
                        scrollers.forEach(el => { if (el.scrollHeight > el.clientHeight + 80) el.scrollTop = el.scrollHeight; });
                        window.scrollBy(0, 1200);
                        }"""
                    )
                    page.wait_for_timeout(650)
        except Exception:
            pass

        return page.evaluate(
            """() => {
            const txt = (el) => (el ? el.textContent.trim() : '');
            const title = txt(document.querySelector('h1.ui-pdp-title')) || document.title.split('-')[0].trim();
            let price = 0;
            const metaPrice = document.querySelector('meta[itemprop="price"]');
            if (metaPrice && metaPrice.content) price = parseFloat(metaPrice.content) || 0;
            if (!price) {
              const frac = txt(document.querySelector('.ui-pdp-price__second-line .andes-money-amount__fraction'));
              const cents = txt(document.querySelector('.ui-pdp-price__second-line .andes-money-amount__cents')) || '00';
              if (frac) price = parseFloat(frac.replace(/\\./g, '') + '.' + cents) || 0;
            }
            const slides = [];
            const seen = new Set();
            document.querySelectorAll('.ui-pdp-gallery__figure img, figure.ui-pdp-gallery__figure img').forEach(im => {
              let u = im.getAttribute('data-zoom') || im.getAttribute('src') || '';
              u = u.replace(/-[A-Z](\\.(?:webp|jpg|jpeg|png))(\\?.*)?$/i, '-O$1');
              if (u.startsWith('http') && !seen.has(u)) { seen.add(u); slides.push(u); }
            });
            const variations = {};
            document.querySelectorAll('.ui-pdp-variations__picker').forEach((pk, idx) => {
              const lblRaw = txt(pk.querySelector('.ui-pdp-variations__label')) || ('Opção ' + (idx + 1));
              const label = lblRaw.split(':')[0].trim() || 'Cor';
              const key = idx === 0 ? 'cor' : ('grupo_' + idx);
              const opts = [];
              pk.querySelectorAll('a, button, li').forEach(item => {
                const im = item.querySelector('img');
                const optName = (item.getAttribute('title') || (im && im.getAttribute('alt')) || txt(item)).trim();
                if (!optName || optName.length > 48) return;
                let imgUrl = im ? (im.getAttribute('src') || im.getAttribute('data-src') || '') : '';
                imgUrl = imgUrl.replace(/-[A-Z](\\.(?:webp|jpg|jpeg|png))(\\?.*)?$/i, '-O$1');
                if (!opts.some(o => (o.nome || o) === optName)) {
                  opts.push(imgUrl.startsWith('http') ? { nome: optName, imagem: imgUrl } : optName);
                }
              });
              if (opts.length) {
                variations[key] = { com_imagem: opts.some(o => typeof o === 'object' && o.imagem), label, opcoes: opts };
              }
            });
            const details = [];
            document.querySelectorAll('.andes-table__row, .ui-vpp-striped-specs__table tr').forEach(tr => {
              const th = txt(tr.querySelector('th, .andes-table__header'));
              const td = txt(tr.querySelector('td, .andes-table__column'));
              if (th && td && details.length < 10) details.push({ label: th, value: td, hidden: details.length >= 5 });
            });
            const descEl = document.querySelector('.ui-pdp-description__content');
            const desc = descEl ? descEl.innerText.split('\\n').filter(l => l.trim().length > 15).slice(0, 8).map(l => '<p>' + l.trim() + '</p>').join('\\n') : '';

            const reviews = [];
            const seenComments = new Set();
            document.querySelectorAll('article.ui-review-capability-comments__comment, [class*="ui-review-capability-comments__comment"]').forEach(card => {
              const comment = txt(card.querySelector('p.ui-review-capability-comments__comment__content, p'));
              if (!comment || seenComments.has(comment)) return;
              seenComments.add(comment);
              const date = txt(card.querySelector('.ui-review-capability-comments__comment__date'));
              const photos = [];
              card.querySelectorAll('img').forEach(im => {
                let src = im.getAttribute('data-src') || im.getAttribute('src') || '';
                if (src.includes('mlstatic.com') && !src.includes('avatar') && !src.includes('svg')) {
                  src = src.replace(/-[A-Z](\\.(?:webp|jpg|jpeg|png))(\\?.*)?$/i, '-O$1');
                  if (!photos.includes(src)) photos.push(src);
                }
              });
              reviews.push({ name: '', comment, date, stars: 5, photos });
            });
            return { captcha: false, title, price_original: price, slides: slides.slice(0, 8), variations, details, description_html: desc, reviews };
            }"""
        )

    # TikTok Shop: click "Ver mais" on reviews if present + parse SSR hydration JSON & DOM
    try:
        for _ in range(3):
            page.evaluate("window.scrollBy(0, 1100)")
            page.wait_for_timeout(650)
    except Exception:
        pass

    return page.evaluate(
        """() => {
        const txt = (el) => (el ? el.textContent.trim() : '');
        let title = txt(document.querySelector('h1')) || document.title.split('|')[0].split('-')[0].trim();
        let price = 0;
        const slides = [];
        const seenSlides = new Set();
        const variations = {};
        const details = [];
        let desc = '';
        const reviews = [];

        // 1. Parse TikTok Shop SSR Hydration JSON if present
        for (const sid of ['__MODERN_ROUTER_DATA__', 'SIGI_STATE', '__NEXT_DATA__']) {
          const sEl = document.getElementById(sid);
          if (!sEl) continue;
          try {
            const raw = sEl.textContent || '';
            const imgMatches = raw.match(/https:\\/\\/p\\d+-oec-[a-z0-9-]+\\.ibyteimg\\.com\\/[^"\\\\]+/gi) || [];
            imgMatches.forEach(u => {
              const clean = u.replace(/\\\\u002F/g, '/');
              if (!clean.includes('avatar') && !seenSlides.has(clean) && slides.length < 10) {
                seenSlides.add(clean);
                slides.push(clean);
              }
            });
          } catch (_) {}
        }

        // 2. DOM Gallery + Variations + Specs + Description + Reviews
        const bodyText = document.body ? document.body.innerText : '';
        const pm = bodyText.match(/R\\$\\s*(\\d{1,4}(?:\\.\\d{3})*,\\d{2})/);
        if (pm) price = parseFloat(pm[1].replace(/\\./g, '').replace(',', '.')) || 0;

        document.querySelectorAll('img').forEach(im => {
          const w = im.naturalWidth || im.width || 0;
          const src = im.currentSrc || im.src || '';
          if (src.startsWith('http') && (w >= 260 || src.includes('ibyteimg')) && !src.includes('avatar') && !seenSlides.has(src) && slides.length < 8) {
            seenSlides.add(src);
            slides.push(src);
          }
        });

        document.querySelectorAll('[class*="sku-prop"], [class*="SkuProp"], [data-testid*="sku"]').forEach((grp, idx) => {
          const label = txt(grp.querySelector('[class*="title"], [class*="label"]')).split(':')[0].trim() || (idx === 0 ? 'Cor' : 'Tamanho');
          const key = idx === 0 ? 'cor' : ('grupo_' + idx);
          const opts = [];
          grp.querySelectorAll('button, [role="radio"], li').forEach(b => {
            const im = b.querySelector('img');
            const n = (b.getAttribute('aria-label') || (im && im.alt) || txt(b)).trim();
            if (!n || n.length > 44) return;
            const imgU = im ? (im.currentSrc || im.src || '') : '';
            if (!opts.some(o => (o.nome || o) === n)) {
              opts.push(imgU.startsWith('http') ? { nome: n, imagem: imgU } : n);
            }
          });
          if (opts.length) {
            variations[key] = { com_imagem: opts.some(o => typeof o === 'object' && o.imagem), label, opcoes: opts };
          }
        });

        document.querySelectorAll('[class*="spec-item"], [class*="SpecItem"], table tr').forEach(row => {
          const cells = row.querySelectorAll('span, td, th, div');
          if (cells.length >= 2) {
            const k = txt(cells[0]);
            const v = txt(cells[1]);
            if (k && v && k !== v && k.length < 36 && v.length < 120 && details.length < 10) {
              details.push({ label: k, value: v, hidden: details.length >= 5 });
            }
          }
        });

        const descNode = document.querySelector('[class*="product-desc"], [class*="ProductDesc"], [data-testid*="description"]');
        if (descNode) {
          desc = descNode.innerText.split('\\n').filter(l => l.trim().length > 18).slice(0, 8).map(l => '<p>' + l.trim() + '</p>').join('\\n');
        }

        const seenRev = new Set();
        document.querySelectorAll('[class*="review-item"], [class*="ReviewItem"], [data-testid*="review"]').forEach(card => {
          const comment = txt(card.querySelector('p, [class*="text"], [class*="content"]'));
          if (!comment || comment.length < 8 || seenRev.has(comment)) return;
          seenRev.add(comment);
          const user = txt(card.querySelector('[class*="name"], [class*="author"], [class*="user"]'));
          const photos = [];
          card.querySelectorAll('img').forEach(im => {
            const s = im.currentSrc || im.src || '';
            const w = im.naturalWidth || im.width || 0;
            if (s.startsWith('http') && w >= 55 && !s.includes('avatar') && !photos.includes(s)) photos.push(s);
          });
          reviews.push({ name: user, comment, date: '25/11', stars: 5, photos });
        });

        return { captcha: false, title, price_original: price, slides: slides.slice(0, 8), variations, details, description_html: desc, reviews };
        }"""
    )


def _search_tiktok_video_urls(page, query: str) -> dict:
    q_enc = urllib.parse.quote(query.strip())
    search_url = f"https://www.tiktok.com/search/video?q={q_enc}"
    page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
    page.wait_for_timeout(2200)
    cur_url = page.url
    if detect_captcha_or_verification(cur_url, page.content()[:15000]):
        return {"captcha": True, "items": []}
    try:
        page.evaluate("window.scrollBy(0, 1400)")
        page.wait_for_timeout(1200)
    except Exception:
        pass
    items = page.evaluate(
        """() => {
        const found = [];
        const seen = new Set();
        document.querySelectorAll('a[href*="/video/"]').forEach(a => {
          const href = a.href.split('?')[0];
          const m = href.match(/tiktok\\.com\\/@([^/]+)\\/video\\/(\\d+)/i);
          if (m && !seen.has(m[2])) {
            seen.add(m[2]);
            found.push({ url: href, username: m[1], video_id: m[2] });
          }
        });
        return found.slice(0, 26);
        }"""
    )
    filtered = [it for it in (items or []) if is_person_creator_handle(it.get("username", ""), "")]
    return {"captcha": False, "items": filtered}


def fetch_tikwm_info(video_url: str) -> dict | None:
    api = "https://www.tikwm.com/api/?" + urllib.parse.urlencode({"url": video_url, "hd": "0"})
    try:
        req = urllib.request.Request(api, headers={"User-Agent": DESKTOP_UA, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            payload = json.loads(resp.read().decode("utf-8", "ignore"))
        data = (payload or {}).get("data") or {}
        play_url = data.get("play") or data.get("wmplay") or ""
        if not play_url:
            return None
        if play_url.startswith("/"):
            play_url = "https://www.tikwm.com" + play_url
        author = data.get("author") or {}
        uname = str(author.get("unique_id") or "criadora.real")
        nick = str(author.get("nickname") or uname)
        cover = data.get("origin_cover") or data.get("cover") or ""
        if cover.startswith("/"):
            cover = "https://www.tikwm.com" + cover
        avatar = author.get("avatar") or ""
        if avatar.startswith("/"):
            avatar = "https://www.tikwm.com" + avatar
        dur_s = int(data.get("duration") or 18)
        return {
            "id": f"tt_{data.get('id') or int(time.time() * 1000)}",
            "source_url": video_url,
            "username": uname,
            "name": nick,
            "avatar_remote": avatar,
            "poster_remote": cover,
            "stream_url": play_url,
            "duration": f"0:{min(59, max(8, dur_s)):02d}",
            "description": str(data.get("title") or "").strip()[:140],
            "likes": f"{max(1.1, round((int(data.get('digg_count') or 1800)) / 1000, 1))}K".replace(".", ","),
            "commentsCount": max(18, int(data.get("comment_count") or 46)),
            "saves": str(max(65, int(data.get("collect_count") or 210))),
            "shares": str(max(30, int(data.get("share_count") or 88))),
        }
    except Exception:
        return None


def upload_file_to_catbox(filepath: str) -> str | None:
    boundary = "----StoneStudioBoundary" + hashlib.md5(filepath.encode()).hexdigest()[:12]
    filename = os.path.basename(filepath)
    with open(filepath, "rb") as f:
        file_bytes = f.read()
    if len(file_bytes) < 100_000:
        return None

    parts = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"reqtype\"\r\n\r\nfileupload\r\n".encode("utf-8"),
        (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"fileToUpload\"; filename=\"{filename}\"\r\n"
            f"Content-Type: video/mp4\r\n\r\n"
        ).encode("utf-8"),
        file_bytes,
        f"\r\n--{boundary}--\r\n".encode("utf-8"),
    ]
    body = b"".join(parts)
    req = urllib.request.Request(
        "https://catbox.moe/user/api.php",
        data=body,
        headers={
            "User-Agent": DESKTOP_UA,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            out = resp.read().decode("utf-8", "ignore").strip()
            if out.startswith("https://files.catbox.moe/"):
                return out
    except Exception as e:
        print(f"[StudioDaemon] Catbox upload error: {e}", flush=True)
    return None


def process_single_video_to_catbox(draft_id: str, draft_dir: str, vid_meta: dict, idx: int):
    media_dir = os.path.join(draft_dir, "media")
    os.makedirs(media_dir, exist_ok=True)
    vid_id = re.sub(r"[^a-zA-Z0-9_-]", "", str(vid_meta.get("id") or f"v{idx}"))
    raw_mp4 = os.path.join(media_dir, f"{vid_id}_raw.mp4")
    final_mp4 = os.path.join(media_dir, f"{vid_id}.mp4")
    poster_rel = f"/.studio-drafts/{draft_id}/media/poster_{vid_id}.jpg"
    poster_abs = os.path.join(media_dir, f"poster_{vid_id}.jpg")
    avatar_rel = f"/.studio-drafts/{draft_id}/media/avatar_{vid_id}.jpg"
    avatar_abs = os.path.join(media_dir, f"avatar_{vid_id}.jpg")

    try:
        req = urllib.request.Request(vid_meta["stream_url"], headers={"User-Agent": DESKTOP_UA})
        with urllib.request.urlopen(req, timeout=45) as resp, open(raw_mp4, "wb") as out_f:
            shutil.copyfileobj(resp, out_f)

        size_mb = os.path.getsize(raw_mp4) / (1024 * 1024)
        if size_mb < 0.45:
            return

        if size_mb > 35.0 and os.path.exists(FFMPEG_BIN):
            subprocess.run(
                [
                    FFMPEG_BIN, "-y", "-i", raw_mp4, "-t", "32",
                    "-vf", "scale='min(720,iw)':-2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
                    "-c:a", "aac", "-b:a", "96k", final_mp4,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=90,
            )
        if not os.path.exists(final_mp4):
            shutil.copyfile(raw_mp4, final_mp4)

        if os.path.exists(FFMPEG_BIN):
            subprocess.run(
                [FFMPEG_BIN, "-y", "-ss", "0.5", "-i", final_mp4, "-vframes", "1", "-q:v", "3", poster_abs],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=25,
            )

        av_bytes = download_bytes(vid_meta.get("avatar_remote") or "")
        if av_bytes:
            with Image.open(io.BytesIO(av_bytes)) as im:
                im.convert("RGB").resize((200, 200), Image.Resampling.LANCZOS).save(avatar_abs, "JPEG", quality=86)

        catbox_url = upload_file_to_catbox(final_mp4)
        try:
            os.remove(raw_mp4)
            os.remove(final_mp4)
        except Exception:
            pass
        if not catbox_url:
            return

        catbox_id = catbox_url.split("/")[-1]
        patch_node_draft(
            draft_id,
            "video_catbox_done",
            event_name="video_catbox_done",
            videoId=vid_meta["id"],
            catboxUrl=catbox_url,
            catboxId=catbox_id,
            poster=poster_rel if os.path.exists(poster_abs) else "",
            avatar=avatar_rel if os.path.exists(avatar_abs) else "",
        )
    except Exception as e:
        print(f"[StudioDaemon] video worker err ({vid_id}): {e}", flush=True)


def run_videos_pipeline(draft_id: str, draft_dir: str, mode: str, query: str = "", urls: list[str] | None = None):
    candidates = []
    if mode == "urls" and urls:
        for u in urls:
            cu, _ = resolve_and_classify_url(u, follow_redirects=True)
            if cu:
                candidates.append({"url": cu})
    else:
        q = (query or "").strip()
        if q:
            try:
                search_res = _BROWSER.submit(_search_tiktok_video_urls, q, timeout=35)
                if search_res.get("captcha"):
                    notify_node_studio(
                        draft_id,
                        "warning",
                        {
                            "code": "NEEDS_USER_ACTION",
                            "message": "TikTok pediu verificação humana na busca automática. Cole os links dos vídeos manualmente na aba Vídeos.",
                        },
                    )
                candidates.extend(search_res.get("items") or [])
            except Exception as e:
                print(f"[StudioDaemon] TikTok search error: {e}", flush=True)

    if not candidates:
        notify_node_studio(draft_id, "videos_preview_ready", {"count": 0})
        return

    resolved = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as meta_pool:
        futs = [meta_pool.submit(fetch_tikwm_info, c["url"]) for c in candidates[:22]]
        seen_streams = set()
        for fut in concurrent.futures.as_completed(futs):
            info = fut.result()
            if not info:
                continue
            if mode != "urls" and not is_person_creator_handle(info["username"], info["name"]):
                continue
            if info["id"] in seen_streams:
                continue
            seen_streams.add(info["id"])
            resolved.append(info)

    if not resolved:
        notify_node_studio(draft_id, "videos_preview_ready", {"count": 0})
        return

    mapped = [
        {
            "id": inf["id"],
            "name": inf["name"],
            "username": inf["username"],
            "avatar": inf["avatar_remote"] or "../img/reviews-avatars/mulheres_validadas/mulher_01.jpg",
            "poster": inf["poster_remote"] or "/logo.png",
            "video": inf["stream_url"],
            "stream_url": inf["stream_url"],
            "catbox_id": "",
            "catbox_ready": False,
            "startTime": 0,
            "likes": inf["likes"],
            "commentsCount": inf["commentsCount"],
            "saves": inf["saves"],
            "shares": inf["shares"],
            "description": inf["description"] or "Qualidade absurda, chegou super rápido!",
        }
        for inf in resolved
    ]

    patch_node_draft(
        draft_id,
        "videos_merge",
        event_name="videos_preview_ready",
        mode=mode,
        videos=mapped,
        firstDuration=resolved[0]["duration"],
    )

    for idx, inf in enumerate(resolved[:14]):
        _CATBOX_POOL.submit(process_single_video_to_catbox, draft_id, draft_dir, inf, idx)


def run_extract_pipeline(draft_id: str, draft_dir: str, url1: str, url2: str = "", auto_videos: bool = True):
    media_dir = os.path.join(draft_dir, "media")
    os.makedirs(media_dir, exist_ok=True)

    u1, kind1 = resolve_and_classify_url(url1, follow_redirects=True)
    u2, kind2 = resolve_and_classify_url(url2, follow_redirects=True) if url2 else ("", "unknown")

    # Never open tiktok_video links in Playwright — route them directly through silent tikwm!
    direct_video_urls = []
    if kind1 == "tiktok_video":
        direct_video_urls.append(u1)
    if kind2 == "tiktok_video":
        direct_video_urls.append(u2)
    if direct_video_urls:
        run_videos_pipeline(draft_id, draft_dir, mode="urls", urls=direct_video_urls)

    # Stage 1A: Ultra-Fast HTTP SSR Pass (~1.5s)
    fast_data = parse_ml_html_fast(u1) if kind1 == "mercadolivre" else None
    if fast_data and fast_data.get("captcha"):
        fast_data = None

    if fast_data and fast_data.get("title"):
        fast_slides = [{"src": s, "alt": f"{fast_data['title']} - {i + 1}"} for i, s in enumerate(fast_data.get("slides") or [])]
        patch_node_draft(
            draft_id,
            "extract_fast",
            event_name="fast_preview",
            title=fast_data["title"],
            price_original=float(fast_data.get("price_original") or 0),
            slides=fast_slides,
            description_html=fast_data.get("description_html") or "",
        )

    # Stage 1B: Warm Playwright Pass (strictly for mercadolivre / tiktok_shop PDPs)
    merged_slides = list((fast_data or {}).get("slides") or [])
    merged_vars = {}
    merged_details = []
    merged_desc = (fast_data or {}).get("description_html") or ""
    merged_title = (fast_data or {}).get("title") or ""
    merged_price = float((fast_data or {}).get("price_original") or 0)
    raw_reviews = []

    for src_u, src_k in [(u1, kind1), (u2, kind2)]:
        if not src_u or src_k not in ("mercadolivre", "tiktok_shop"):
            continue
        try:
            dom_res = _BROWSER.submit(_scrape_dom_in_playwright, src_u, src_k, timeout=42)
            if dom_res.get("redirected_video"):
                run_videos_pipeline(draft_id, draft_dir, mode="urls", urls=[dom_res["redirected_video"]])
                continue
            if dom_res.get("captcha"):
                notify_node_studio(
                    draft_id,
                    "warning",
                    {
                        "code": "NEEDS_USER_ACTION",
                        "message": f"A fonte {src_k} solicitou verificação humana. Seguindo regra anti-CAPTCHA, parei essa fonte.",
                    },
                )
                continue
            if not merged_title and dom_res.get("title"):
                merged_title = dom_res["title"]
            if not merged_price and dom_res.get("price_original"):
                merged_price = float(dom_res["price_original"])
            for s in dom_res.get("slides") or []:
                if s not in merged_slides:
                    merged_slides.append(s)
            if not merged_vars and dom_res.get("variations"):
                merged_vars = dom_res["variations"]
            if not merged_details and dom_res.get("details"):
                merged_details = dom_res["details"]
            if not merged_desc and dom_res.get("description_html"):
                merged_desc = dom_res["description_html"]
            raw_reviews.extend(dom_res.get("reviews") or [])
        except Exception as e:
            print(f"[StudioDaemon] DOM scrape err ({src_u}): {e}", flush=True)

    local_slides = []
    for i, s_url in enumerate(merged_slides[:8]):
        raw_b = download_bytes(s_url)
        if raw_b:
            out_abs = os.path.join(media_dir, f"slide_{i + 1}.webp")
            try:
                pad_image_1to1_webp(raw_b, out_abs, size=1000)
                local_slides.append({"src": f"/.studio-drafts/{draft_id}/media/slide_{i + 1}.webp", "alt": f"{merged_title} - {i + 1}"})
                continue
            except Exception:
                pass
        local_slides.append({"src": s_url, "alt": f"{merged_title} - {i + 1}"})

    for grp_k, grp in (merged_vars or {}).items():
        new_opts = []
        for o_idx, opt in enumerate(grp.get("opcoes") or []):
            if isinstance(opt, dict) and opt.get("imagem"):
                vb = download_bytes(opt["imagem"])
                if vb:
                    v_abs = os.path.join(media_dir, f"var_{grp_k}_{o_idx + 1}.webp")
                    try:
                        pad_image_1to1_webp(vb, v_abs, size=1000)
                        opt = dict(opt, imagem=f"/.studio-drafts/{draft_id}/media/var_{grp_k}_{o_idx + 1}.webp")
                    except Exception:
                        pass
            new_opts.append(opt)
        grp["opcoes"] = new_opts

    unboxing_cards = []
    text_reviews = []
    seen_comments = set()

    for idx, rv in enumerate(raw_reviews):
        cleaned = clean_review_text(rv.get("comment") or "")
        if not cleaned or cleaned.lower() in seen_comments:
            continue
        seen_comments.add(cleaned.lower())

        buyer_photos = []
        for p_idx, p_url in enumerate((rv.get("photos") or [])[:4]):
            pb = download_bytes(p_url)
            if pb:
                p_abs = os.path.join(media_dir, f"unbox_{idx + 1}_{p_idx + 1}.jpg")
                try:
                    with Image.open(io.BytesIO(pb)) as im:
                        im.convert("RGB").save(p_abs, "JPEG", quality=88)
                    buyer_photos.append(f"/.studio-drafts/{draft_id}/media/unbox_{idx + 1}_{p_idx + 1}.jpg")
                except Exception:
                    pass

        entry = {
            "id": f"rev_{idx + 1}",
            "name": mask_buyer_name(rv.get("name") or "", idx),
            "avatar": "../img/reviews-avatars/mulheres_validadas/mulher_01.jpg",
            "stars": 5 if (idx % 9 != 7) else 4,
            "date": f"{max(1, 27 - (idx % 24)):02d}/11",
            "variation": "",
            "comment": cleaned,
            "photos": buyer_photos,
        }
        if buyer_photos:
            unboxing_cards.append(entry)
        else:
            text_reviews.append(entry)

    active_unbox = unboxing_cards[:8]
    reserve_unbox = unboxing_cards[8:]
    needed_text = max(14, 22 - len(active_unbox))
    active_text = text_reviews[:needed_text]
    reserve_text = text_reviews[needed_text:]

    patch_node_draft(
        draft_id,
        "extract_full",
        event_name="reviews_pool_ready",
        title=merged_title,
        price_original=merged_price,
        slides=local_slides,
        variations=merged_vars,
        details=merged_details,
        description_html=merged_desc,
        reviews=active_unbox + active_text,
        reserve_unboxings=reserve_unbox,
        reserve_reviews=reserve_text,
    )

    if auto_videos and merged_title:
        words = [w for w in re.sub(r"[^\w\sÀ-ÿ]", " ", merged_title).split() if len(w) > 2][:5]
        q = " ".join(words)
        if q:
            run_videos_pipeline(draft_id, draft_dir, mode="search", query=q)


class StudioDaemonHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _send_json(self, code: int, obj: dict):
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path.startswith("/health"):
            return self._send_json(200, {"ok": True, "browser_warm": _BROWSER.is_warm})
        return self._send_json(404, {"ok": False})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length).decode("utf-8") or "{}") if length else {}

        if self.path == "/extract":
            threading.Thread(
                target=run_extract_pipeline,
                args=(body["draftId"], body["draftDir"], body.get("url1") or "", body.get("url2") or "", bool(body.get("autoVideos", True))),
                daemon=True,
            ).start()
            return self._send_json(202, {"ok": True, "queued": "extract"})

        if self.path == "/videos":
            threading.Thread(
                target=run_videos_pipeline,
                args=(body["draftId"], body["draftDir"], body.get("mode") or "search", body.get("query") or "", body.get("urls") or []),
                daemon=True,
            ).start()
            return self._send_json(202, {"ok": True, "queued": "videos"})

        return self._send_json(404, {"ok": False})


def run_server(port: int = 3334):
    threading.Thread(target=lambda: _BROWSER.submit(lambda p: True, timeout=30), daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", port), StudioDaemonHandler)
    print(f"[StudioDaemon] Online em http://127.0.0.1:{port} (warm zero-audio mode)", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    p = int(os.environ.get("STUDIO_DAEMON_PORT", "3334"))
    run_server(p)
