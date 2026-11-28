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
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOCAL_STATE_DIR = os.path.join(os.environ.get("LOCALAPPDATA") or ROOT, "stone-studio")
STUDIO_PROFILE_DIR = os.path.join(LOCAL_STATE_DIR, "chrome-real-profile")
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
    r"(verify you are human|verify to continue|drag the puzzle piece|<title>\s*security check\s*</title>|confirme que voc[eê] [eé] humano|g-recaptcha|h-captcha|cf-turnstile|waf-captcha-verify)",
    re.IGNORECASE,
)

PT_SEARCH_STOPWORDS = {
    "a", "o", "as", "os", "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "para", "pra", "por", "com", "sem", "e", "ou", "um", "uma", "kit", "combo", "novo", "nova",
    "alta", "qualidade", "original", "oficial", "envio", "rapido", "rápido", "promocao", "promoção",
    "oferta", "luzes", "norte", "estrelado", "atmosfera", "luz", "noite", "aura", "brilhante",
}

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
)
DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def strip_accents(text: str) -> str:
    norm = unicodedata.normalize("NFKD", str(text or ""))
    return "".join(ch for ch in norm if not unicodedata.combining(ch))


def parse_tiktok_share_redirect(url: str) -> dict:
    out = {
        "product_id": "",
        "canonical_pdp_url": "",
        "title": "",
        "hero_image": "",
        "seed_video_url": "",
        "gated_login_redirect": False,
    }
    raw = str(url or "").strip()
    if not raw or "tiktok.com" not in raw.lower():
        return out

    if "/login" in raw.lower() or "redirect_url=" in raw.lower():
        out["gated_login_redirect"] = True

    target_u = raw
    try:
        parsed = urllib.parse.urlparse(raw)
        qs_outer = urllib.parse.parse_qs(parsed.query)
        if "redirect_url" in qs_outer and qs_outer["redirect_url"]:
            cand = qs_outer["redirect_url"][0]
            for _ in range(3):
                if "%25" in cand or cand.lower().startswith("https%3a") or cand.lower().startswith("http%3a"):
                    cand = urllib.parse.unquote(cand)
                else:
                    break
            target_u = cand
    except Exception:
        target_u = raw

    decoded_full = target_u
    for _ in range(3):
        dec = urllib.parse.unquote_plus(decoded_full)
        if dec == decoded_full:
            break
        decoded_full = dec

    m_pid = (
        re.search(r"/(?:view/product|pdp)/(?:[a-zA-Z-]+/)?(\d{12,25})", target_u)
        or re.search(r"/(?:view/product|pdp)/(?:[a-zA-Z-]+/)?(\d{12,25})", decoded_full)
        or re.search(r'"product_id"\s*:\s*"(\d{12,25})"', decoded_full)
    )
    if m_pid:
        pid = m_pid.group(1)
        out["product_id"] = pid
        out["canonical_pdp_url"] = f"https://shop.tiktok.com/view/product/{pid}?region=BR&locale=pt-BR"

    unique_id = ""
    group_id = ""
    try:
        t_parsed = urllib.parse.urlparse(target_u)
        t_qs = urllib.parse.parse_qs(t_parsed.query)
        if "unique_id" in t_qs and t_qs["unique_id"]:
            unique_id = urllib.parse.unquote_plus(t_qs["unique_id"][0]).strip()

        if "og_info" in t_qs and t_qs["og_info"]:
            og_raw = t_qs["og_info"][0]
            for _ in range(2):
                if og_raw.strip().startswith("%"):
                    og_raw = urllib.parse.unquote_plus(og_raw)
            og_obj = json.loads(og_raw)
            if isinstance(og_obj, dict):
                out["title"] = str(og_obj.get("title") or "").replace("+", " ").strip()
                img_u = str(og_obj.get("image") or "").strip()
                if img_u.startswith("http"):
                    out["hero_image"] = img_u

        if "trackParams" in t_qs and t_qs["trackParams"]:
            tp_raw = t_qs["trackParams"][0]
            for _ in range(2):
                if tp_raw.strip().startswith("%"):
                    tp_raw = urllib.parse.unquote_plus(tp_raw)
            tp_obj = json.loads(tp_raw)
            if isinstance(tp_obj, dict) and tp_obj.get("group_id"):
                group_id = str(tp_obj["group_id"]).strip()
    except Exception:
        pass

    if not unique_id:
        m_uid = re.search(r"[?&]unique_id=([a-zA-Z0-9._-]+)", decoded_full)
        if m_uid:
            unique_id = m_uid.group(1)
    if not group_id:
        m_gid = re.search(r'"group_id"\s*:\s*"(\d{15,25})"', decoded_full)
        if m_gid:
            group_id = m_gid.group(1)

    if group_id and re.match(r"^\d{15,25}$", group_id):
        safe_handle = re.sub(r"[^a-zA-Z0-9._-]", "", unique_id) or "tiktok"
        out["seed_video_url"] = f"https://www.tiktok.com/@{safe_handle}/video/{group_id}"

    return out


def build_clean_pt_search_query(title: str, max_words: int = 5) -> str:
    tokens = re.findall(r"[A-Za-zÀ-ÿ0-9]{2,}", str(title or ""))
    kept = []
    seen = set()
    for tok in tokens:
        low = tok.lower()
        if low in PT_SEARCH_STOPWORDS:
            continue
        if len(low) < 3 and low not in ("tv", "5g", "4k", "3d"):
            continue
        if low in seen:
            continue
        seen.add(low)
        kept.append(tok)
        if len(kept) >= max_words:
            break
    if not kept:
        kept = tokens[:max_words]
    return " ".join(kept)


def resolve_source_url_metadata(url: str, follow_redirects: bool = True) -> dict:
    raw = str(url or "").strip()
    base = {
        "canonical": "",
        "kind": "unknown",
        "product_id": "",
        "canonical_pdp_url": "",
        "title": "",
        "hero_image": "",
        "seed_video_url": "",
    }
    if not raw:
        return base
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

    tt_meta = parse_tiktok_share_redirect(canonical) if "tiktok.com" in canonical.lower() else {}
    if tt_meta.get("product_id") and tt_meta.get("canonical_pdp_url"):
        return {
            "canonical": tt_meta["canonical_pdp_url"],
            "kind": "tiktok_shop",
            **tt_meta,
        }

    low = canonical.lower()
    if "mercadolivre.com" in low or "mercadolibre.com" in low or "meli.la" in low:
        kind = "mercadolivre"
    elif "tiktok.com/" in low and ("/video/" in low or "/photo/" in low):
        kind = "tiktok_video"
    elif "shop.tiktok.com" in low or "/pdp/" in low or ("product" in low and "tiktok.com" in low):
        kind = "tiktok_shop"
    elif "vm.tiktok.com" in low or "vt.tiktok.com" in low or "tiktok.com/@" in low:
        kind = "tiktok_video"
    elif "tiktok.com" in low:
        kind = "tiktok_shop"
    else:
        kind = "unknown"

    return {
        "canonical": canonical,
        "kind": kind,
        **tt_meta,
    }


def resolve_and_classify_url(url: str, follow_redirects: bool = True) -> tuple[str, str]:
    meta = resolve_source_url_metadata(url, follow_redirects=follow_redirects)
    return (meta["canonical"], meta["kind"])


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


CHROME_EXE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROME_USER_DATA_DIR = os.path.join(os.environ.get("LOCALAPPDATA") or "", "Google", "Chrome", "User Data")
DEVTOOLS_ACTIVE_PORT_FILE = os.path.join(CHROME_USER_DATA_DIR, "DevToolsActivePort")


_PROFILE_42_OPENED_ONCE = False


def ensure_profile_42_open():
    global _PROFILE_42_OPENED_ONCE
    if _PROFILE_42_OPENED_ONCE or not os.path.exists(CHROME_EXE):
        return
    _PROFILE_42_OPENED_ONCE = True
    try:
        subprocess.Popen(
            [
                CHROME_EXE,
                "--profile-directory=Profile 42",
                "--mute-audio",
                "about:blank",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception:
        pass


class WarmPlaywrightWorker:
    """Single-thread warm Playwright controller connected to Chrome Profile 42 (with safe isolated fallback)."""

    def __init__(self):
        self.tasks = queue.Queue()
        self.is_warm = False
        self.profile42_connected = False
        self.connecting_p42 = False
        self.force_reconnect_p42 = True
        self.thread = threading.Thread(target=self._loop, daemon=True)
        self.thread.start()

    def request_profile42_reconnect(self):
        self.force_reconnect_p42 = True
        self.tasks.put((lambda _p: self.profile42_connected, (), queue.Queue(maxsize=1)))

    def submit(self, fn, *args, timeout=75):
        res_q = queue.Queue(maxsize=1)
        self.tasks.put((fn, args, res_q))
        ok, val = res_q.get(timeout=timeout)
        if not ok:
            raise RuntimeError(val)
        return val

    def _connect_cdp_profile42(self, pw, timeout_ms=90000):
        if not os.path.exists(DEVTOOLS_ACTIVE_PORT_FILE):
            return None, None
        self.connecting_p42 = True
        try:
            lines = open(DEVTOOLS_ACTIVE_PORT_FILE, "r", encoding="utf-8").read().strip().splitlines()
            if len(lines) < 2:
                return None, None
            ws_url = f"ws://127.0.0.1:{lines[0].strip()}{lines[1].strip()}"
            print(f"[StudioDaemon] Aguardando clique em Permitir no Chrome Profile 42 ({ws_url})...", flush=True)
            browser = pw.chromium.connect_over_cdp(ws_url, timeout=timeout_ms)
            ensure_profile_42_open()
            time.sleep(1.2)

            # Pick the Profile 42 context (prefer context with blank tab or TikTok/ML cookies; never touch Netflix tabs!)
            chosen_ctx = None
            chosen_blank_page = None
            for c in reversed(browser.contexts):
                urls = [pg.url for pg in c.pages]
                if any("netflix.com" in u.lower() or "youtube.com/watch" in u.lower() for u in urls):
                    continue
                for pg in c.pages:
                    if pg.url in ("about:blank", "chrome://newtab/", "chrome://new-tab-page/"):
                        chosen_ctx = c
                        chosen_blank_page = pg
                        break
                if chosen_ctx:
                    break

            if chosen_ctx is None and browser.contexts:
                # Fallback: pick last context and open a fresh background tab without touching existing tabs
                chosen_ctx = browser.contexts[-1]

            if chosen_ctx is None:
                return None, None

            page = chosen_blank_page if chosen_blank_page is not None else chosen_ctx.new_page()
            try:
                # Minimize ONLY if this window has a single blank tab (never minimize user's active browsing window)
                if len(chosen_ctx.pages) <= 2 and chosen_blank_page is not None:
                    cdp = chosen_ctx.new_cdp_session(page)
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

            try:
                page.unroute("**/*")
            except Exception:
                pass
            page.route("**/*", _block_media)
            self.profile42_connected = True
            self.is_warm = True
            print("[StudioDaemon] CONECTADO COM SUCESSO AO CHROME PROFILE 42!", flush=True)
            return chosen_ctx, page
        except Exception as e:
            print(f"[StudioDaemon] CDP Profile 42 timeout/aviso: {e}", flush=True)
            self.profile42_connected = False
            return None, None
        finally:
            self.connecting_p42 = False

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
                            self.profile42_connected = False
                    except Exception:
                        page = None
                        ctx = None
                        self.profile42_connected = False

                if pw is None:
                    from playwright.sync_api import sync_playwright
                    pw = sync_playwright().start()

                if self.force_reconnect_p42 and not self.profile42_connected:
                    self.force_reconnect_p42 = False
                    p42_ctx, p42_page = self._connect_cdp_profile42(pw, timeout_ms=75000)
                    if p42_ctx and p42_page:
                        ctx = p42_ctx
                        page = p42_page

                if ctx is None or page is None:
                    session_profile_dir = os.path.join(LOCAL_STATE_DIR, f"chrome-session-{os.getpid()}")
                    os.makedirs(session_profile_dir, exist_ok=True)
                    launch_args = [
                        "--mute-audio",
                        "--disable-audio-output",
                        "--autoplay-policy=user-gesture-required",
                        "--window-position=-2400,-2400",
                        "--window-size=1280,860",
                        "--disable-blink-features=AutomationControlled",
                    ]
                    try:
                        ctx = pw.chromium.launch_persistent_context(
                            session_profile_dir,
                            channel="chrome",
                            headless=False,
                            args=launch_args,
                            locale="pt-BR",
                            viewport={"width": 1280, "height": 860},
                        )
                    except Exception:
                        ctx = pw.chromium.launch_persistent_context(
                            session_profile_dir,
                            headless=False,
                            args=launch_args,
                            locale="pt-BR",
                            viewport={"width": 1280, "height": 860},
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

                    def _block_media_fallback(route):
                        if route.request.resource_type in ("media", "font"):
                            route.abort()
                        else:
                            route.continue_()

                    page.route("**/*", _block_media_fallback)
                    self.is_warm = True

                out = fn(page, *args)
                try:
                    page.goto("about:blank", timeout=4000)
                except Exception:
                    pass
                try:
                    res_q.put_nowait((True, out))
                except queue.Full:
                    pass
            except Exception as e:
                if "Target page, context or browser has been closed" in str(e):
                    ctx = None
                    page = None
                    self.profile42_connected = False
                try:
                    if page:
                        page.goto("about:blank", timeout=3000)
                except Exception:
                    pass
                try:
                    res_q.put_nowait((False, str(e)))
                except queue.Full:
                    pass


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


def _discover_and_scrape_ml_by_query(page, query: str) -> dict:
    ascii_q = strip_accents(query).lower()
    ascii_q = re.sub(r"\blampada\b", "luminaria", ascii_q)
    slug_q = re.sub(r"[^a-z0-9]+", "-", ascii_q).strip("-")
    if not slug_q:
        return {"captcha": False, "found": False}
    list_url = f"https://lista.mercadolivre.com.br/{urllib.parse.quote(slug_q)}"
    page.goto(list_url, wait_until="domcontentloaded", timeout=18000)
    page.wait_for_timeout(1300)
    if detect_captcha_or_verification(page.url, page.content()[:15000]):
        return {"captcha": True, "found": False}

    candidates = page.evaluate(
        """() => {
        const byUrl = new Map();
        const registerLink = (rawHref, revs) => {
          const raw = (rawHref || '').split('#')[0].split('?')[0];
          if (!raw || raw.includes('click1.') || raw.includes('/ofertas') || raw.includes('/ajuda') || raw.includes('lista.mercadolivre')) return;
          if (!(/\\/p\\/MLB\\d+/i.test(raw) || /MLB-?\\d{7,}/i.test(raw) || /\\/up\\/MLBU\\d+/i.test(raw))) return;
          const isCat = /\\/p\\/MLB\\d+/i.test(raw) ? 1 : 0;
          const prev = byUrl.get(raw);
          if (!prev || revs > prev.revs) byUrl.set(raw, { url: raw, revs, isCat });
        };

        document.querySelectorAll('li.ui-search-layout__item, div.poly-card, div.ui-search-result__wrapper').forEach(card => {
          const revMatch = (card.innerText || '').match(/\\((\\d[\\d.]*)\\)/);
          const revs = revMatch ? (parseInt(revMatch[1].replace(/\\./g, ''), 10) || 0) : 0;
          card.querySelectorAll('a[href*="mercadolivre.com.br"]:not([href*="click1."])').forEach(a => registerLink(a.href, revs));
        });

        if (byUrl.size === 0) {
          document.querySelectorAll('a[href*="mercadolivre.com.br"]:not([href*="click1."])').forEach(a => registerLink(a.href, 0));
        }

        const arr = Array.from(byUrl.values());
        arr.sort((a, b) => (b.revs - a.revs) || (b.isCat - a.isCat));
        return arr.slice(0, 4).map(x => x.url);
        }"""
    )

    agg = {
        "captcha": False,
        "found": False,
        "title": "",
        "price_original": 0.0,
        "slides": [],
        "variations": {},
        "details": [],
        "description_html": "",
        "reviews": [],
    }
    for cand_url in (candidates or [])[:3]:
        try:
            dom = _scrape_dom_in_playwright(page, cand_url, "mercadolivre")
            if dom.get("captcha"):
                break
            agg["found"] = True
            if not agg["title"] and dom.get("title"):
                agg["title"] = dom["title"]
            if not agg["price_original"] and dom.get("price_original"):
                agg["price_original"] = float(dom["price_original"])
            for s in dom.get("slides") or []:
                if s not in agg["slides"]:
                    agg["slides"].append(s)
            if not agg["variations"] and dom.get("variations"):
                agg["variations"] = dom["variations"]
            if not agg["details"] and dom.get("details"):
                agg["details"] = dom["details"]
            if not agg["description_html"] and dom.get("description_html"):
                agg["description_html"] = dom["description_html"]
            agg["reviews"].extend(dom.get("reviews") or [])

            photo_revs = sum(1 for r in agg["reviews"] if r.get("photos"))
            if len(agg["slides"]) >= 5 and photo_revs >= 7 and len(agg["reviews"]) >= 26:
                break
        except Exception:
            pass
    return agg


def _search_tiktok_video_urls(page, query: str) -> dict:
    ascii_q = strip_accents(query).lower()
    ascii_q = re.sub(r"\blampada\b", "luminaria", ascii_q)
    words = [w for w in ascii_q.split() if len(w) >= 2]
    q_full = " ".join(words[:5])
    q_core = " ".join(words[:3])
    q_tail = " ".join([words[0]] + words[2:5]) if len(words) >= 4 else f"{q_core} review"

    ddg_queries = []
    for cand_q in [
        f"tiktok.com video {q_full}",
        f"tiktok.com video {q_tail}",
        f"tiktok.com video {q_core} review",
    ]:
        if cand_q not in ddg_queries:
            ddg_queries.append(cand_q)

    collected = []
    seen_vids = set()
    seen_users = set()

    for dq in ddg_queries:
        try:
            ddg_url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(dq)
            page.goto(ddg_url, wait_until="domcontentloaded", timeout=14000)
            page.wait_for_timeout(950)
            rows = page.evaluate(
                """() => {
                const found = [];
                document.querySelectorAll('a[href]').forEach(a => {
                  let h = a.href || '';
                  if (h.includes('duckduckgo.com/y.js')) return;
                  const mUddg = h.match(/uddg=([^&]+)/);
                  if (mUddg) { try { h = decodeURIComponent(mUddg[1]); } catch(e) {} }
                  const clean = h.split('?')[0];
                  const m = clean.match(/tiktok\\.com\\/@([^/]+)\\/video\\/(\\d+)/i);
                  if (m) found.push({ url: clean, username: m[1], video_id: m[2] });
                });
                return found;
                }"""
            )
            for it in rows or []:
                vid = it.get("video_id") or ""
                uname = (it.get("username") or "").lower()
                if not vid or vid in seen_vids or uname in seen_users:
                    continue
                if not is_person_creator_handle(uname, ""):
                    continue
                seen_vids.add(vid)
                seen_users.add(uname)
                collected.append(it)
        except Exception:
            pass
        if len(collected) >= 14:
            break

    return {"captcha": False, "items": collected[:24]}


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
    if not os.path.exists(filepath) or os.path.getsize(filepath) < 100_000:
        return None

    # Primary fast path on Windows: native curl.exe (uses Schannel TLS, zero memory copy)
    curl_bin = shutil.which("curl.exe") or r"C:\Windows\System32\curl.exe"
    if os.path.exists(curl_bin):
        try:
            proc = subprocess.run(
                [
                    curl_bin,
                    "-sS",
                    "--max-time",
                    "80",
                    "-F",
                    "reqtype=fileupload",
                    "-F",
                    f"fileToUpload=@{filepath};type=video/mp4",
                    "https://catbox.moe/user/api.php",
                ],
                capture_output=True,
                text=True,
                timeout=85,
            )
            out_curl = (proc.stdout or "").strip()
            if proc.returncode == 0 and out_curl.startswith("https://files.catbox.moe/"):
                return out_curl
        except Exception as e:
            print(f"[StudioDaemon] curl Catbox fallback notice: {e}", flush=True)

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
        req = urllib.request.Request(
            vid_meta["stream_url"],
            headers={"User-Agent": DESKTOP_UA, "Referer": "https://www.tiktok.com/"},
        )
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


def run_videos_pipeline(
    draft_id: str,
    draft_dir: str,
    mode: str,
    query: str = "",
    urls: list[str] | None = None,
    seed_urls: list[str] | None = None,
):
    candidates = []
    seen_cand_urls = set()

    for su in seed_urls or []:
        if su and su not in seen_cand_urls:
            seen_cand_urls.add(su)
            candidates.append({"url": su, "is_seed": True})

    if mode == "urls" and urls:
        for u in urls:
            meta_u = resolve_source_url_metadata(u, follow_redirects=True)
            cu = meta_u.get("seed_video_url") or meta_u.get("canonical") or ""
            if cu and cu not in seen_cand_urls:
                seen_cand_urls.add(cu)
                candidates.append({"url": cu, "is_seed": True})
    else:
        q = (query or "").strip()
        if q:
            try:
                search_res = _BROWSER.submit(_search_tiktok_video_urls, q, timeout=40)
                for it in search_res.get("items") or []:
                    u_it = it.get("url") or ""
                    if u_it and u_it not in seen_cand_urls:
                        seen_cand_urls.add(u_it)
                        candidates.append(it)
                if search_res.get("captcha") and not candidates:
                    notify_node_studio(
                        draft_id,
                        "warning",
                        {
                            "code": "NEEDS_USER_ACTION",
                            "message": "A busca automática pediu verificação humana. Cole links do TikTok na aba Vídeos se quiser adicionar.",
                        },
                    )
            except Exception as e:
                print(f"[StudioDaemon] TikTok search error: {e}", flush=True)

    if not candidates:
        notify_node_studio(draft_id, "videos_preview_ready", {"count": 0})
        return

    # Preserve order (seed video first!) while resolving via tikwm in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as meta_pool:
        ordered_futs = [(c, meta_pool.submit(fetch_tikwm_info, c["url"])) for c in candidates[:22]]
        resolved = []
        seen_streams = set()
        seen_resolved_users = set()
        for c_item, fut in ordered_futs:
            try:
                info = fut.result(timeout=15)
            except Exception:
                info = None
            if not info:
                continue
            uname_low = str(info.get("username") or "").lower()
            if mode != "urls" and not c_item.get("is_seed") and not is_person_creator_handle(info["username"], info["name"]):
                continue
            if info["id"] in seen_streams or (uname_low and uname_low in seen_resolved_users):
                continue
            seen_streams.add(info["id"])
            if uname_low:
                seen_resolved_users.add(uname_low)
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
        extra={"count": len(mapped)},
    )

    for idx, inf in enumerate(resolved[:14]):
        _CATBOX_POOL.submit(process_single_video_to_catbox, draft_id, draft_dir, inf, idx)


def run_extract_pipeline(draft_id: str, draft_dir: str, url1: str, url2: str = "", auto_videos: bool = True):
    media_dir = os.path.join(draft_dir, "media")
    os.makedirs(media_dir, exist_ok=True)

    meta1 = resolve_source_url_metadata(url1, follow_redirects=True)
    meta2 = resolve_source_url_metadata(url2, follow_redirects=True) if url2 else {"canonical": "", "kind": "unknown"}

    u1, kind1 = meta1["canonical"], meta1["kind"]
    u2, kind2 = meta2.get("canonical") or "", meta2.get("kind") or "unknown"

    seed_video_urls = []
    for m_src in (meta1, meta2):
        sv = m_src.get("seed_video_url") or ""
        if sv and sv not in seed_video_urls:
            seed_video_urls.append(sv)

    # Never open tiktok_video links in Playwright — route them directly through silent tikwm!
    direct_video_urls = []
    if kind1 == "tiktok_video":
        direct_video_urls.append(u1)
    if kind2 == "tiktok_video":
        direct_video_urls.append(u2)
    if direct_video_urls:
        run_videos_pipeline(draft_id, draft_dir, mode="urls", urls=direct_video_urls)

    # Stage 1A: Instant Metadata & Hero Image Preview (< 1s for vt.tiktok.com or ML SSR!)
    fast_data = parse_ml_html_fast(u1) if kind1 == "mercadolivre" else None
    if fast_data and fast_data.get("captcha"):
        fast_data = None

    initial_title = (fast_data or {}).get("title") or meta1.get("title") or meta2.get("title") or ""
    initial_price = float((fast_data or {}).get("price_original") or 0)
    initial_remote_slides = list((fast_data or {}).get("slides") or [])
    for hero in (meta1.get("hero_image"), meta2.get("hero_image")):
        if hero and hero not in initial_remote_slides:
            initial_remote_slides.insert(0, hero)

    local_fast_slides = []
    seen_slide_md5 = set()
    for idx_s, s_u in enumerate(initial_remote_slides[:4]):
        b_fast = download_bytes(s_u, timeout=8)
        if b_fast:
            h_md5 = hashlib.md5(b_fast).hexdigest()
            if h_md5 in seen_slide_md5:
                continue
            seen_slide_md5.add(h_md5)
            out_fast = os.path.join(media_dir, f"slide_{len(local_fast_slides) + 1}.webp")
            try:
                pad_image_1to1_webp(b_fast, out_fast, size=1000)
                local_fast_slides.append(
                    {
                        "src": f"/.studio-drafts/{draft_id}/media/slide_{len(local_fast_slides) + 1}.webp",
                        "alt": f"{initial_title or 'Produto'} - {len(local_fast_slides) + 1}",
                    }
                )
                continue
            except Exception:
                pass
        local_fast_slides.append({"src": s_u, "alt": f"{initial_title or 'Produto'} - {idx_s + 1}"})

    if initial_title or local_fast_slides:
        patch_node_draft(
            draft_id,
            "extract_fast",
            event_name="fast_preview",
            title=initial_title,
            price_original=initial_price,
            slides=local_fast_slides,
            description_html=(fast_data or {}).get("description_html") or "",
        )

    # Stage 1B: Warm Playwright Pass (Official Chrome) + Auto Cross-Marketplace Enrichment
    merged_slides = list(initial_remote_slides)
    merged_vars = {}
    merged_details = []
    merged_desc = (fast_data or {}).get("description_html") or ""
    merged_title = initial_title
    merged_price = initial_price
    raw_reviews = []
    hit_primary_captcha = False

    for src_meta in (meta1, meta2):
        src_u = src_meta.get("canonical") or ""
        src_k = src_meta.get("kind") or "unknown"
        if not src_u or src_k not in ("mercadolivre", "tiktok_shop"):
            continue
        # Skip gated TikTok Shop PDP ONLY if Profile 42 is NOT connected; when Profile 42 IS connected, scrape the logged-in TikTok Shop PDP directly!
        if src_k == "tiktok_shop" and src_meta.get("gated_login_redirect") and initial_title and not _BROWSER.profile42_connected:
            hit_primary_captcha = True
            continue
        try:
            dom_res = _BROWSER.submit(_scrape_dom_in_playwright, src_u, src_k, timeout=30)
            if dom_res.get("redirected_video"):
                if dom_res["redirected_video"] not in seed_video_urls:
                    seed_video_urls.append(dom_res["redirected_video"])
                continue
            if dom_res.get("captcha"):
                hit_primary_captcha = True
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

    photo_rev_count = sum(1 for r in raw_reviews if r.get("photos"))
    search_q = build_clean_pt_search_query(merged_title, max_words=5) if merged_title else ""

    # Auto-enrich gallery 1:1, specs, PT-BR reviews, and buyer unboxing photos when TikTok Shop gates PDP or has < 4 slides / < 6 unboxings
    if search_q and (len(merged_slides) < 4 or photo_rev_count < 6 or len(raw_reviews) < 20):
        notify_node_studio(
            draft_id,
            "status_info",
            {"message": f'Enriquecendo fotos HD 1:1 e avaliações reais para "{search_q}"...'},
        )
        try:
            enrich_res = _BROWSER.submit(_discover_and_scrape_ml_by_query, search_q, timeout=55)
            if enrich_res.get("found"):
                if not merged_price and enrich_res.get("price_original"):
                    merged_price = float(enrich_res["price_original"])
                for s in enrich_res.get("slides") or []:
                    if s not in merged_slides:
                        merged_slides.append(s)
                if not merged_vars and enrich_res.get("variations"):
                    merged_vars = enrich_res["variations"]
                if not merged_details and enrich_res.get("details"):
                    merged_details = enrich_res["details"]
                if not merged_desc and enrich_res.get("description_html"):
                    merged_desc = enrich_res["description_html"]
                raw_reviews.extend(enrich_res.get("reviews") or [])
        except Exception as e:
            print(f"[StudioDaemon] Auto-enrich err ({search_q}): {e}", flush=True)

    if hit_primary_captcha and not merged_slides and not raw_reviews:
        notify_node_studio(
            draft_id,
            "warning",
            {
                "code": "NEEDS_USER_ACTION",
                "message": "O link pediu verificação humana e não trouxe título suficiente. Cole também o link do Mercado Livre em '+ Opções'.",
            },
        )

    local_slides = []
    seen_final_slide_md5 = set()
    cand_slide_urls = merged_slides[:10]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as img_pool:
        slide_bytes_list = list(img_pool.map(download_bytes, cand_slide_urls))

    for s_url, raw_b in zip(cand_slide_urls, slide_bytes_list):
        if len(local_slides) >= 8 or not raw_b:
            continue
        h_md5 = hashlib.md5(raw_b).hexdigest()
        if h_md5 in seen_final_slide_md5:
            continue
        seen_final_slide_md5.add(h_md5)
        idx_num = len(local_slides) + 1
        out_abs = os.path.join(media_dir, f"slide_{idx_num}.webp")
        try:
            pad_image_1to1_webp(raw_b, out_abs, size=1000)
            local_slides.append({"src": f"/.studio-drafts/{draft_id}/media/slide_{idx_num}.webp", "alt": f"{merged_title} - {idx_num}"})
        except Exception:
            pass

    for grp_k, grp in (merged_vars or {}).items():
        new_opts = []
        seen_var_md5 = set()
        for o_idx, opt in enumerate(grp.get("opcoes") or []):
            if isinstance(opt, dict) and opt.get("imagem"):
                vb = download_bytes(opt["imagem"])
                if vb:
                    vh = hashlib.md5(vb).hexdigest()
                    if vh not in seen_var_md5:
                        seen_var_md5.add(vh)
                        v_abs = os.path.join(media_dir, f"var_{grp_k}_{o_idx + 1}.webp")
                        try:
                            pad_image_1to1_webp(vb, v_abs, size=1000)
                            opt = dict(opt, imagem=f"/.studio-drafts/{draft_id}/media/var_{grp_k}_{o_idx + 1}.webp")
                        except Exception:
                            pass
                    else:
                        opt = opt.get("nome") or f"Opção {o_idx + 1}"
            new_opts.append(opt)
        grp["opcoes"] = new_opts

    # Pre-download buyer unboxing photos in parallel (8 threads) so 15+ photos finish in ~1.2s!
    all_photo_urls = []
    for rv in raw_reviews[:60]:
        for p_u in (rv.get("photos") or [])[:3]:
            if p_u not in all_photo_urls:
                all_photo_urls.append(p_u)

    photo_bytes_map = {}
    if all_photo_urls:
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ph_pool:
            for u_ph, b_ph in zip(all_photo_urls[:36], ph_pool.map(download_bytes, all_photo_urls[:36])):
                if b_ph:
                    photo_bytes_map[u_ph] = b_ph

    unboxing_cards = []
    text_reviews = []
    seen_comments = set()
    seen_unbox_md5 = set()

    for idx, rv in enumerate(raw_reviews[:65]):
        cleaned = clean_review_text(rv.get("comment") or "")
        if not cleaned or cleaned.lower() in seen_comments:
            continue
        seen_comments.add(cleaned.lower())

        buyer_photos = []
        for p_idx, p_url in enumerate((rv.get("photos") or [])[:3]):
            pb = photo_bytes_map.get(p_url)
            if pb:
                ph_md5 = hashlib.md5(pb).hexdigest()
                if ph_md5 in seen_unbox_md5:
                    continue
                seen_unbox_md5.add(ph_md5)
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
    needed_text = max(18, 26 - len(active_unbox))
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

    if auto_videos and (search_q or seed_video_urls):
        run_videos_pipeline(draft_id, draft_dir, mode="search", query=search_q, seed_urls=seed_video_urls)


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
            return self._send_json(
                200,
                {
                    "ok": True,
                    "browser_warm": _BROWSER.is_warm,
                    "profile42_connected": _BROWSER.profile42_connected,
                    "connecting_p42": _BROWSER.connecting_p42,
                },
            )
        return self._send_json(404, {"ok": False})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length).decode("utf-8") or "{}") if length else {}

        if self.path == "/connect-profile42":
            _BROWSER.request_profile42_reconnect()
            return self._send_json(202, {"ok": True, "connecting": True})

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
    try:
        if os.path.exists(LOCAL_STATE_DIR):
            for entry in os.listdir(LOCAL_STATE_DIR):
                if entry.startswith("chrome-session-"):
                    shutil.rmtree(os.path.join(LOCAL_STATE_DIR, entry), ignore_errors=True)
    except Exception:
        pass
    threading.Thread(target=lambda: _BROWSER.submit(lambda p: True, timeout=80), daemon=True).start()
    srv = ThreadingHTTPServer(("127.0.0.1", port), StudioDaemonHandler)
    print(f"[StudioDaemon] Online em http://127.0.0.1:{port} (warm zero-audio mode)", flush=True)
    srv.serve_forever()


if __name__ == "__main__":
    p = int(os.environ.get("STUDIO_DAEMON_PORT", "3334"))
    run_server(p)
