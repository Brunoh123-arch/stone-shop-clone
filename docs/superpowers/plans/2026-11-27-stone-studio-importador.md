# Stone Studio (`/importador`) Zero-Delay Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the self-service **Stone Studio (`/importador`)** web importer and live mobile previewer with zero-delay progressive extraction, `0ms` pre-fetched reserve pools (`+ Mais Vídeos`, `+ Mais Fotos de Compradores`, `+ Mais Comentários`), `0ms` `postMessage` inline editing, atomic validation via `validar-modelo-unico.js`, 1-click Vercel deploy, and public HTTPS access via Cloudflare Tunnel.

**Architecture:** `server.js` mounts a token-protected `/importador` Bento Obsidian UI and `/api/studio/*` router (only when `STUDIO_MODE=1`) backed by `.studio-drafts/<draftId>/` drafts with active + reserve pools and in-memory live mobile rendering via `renderProdutoFromData()`. A persistent warm Python/Playwright daemon (`scripts/studio/studio_daemon.py` on `127.0.0.1:3334`, muted and minimized) handles fast SSR/DOM extraction from Mercado Livre and TikTok Shop plus parallel 4-worker `tikwm` + `ffmpeg` + `Catbox` media processing, exposed publicly over HTTPS by `scripts/studio/start-studio.ps1` (`cloudflared`).

**Tech Stack:** Node.js v24 (`http`, `node:test`, CommonJS), Python 3.13 (`playwright`, `Pillow`, `urllib`, `concurrent.futures`, `unittest`), `ffmpeg`, `Catbox` HTTP upload, Vanilla HTML/CSS/JS (Bento Obsidian + `Server-Sent Events` + `window.postMessage`), `cloudflared`.

**Spec:** `docs/superpowers/specs/2026-11-27-stone-studio-importador-design.md`

## Global Constraints

- **Cloudflare First — Never Send Localhost:** All user-facing studio URLs must use the public HTTPS `https://<subdomain>.trycloudflare.com/importador?key=<token>` tunnel URL; never output `localhost` or `127.0.0.1` to the user.
- **Zero Audio & Minimized Browser:** Playwright must run with `--mute-audio`, minimize immediately via CDP `Browser.setWindowBounds({windowState: "minimized"})`, abort `media` resource requests, never navigate to TikTok `/video/...` pages in the browser (use `tikwm` API in Python), and return to `about:blank` when idle.
- **Strict Anti-CAPTCHA Rule:** Never solve, click through, wait out, or bypass any CAPTCHA or human-verification screen; immediately halt that source and report `NEEDS_USER_ACTION` to the UI.
- **Zero Repo Clutter & Production Isolation:** Keep `.studio-drafts/`, `.studio-chrome-profile/`, and `.studio-bin/` gitignored and `.vercelignore`d; place all new backend/worker files inside `scripts/studio/`; never expose `/api/studio/*` write routes on Vercel serverless (`api/serve.js`).
- **Validator Hard Gate:** Every published product (`id >= 160`) must pass `node scripts/validar-modelo-unico.js` with `ZERO ERROS` (`>= 4` `1:1` slides, `>= 6` buyer unboxing photo cards, `>= 20` reviews, `reviews_header` count identical to `rating_count`, unique `catbox_id`s, zero `BAD_AVATARS`, zero MD5 avatar collisions) or automatically roll back all touched files.

## Review Focus

1. **Commas inside extracted variation option names** (e.g. `"Kit 4 Cores (Preto, Branco, Cinza)"`): `validar-modelo-unico.js` splits composite `review.variation` strings on `/\s*[·•,|]\s*/`, so commas inside an option name cause false validation errors — sanitize commas inside option names to `/` in `draft-manager.js` (pinned in Task 2 test).
2. **Desktop Cloaker blocking the live mobile preview `<iframe>`**: `js/tiktok-cloaker.js` redirects desktop viewports to `/` unless `?owner=1` or `?preview=1` is in the URL — `/api/studio/preview/:draftId` must always be loaded with `?owner=1` and inject `studioPreview` `postMessage` bindings cleanly (pinned in Task 1 & Task 5 tests).
3. **Short mobile share links pasted from TikTok / Mercado Livre apps** (`https://vt.tiktok.com/...`, `https://vm.tiktok.com/...`, `https://mercadolivre.com/sec/...`): must follow HTTP redirects / canonicalize before marketplace detection so mobile copy-paste never fails with "unsupported URL" (pinned in Task 3 test).
4. **Publishing a draft that fails `validar-modelo-unico.js` (e.g. `< 6` unboxings)**: must restore exact pre-publish snapshots of `index.html`, `js/catalogo.js`, `data/produtos/index.js`, and `data/admin-catalogo-360.json` and remove copied `img/` files so the repo stays 100% clean (pinned in Task 4 test).
5. **Unauthenticated Internet scanner hitting the public `*.trycloudflare.com` tunnel URL**: every request to `/importador`, `/.studio-drafts/*`, and `/api/studio/*` without the active `STUDIO_TOKEN` (`?key=` or `x-studio-key` header / `studio_key` cookie) must be rejected with `HTTP 401` (pinned in Task 5 test).

---

### Task 1: Repo Ignore Rules & In-Memory Live Preview Renderer (`renderProdutoFromData`)

**Files:**
- Modify: `.gitignore`
- Modify: `.vercelignore`
- Modify: `api/_lib/render-produto.js:244-311`
- Test: `scripts/studio/tests/test_render_draft.js`

**Interfaces:**
- Consumes: `templates/produto-modelo.html`
- Produces:
  - `renderProdutoFromData(data: object, options?: { studioPreview?: boolean }): { status: number, html?: string, redirect?: string }` exported from `api/_lib/render-produto.js` alongside existing `renderProdutoHtml(id)` and `getProductData(id)`.
  - When `options.studioPreview === true`, injects `<script id="studio-live-bridge">...</script>` before `</body>` listening for `window.postMessage` payloads `{ type: 'STUDIO_LIVE_PATCH', payload: { product_title?, price_int?, price_cents?, price_original?, discount_badge?, installment_text?, sold_count?, rating_score?, rating_count?, reviews_header?, description_html?, slider_imgs?, creators?, produto_atual? } }` and updating the live DOM in `0ms` without page reload.

- [ ] **Step 1: Write the failing test in `scripts/studio/tests/test_render_draft.js`**

```javascript
const test = require('node:test');
const assert = require('node:assert/strict');
const { renderProdutoHtml, renderProdutoFromData } = require('../../../api/_lib/render-produto');

test('renderProdutoFromData renders in-memory draft with studio live bridge without touching disk', () => {
  const sample = {
    id: 999,
    title: 'Produto Teste Studio - Stone Shop',
    meta_description: 'Desc teste',
    product_title: 'Kit Teste Instantâneo Zero Delay',
    slider_imgs: [{ src: '/.studio-drafts/d1/slide-1.webp', alt: 'Slide 1' }],
    discount_badge: '-75%',
    price_int: '49',
    price_cents: ',89',
    price_original: 'R$ 199,90',
    installment_text: '3x R$ 16,63',
    installment_highlight: 'sem juros',
    coupon_main: 'Economize R$ 150,01',
    rating_score: '4.9',
    rating_count: '(22)',
    sold_count: '3420 vendidos on-line',
    frete_original: 'R$ 22,90',
    reviews_header: 'Avaliações dos clientes (22)',
    reviews_avg: '4.9',
    reviews: [{ name: 'M**a S**a', avatar: '../img/reviews-avatars/mulheres_validadas/av1.jpg', stars: 5, date: '25/11', variation: 'Preto', date_line: '25/11 · Preto', comment: 'Chegou super rápido!', photos: [] }],
    details: [{ label: 'Material', value: 'ABS', hidden: false }],
    video: { src: 'https://files.catbox.moe/test01.mp4', poster: '/.studio-drafts/d1/poster.jpg', duration: '0:18', catbox_id: 'test01.mp4' },
    size_guide_html: '',
    description_html: '<p>Descrição real do produto.</p>',
    related: [],
    produto_atual: { id: 999, nome: 'Kit Teste Instantâneo Zero Delay', preco: 49.89, preco_antigo: 199.9, imagens: ['/.studio-drafts/d1/slide-1.webp'] },
    extra_scripts: [],
    creator_context: 'casa',
    creators: []
  };

  const res = renderProdutoFromData(sample, { studioPreview: true });
  assert.equal(res.status, 200);
  assert.match(res.html, /Kit Teste Instantâneo Zero Delay/);
  assert.match(res.html, /id="studio-live-bridge"/);
  assert.match(res.html, /STUDIO_LIVE_PATCH/);

  const prod155 = renderProdutoHtml('155');
  assert.equal(prod155.status, 200);
  assert.doesNotMatch(prod155.html, /id="studio-live-bridge"/);
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/studio/tests/test_render_draft.js`
Expected: FAIL with `TypeError: renderProdutoFromData is not a function`

- [ ] **Step 3: Update `.gitignore`, `.vercelignore`, and implement `renderProdutoFromData` in `api/_lib/render-produto.js`**

Add `.studio-drafts/`, `.studio-chrome-profile/`, `.studio-bin/` to `.gitignore` and `.vercelignore` (plus `docs/` to `.vercelignore`). In `api/_lib/render-produto.js`, extract template token replacement from `renderProdutoHtml(id)` into `renderProdutoFromData(data, options = {})`, have `renderProdutoHtml(id)` delegate to `renderProdutoFromData(data)`, and when `options.studioPreview === true`, append `<script id="studio-live-bridge">` before `</body>` to handle `STUDIO_LIVE_PATCH` messages updating `.product-title`, `.price-current` (`price_int` + `.price-cents`), `.price-original`, `.discount-badge-white`, `.inst-val`, `.sold-num`, `#btn-buy .btn-line2`, `#desc-content-text`, `.slider-track`, `.reviews-section`, and `window.PRODUTO_ATUAL`.

- [ ] **Step 4: Run test and validator to verify they pass**

Run: `node --test scripts/studio/tests/test_render_draft.js; node scripts/validar-modelo-unico.js`
Expected: PASS (`1/1`) and `ZERO ERROS EM 90 PRODUTOS`

- [ ] **Step 5: Commit**

```powershell
git add .gitignore .vercelignore api/_lib/render-produto.js scripts/studio/tests/test_render_draft.js
git commit -m "feat(studio): extrair renderProdutoFromData com bridge postMessage 0ms"
```

---

### Task 2: Draft Manager, Sweet-Spot PIX Calibrator & `0ms` Reserve Pool (`scripts/studio/draft-manager.js`)

**Files:**
- Create: `scripts/studio/draft-manager.js`
- Test: `scripts/studio/tests/test_draft_manager.js`

**Interfaces:**
- Consumes: `data/produtos/index.js` (to compute next free product ID `>= 160`)
- Produces (`scripts/studio/draft-manager.js` exports):
  - `getNextProductId(): number`
  - `computeSweetSpotPix(originalPrice: number): { pix: number, orig: number }`
  - `sanitizeVariationName(name: string): string` (replaces `,`, `|`, `·`, `•` inside an option name with `/` so composite variation splitting in `validar-modelo-unico.js` never breaks)
  - `createDraft(init?: Partial<StudioDraft>): StudioDraft` (persisted in `.studio-drafts/<draftId>/draft.json` with `active` arrays `slides`, `variations`, `reviews`, `creators` and `reserve` arrays `reserve_videos`, `reserve_unboxings`, `reserve_reviews`)
  - `loadDraft(draftId: string): StudioDraft | null`
  - `saveDraft(draft: StudioDraft): StudioDraft`
  - `applyDraftPatch(draftId: string, patch: object): { draft: StudioDraft, livePatch: object }`
  - `popFromReserve(draftId: string, kind: 'videos' | 'unboxings' | 'reviews', count?: number): { draft: StudioDraft, added: any[], remaining: number }`
  - `buildProductJsonFromDraft(draft: StudioDraft): object` (builds full schema-compliant `produto-<id>.json` payload ready for `renderProdutoFromData` or disk publish, guaranteeing `reviews_header === "Avaliações dos clientes (" + reviewsTotal + ")"` and `rating_count === "(" + reviewsTotal + ")"`)

- [ ] **Step 1: Write the failing tests in `scripts/studio/tests/test_draft_manager.js`**

```javascript
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const {
  computeSweetSpotPix,
  sanitizeVariationName,
  createDraft,
  applyDraftPatch,
  popFromReserve,
  buildProductJsonFromDraft,
} = require('../draft-manager');

test('computeSweetSpotPix calibrates realistic PIX and anchor prices when user pastes only URL', () => {
  const low = computeSweetSpotPix(69.9);
  assert.ok(low.pix >= 24.89 && low.pix <= 39.9 && low.orig > low.pix * 2);
  const mid = computeSweetSpotPix(149.9);
  assert.ok(mid.pix >= 44.89 && mid.pix <= 59.9 && mid.orig > mid.pix * 2);
});

test('sanitizeVariationName strips commas and separator chars that break validar-modelo-unico.js', () => {
  assert.equal(sanitizeVariationName('Kit 4 Cores (Preto, Vinho, Cinza)'), 'Kit 4 Cores (Preto/ Vinho/ Cinza)');
});

test('popFromReserve moves pre-fetched videos, unboxings, and comments in 0ms and keeps rating_count synced', () => {
  const draft = createDraft({
    targetId: 998,
    product_title: 'Porta-Joias Rosa Eterna',
    price_pix: 49.89,
    price_original_num: 249.9,
    reserve_videos: [
      { id: 'v1', video: 'https://files.catbox.moe/v1.mp4', poster: '/p1.jpg', username: 'ana_br', name: 'Ana' },
      { id: 'v2', video: 'https://files.catbox.moe/v2.mp4', poster: '/p2.jpg', username: 'bia_br', name: 'Bia' }
    ],
    reserve_unboxings: [
      { id: 'u1', name: 'C**a M**s', stars: 5, date: '26/11', variation: 'Vermelho', comment: 'Lindo demais!', photos: ['/u1.jpg'] }
    ],
    reserve_reviews: [
      { id: 'r1', name: 'J**a P**a', stars: 5, date: '25/11', variation: 'Vermelho', comment: 'Amei o colar!', photos: [] }
    ]
  });

  const vRes = popFromReserve(draft.draftId, 'videos', 1);
  assert.equal(vRes.added.length, 1);
  assert.equal(vRes.remaining, 1);
  assert.equal(vRes.draft.creators.length, 1);

  const uRes = popFromReserve(draft.draftId, 'unboxings', 1);
  assert.equal(uRes.added.length, 1);
  assert.equal(uRes.draft.reviews.filter(r => r.photos && r.photos.length).length, 1);

  const patched = applyDraftPatch(draft.draftId, { product_title: 'Porta-Joias Luxo 100 Idiomas', price_pix: 44.89 });
  assert.equal(patched.livePatch.price_int, '44');
  assert.equal(patched.livePatch.price_cents, ',89');

  const built = buildProductJsonFromDraft(patched.draft);
  assert.equal(built.reviews_header, `Avaliações dos clientes (${built.rating_count.replace(/[()]/g, '')})`);
  assert.equal(built.produto_atual.preco, 44.89);

  fs.rmSync(path.join(process.cwd(), '.studio-drafts', draft.draftId), { recursive: true, force: true });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/studio/tests/test_draft_manager.js`
Expected: FAIL with `Cannot find module '../draft-manager'`

- [ ] **Step 3: Implement `scripts/studio/draft-manager.js`**

Implement draft storage in `.studio-drafts/<draftId>/draft.json`, `getNextProductId()` scanning `data/produtos/index.js` (`Math.max(...ids, 159) + 1`), `computeSweetSpotPix(originalPrice)` following Spec §2.3 (`<=80 -> 29.89..37.89`, `81..180 -> 47.89..57.89`, `181..400 -> 69.89..119.90`, `>400 -> 167.90..297.90`), `sanitizeVariationName()`, `popFromReserve()` (gracefully returning `{ added: [], remaining: 0 }` when reserve is empty), `applyDraftPatch()`, and `buildProductJsonFromDraft()` producing every mandatory key from `GEMINI.md §4`.

- [ ] **Step 4: Run test to verify it passes**

Run: `node --test scripts/studio/tests/test_draft_manager.js`
Expected: PASS (`3/3`)

- [ ] **Step 5: Commit**

```powershell
git add scripts/studio/draft-manager.js scripts/studio/tests/test_draft_manager.js
git commit -m "feat(studio): implementar draft-manager, calibrador PIX e pool reserva 0ms"
```

---

### Task 3: Warm Zero-Audio Python Daemon (`scripts/studio/studio_daemon.py` — ML/TikTok Shop Overfetch + 4x Catbox Queue)

**Files:**
- Create: `scripts/studio/studio_daemon.py`
- Test: `scripts/studio/tests/test_daemon_parsers.py`

**Interfaces:**
- Consumes: HTTP JSON requests on `http://127.0.0.1:3334` from `studio-api.js`
- Produces:
  - Pure helper functions importable by unit tests:
    - `resolve_and_classify_url(url: str, follow_redirects: bool = True) -> tuple[str, str]` returning `(canonical_url, 'mercadolivre' | 'tiktok_shop' | 'tiktok_video' | 'unknown')`
    - `clean_review_text(text: str) -> str | None` (rejects Shopee/competitor jargon like `"moedas"`, `"shopee"`, `"mercado livre"`, `"qualidade do produto:"`, or texts `< 8` chars)
    - `is_person_creator_handle(username: str, nickname: str) -> bool` (rejects store/brand handles containing `shop`, `store`, `loja`, `achadinhos`, `atacado`, `oficial`, `importadora`)
    - `pad_image_1to1_webp(src_bytes: bytes, out_path: str, size: int = 1000) -> str` (uses `Pillow` to center-fit onto clean white `1000x1000` canvas when non-square or resize cleanly when square, saving WebP `quality=88`)
    - `detect_captcha_or_verification(url: str, html: str) -> bool` (returns `True` for `/gz/account-verification`, `captcha`, `verify you are human`, `security-check`, halting immediately per Anti-CAPTCHA rule)
  - Local HTTP endpoints on `127.0.0.1:3334`:
    - `GET /health` -> `{ "ok": true, "browser_warm": bool }`
    - `POST /extract` (`{ "draftId", "draftDir", "url1", "url2", "gender" }`) -> runs fast SSR/warm-Playwright extraction (`--mute-audio`, CDP minimized, `media` blocked, `about:blank` cleanup), writes `fast_result` first (title, original price, slides, variations, specs, initial reviews) and overfetches `50+` PT-BR reviews + `20+` buyer unboxing cards + `1000x1000` WebP conversions.
    - `POST /videos` (`{ "draftId", "draftDir", "mode": "search" | "urls", "query", "urls" }`) -> collects up to `24` person-creator videos (via silent TikTok search or pasted URLs, never opening `/video/...` in browser), resolves metadata/covers via `https://www.tikwm.com/api/` immediately for `0ms` UI + reserve pool, and runs a `ThreadPoolExecutor(max_workers=4)` background queue to download MP4s, transcode `> 35 MB` via `ffmpeg -an`, extract `0.5s` real poster via `ffmpeg`, download creator avatars, and upload to `https://catbox.moe/user/api.php`.

- [ ] **Step 1: Write the failing unit tests in `scripts/studio/tests/test_daemon_parsers.py`**

```python
import io
import os
import tempfile
import unittest
from PIL import Image

from scripts.studio.studio_daemon import (
    resolve_and_classify_url,
    clean_review_text,
    is_person_creator_handle,
    pad_image_1to1_webp,
    detect_captcha_or_verification,
)


class StudioDaemonHelpersTest(unittest.TestCase):
    def test_classify_urls_including_short_links_without_network(self):
        _, kind1 = resolve_and_classify_url("https://produto.mercadolivre.com.br/MLB-123456-teste-_JM", follow_redirects=False)
        _, kind2 = resolve_and_classify_url("https://shop.tiktok.com/br/pdp/1738506652937389299", follow_redirects=False)
        _, kind3 = resolve_and_classify_url("https://www.tiktok.com/@maria.silva/video/741234567890", follow_redirects=False)
        self.assertEqual(kind1, "mercadolivre")
        self.assertEqual(kind2, "tiktok_shop")
        self.assertEqual(kind3, "tiktok_video")

    def test_clean_review_text_filters_shopee_and_competitor_jargon(self):
        self.assertIsNone(clean_review_text("Comprei só pra ganhar moedas na shopee"))
        self.assertIsNone(clean_review_text("Qualidade do produto: boa\nParecido com anúncio: sim"))
        self.assertEqual(clean_review_text("Chegou super bem embalado e funcionando perfeitamente!"), "Chegou super bem embalado e funcionando perfeitamente!")

    def test_is_person_creator_handle_blocks_stores(self):
        self.assertFalse(is_person_creator_handle("achadinhos.da.lu", "Achadinhos Oficial"))
        self.assertFalse(is_person_creator_handle("megastorebr", "Mega Store"))
        self.assertTrue(is_person_creator_handle("camila.oliveira92", "Camila Oliveira"))

    def test_pad_image_1to1_webp_outputs_exact_1000x1000(self):
        img = Image.new("RGB", (600, 900), (220, 40, 60))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "slide.webp")
            pad_image_1to1_webp(buf.getvalue(), out, size=1000)
            with Image.open(out) as res:
                self.assertEqual(res.size, (1000, 1000))

    def test_detect_captcha_halts_immediately(self):
        self.assertTrue(detect_captcha_or_verification("https://www.mercadolivre.com.br/gz/account-verification", "<html></html>"))
        self.assertTrue(detect_captcha_or_verification("https://shop.tiktok.com/br/pdp/123", "<div>Verify you are human</div>"))
        self.assertFalse(detect_captcha_or_verification("https://www.mercadolivre.com.br/p/MLB123", "<h1>Porta Joias</h1>"))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m unittest scripts/studio/tests/test_daemon_parsers.py`
Expected: FAIL with `ModuleNotFoundError: No module named 'scripts.studio.studio_daemon'`

- [ ] **Step 3: Implement `scripts/studio/studio_daemon.py`**

Implement the pure helpers plus `ThreadingHTTPServer(('127.0.0.1', 3334), DaemonHandler)` with a lazy-warmed Playwright Chromium persistent context (`.studio-chrome-profile`, `--mute-audio`, minimized window via CDP `Browser.setWindowBounds`, `page.route` blocking `media`, returning to `about:blank` after every job), redirect resolver for `vt.tiktok.com` / `vm.tiktok.com` / `mercadolivre.com/sec/`, Mercado Livre + TikTok Shop SSR/DOM extractors (grouping buyer unboxing photos 1 card per buyer), and the 4-worker `tikwm` + `ffmpeg` + `Catbox` uploader that posts incremental progress callbacks back to the draft file.

- [ ] **Step 4: Run unit tests to verify they pass**

Run: `python -m unittest scripts/studio/tests/test_daemon_parsers.py`
Expected: PASS (`5/5`)

- [ ] **Step 5: Commit**

```powershell
git add scripts/studio/studio_daemon.py scripts/studio/tests/test_daemon_parsers.py
git commit -m "feat(studio): criar studio_daemon aquecido zero-audio com overfetch e fila Catbox"
```

---

### Task 4: Atomic Publisher, Verified BR Avatar Allocator & Validator Rollback (`scripts/studio/publisher.js`)

**Files:**
- Create: `scripts/studio/publisher.js`
- Test: `scripts/studio/tests/test_publisher_rollback.js`

**Interfaces:**
- Consumes: `buildProductJsonFromDraft(draft)` from `scripts/studio/draft-manager.js`, `scripts/validar-modelo-unico.js`
- Produces (`scripts/studio/publisher.js` exports):
  - `allocateVerifiedAvatars(productJson: object, gender: 'feminino' | 'masculino' | 'unissex'): object` (assigns non-colliding MD5 Brazilian human avatars from `img/reviews-avatars/mulheres_validadas/` and `img/reviews-avatars/mulheres_brasil/`, plus verified male avatars `tt_cdn_6.jpg`, `tt_cdn_7.jpg` and verified human files when needed, strictly excluding `BAD_AVATARS`)
  - `publishDraft(draftId: string, options?: { deploy?: boolean }): Promise<{ ok: boolean, productId: number, errors?: string[], warnings?: string[], liveUrl?: string, adsUrl?: string }>`
    - Snapshots `data/produtos/index.js`, `js/catalogo.js`, `index.html`, and `data/admin-catalogo-360.json` in memory before writing.
    - Copies approved draft media into `img/`, `img/posters-desc/`, `videosprodutos/posters/`, `img/avatars-studio/`, rewrites draft paths to production relative paths (`../img/...`), writes `data/produtos/produto-<id>.json`, and registers the product across all 4 catalog/index files.
    - Runs `node scripts/validar-modelo-unico.js`. If `exitCode !== 0`, restores all 4 snapshots, deletes `data/produtos/produto-<id>.json` and every newly copied media file, and returns `{ ok: false, productId, errors }`.
    - When `exitCode === 0` and `options.deploy === true`, runs surgical `git add`, `git commit`, `git pull --rebase --autostash origin main`, `git push origin main`, `npx vercel --prod --yes`, and `npx vercel alias set <deploymentUrl> stoneshopclone.vercel.app`.

- [ ] **Step 1: Write the failing test in `scripts/studio/tests/test_publisher_rollback.js`**

```javascript
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { createDraft } = require('../draft-manager');
const { allocateVerifiedAvatars, publishDraft } = require('../publisher');

test('allocateVerifiedAvatars assigns unique Brazilian avatars with zero BAD_AVATARS', () => {
  const dummy = {
    reviews: Array.from({ length: 10 }, (_, i) => ({ name: `M**a ${i}`, avatar: '', stars: 5, date: '25/11', variation: 'Preto', comment: 'Ótimo produto!', photos: [] })),
    creators: []
  };
  const out = allocateVerifiedAvatars(dummy, 'feminino');
  const seen = new Set(out.reviews.map(r => r.avatar));
  assert.equal(seen.size, 10);
  for (const av of seen) {
    assert.doesNotMatch(av, /tt_avatar_(5|9|11|12|13|17|19|29|31|37|39|43|57)\b/);
    assert.doesNotMatch(av, /tt_cdn_(2|3|4|5|10|13|14|15|19|21|22|23|27|30)\b/);
  }
});

test('publishDraft rolls back 100% cleanly when validar-modelo-unico.js rejects an incomplete draft', async () => {
  const beforeIndex = fs.readFileSync(path.join(process.cwd(), 'data/produtos/index.js'), 'utf8');
  const beforeHome = fs.readFileSync(path.join(process.cwd(), 'index.html'), 'utf8');

  const badDraft = createDraft({
    targetId: 997,
    product_title: 'Rascunho Incompleto Sem Unboxings Suficientes',
    price_pix: 39.89,
    price_original_num: 159.9,
    slides: [{ src: 'img/bolsa-155-slide-1.webp', alt: 'S1' }], // < 4 slides & 0 unboxings -> validator MUST reject
    reviews: [{ name: 'A**a B**a', stars: 5, date: '25/11', variation: 'Único', comment: 'Muito bom mesmo!', photos: [] }]
  });

  const res = await publishDraft(badDraft.draftId, { deploy: false });
  assert.equal(res.ok, false);
  assert.ok(Array.isArray(res.errors) && res.errors.length > 0);
  assert.equal(fs.existsSync(path.join(process.cwd(), 'data/produtos/produto-997.json')), false);
  assert.equal(fs.readFileSync(path.join(process.cwd(), 'data/produtos/index.js'), 'utf8'), beforeIndex);
  assert.equal(fs.readFileSync(path.join(process.cwd(), 'index.html'), 'utf8'), beforeHome);

  fs.rmSync(path.join(process.cwd(), '.studio-drafts', badDraft.draftId), { recursive: true, force: true });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/studio/tests/test_publisher_rollback.js`
Expected: FAIL with `Cannot find module '../publisher'`

- [ ] **Step 3: Implement `scripts/studio/publisher.js`**

Implement MD5-deduplicated avatar allocation from `img/reviews-avatars/mulheres_validadas/` + `img/reviews-avatars/mulheres_brasil/` (and verified male human avatars), atomic file snapshot/restore around catalog registration (`data/produtos/index.js`, `js/catalogo.js`, `index.html` `#recommended-grid` + `#categorias-section` count, `data/admin-catalogo-360.json`), `validar-modelo-unico.js` execution + error parser, and optional Git + Vercel deploy + `stoneshopclone.vercel.app` alias command chain.

- [ ] **Step 4: Run test and validator to verify workspace remains untouched**

Run: `node --test scripts/studio/tests/test_publisher_rollback.js; node scripts/validar-modelo-unico.js`
Expected: PASS (`2/2`) and `ZERO ERROS EM 90 PRODUTOS`

- [ ] **Step 5: Commit**

```powershell
git add scripts/studio/publisher.js scripts/studio/tests/test_publisher_rollback.js
git commit -m "feat(studio): implementar publicador atomico com alocador de avatares BR e rollback"
```

---

### Task 5: Token-Guarded Studio Router (`studio-api.js` + `server.js`) & Zero-Delay Web UI (`importador.html`)

**Files:**
- Create: `scripts/studio/studio-api.js`
- Create: `importador.html`
- Create: `css/studio-importador.css`
- Create: `js/studio-importador.js`
- Modify: `server.js:30-40`
- Test: `scripts/studio/tests/test_studio_api.js`

**Interfaces:**
- Consumes: `renderProdutoFromData` (`api/_lib/render-produto.js`), `draft-manager.js`, `publisher.js`, `http://127.0.0.1:3334` (`studio_daemon.py`)
- Produces:
  - `handleStudioRequest(req, res): boolean` exported from `scripts/studio/studio-api.js` and invoked at the top of `server.js` ONLY when `process.env.STUDIO_MODE === '1'`.
  - Enforces `process.env.STUDIO_TOKEN` via `?key=<token>`, `x-studio-key` header, or `studio_key` cookie (setting `Set-Cookie: studio_key=<token>; Path=/; HttpOnly; SameSite=Lax` when authenticated via `?key=` so nested preview iframe/assets load seamlessly, and returning `401` otherwise).
  - Routes:
    - `GET /importador` -> serves `importador.html`
    - `GET /.studio-drafts/:draftId/*` -> serves draft local media files safely (path-traversal guarded)
    - `GET /api/studio/state` -> `{ nextId, drafts, daemonOnline }`
    - `POST /api/studio/extract` -> creates draft immediately, starts daemon `/extract` + auto `/videos` overfetch in parallel, returns `{ draftId, previewUrl: '/api/studio/preview/' + draftId + '?owner=1' }`
    - `GET /api/studio/stream/:draftId` -> SSE stream emitting `fast_preview`, `reviews_pool_ready`, `videos_preview_ready`, `video_catbox_done`, and `error`
    - `POST /api/studio/draft/:draftId` -> calls `applyDraftPatch`, returns `{ draft, livePatch }`
    - `POST /api/studio/draft/:draftId/more` (`{ kind: 'videos' | 'unboxings' | 'reviews', count }`) -> calls `popFromReserve` in `0ms` (and triggers background refill if reserve `< 4`), returns `{ draft, added, remaining, livePatch }`
    - `POST /api/studio/draft/:draftId/videos` (`{ mode: 'urls' | 'search', urls?, query? }`) -> dispatches extra TikTok links or keyword search to daemon
    - `GET /api/studio/preview/:draftId` -> renders `renderProdutoFromData(buildProductJsonFromDraft(draft), { studioPreview: true })`
    - `POST /api/studio/publish/:draftId` -> calls `publishDraft(draftId, { deploy })`

- [ ] **Step 1: Write the failing API & security test in `scripts/studio/tests/test_studio_api.js`**

```javascript
const test = require('node:test');
const assert = require('node:assert/strict');
const http = require('http');
const fs = require('fs');
const path = require('path');
const { createDraft } = require('../draft-manager');
const { handleStudioRequest } = require('../studio-api');

test('studio-api enforces STUDIO_TOKEN (401 without key) and serves preview + 0ms reserve expansion with key', async () => {
  process.env.STUDIO_MODE = '1';
  process.env.STUDIO_TOKEN = 'test_secret_token_123';

  const draft = createDraft({
    targetId: 996,
    product_title: 'Maleta Maquiagem Completa',
    price_pix: 47.89,
    price_original_num: 239.9,
    reserve_reviews: [{ id: 'r1', name: 'L**a C**a', stars: 5, date: '26/11', variation: 'Rosa', comment: 'Maleta linda demais!', photos: [] }]
  });

  const srv = http.createServer((req, res) => {
    if (!handleStudioRequest(req, res)) {
      res.writeHead(404);
      res.end('not studio');
    }
  });

  await new Promise(resolve => srv.listen(0, '127.0.0.1', resolve));
  const port = srv.address().port;

  const unauth = await fetch(`http://127.0.0.1:${port}/importador`);
  assert.equal(unauth.status, 401);

  const authPage = await fetch(`http://127.0.0.1:${port}/importador?key=test_secret_token_123`);
  assert.equal(authPage.status, 200);
  const cookie = authPage.headers.get('set-cookie') || '';
  assert.match(cookie, /studio_key=test_secret_token_123/);

  const preview = await fetch(`http://127.0.0.1:${port}/api/studio/preview/${draft.draftId}?owner=1`, {
    headers: { Cookie: 'studio_key=test_secret_token_123' }
  });
  assert.equal(preview.status, 200);
  const html = await preview.text();
  assert.match(html, /Maleta Maquiagem Completa/);
  assert.match(html, /STUDIO_LIVE_PATCH/);

  const more = await fetch(`http://127.0.0.1:${port}/api/studio/draft/${draft.draftId}/more`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-studio-key': 'test_secret_token_123' },
    body: JSON.stringify({ kind: 'reviews', count: 1 })
  });
  assert.equal(more.status, 200);
  const moreJson = await more.json();
  assert.equal(moreJson.added.length, 1);

  srv.close();
  fs.rmSync(path.join(process.cwd(), '.studio-drafts', draft.draftId), { recursive: true, force: true });
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `node --test scripts/studio/tests/test_studio_api.js`
Expected: FAIL with `Cannot find module '../studio-api'`

- [ ] **Step 3: Implement `scripts/studio/studio-api.js`, wire `server.js`, and create `importador.html`, `css/studio-importador.css`, and `js/studio-importador.js`**

Wire `if (process.env.STUDIO_MODE === '1' && require('./scripts/studio/studio-api').handleStudioRequest(req, res)) return;` at the top of `server.js`. Build the responsive Bento Obsidian UI in `importador.html` + `css/studio-importador.css` + `js/studio-importador.js` with:
- Single primary URL input (`Cole o link do TikTok Shop ou Mercado Livre e dê Enter`) + expandable optional `Link 2 / Preço PIX / Gênero`
- Live `0ms` inputs (`Nome do Produto`, `Preço PIX`, `Preço Antigo`, `Vendidos`, `Categoria`, `Variações`) dispatching `postMessage({ type: 'STUDIO_LIVE_PATCH', payload })` to `#studioPhoneIframe` while debouncing `POST /api/studio/draft/:draftId`
- `0ms` Reserve Pool buttons (`🎬 + Mais Vídeos (N na reserva)`, `📸 + Mais Fotos de Compradores (N na reserva)`, `💬 + Mais Comentários (N na reserva)`) + textarea to paste extra TikTok video links
- Visual curation cards with 1-click `✕ Remover` / `★ Principal` toggles and Catbox upload badges (`☁️ Catbox ✓`)
- Sticky right-hand iPhone preview (`?owner=1`) on Desktop + bottom tab switcher on Mobile + **`🚀 Validar & Publicar na Loja`** button showing live deploy logs and final links (`stoneshopclone.vercel.app/produto-<id>?owner=1` + `/videos-ads`).

- [ ] **Step 4: Run all Node + Python tests and validator**

Run: `node --test scripts/studio/tests/*.js; python -m unittest scripts/studio/tests/test_daemon_parsers.py; node scripts/validar-modelo-unico.js`
Expected: ALL PASS and `ZERO ERROS EM 90 PRODUTOS`

- [ ] **Step 5: Commit**

```powershell
git add server.js importador.html css/studio-importador.css js/studio-importador.js scripts/studio/studio-api.js scripts/studio/tests/test_studio_api.js
git commit -m "feat(studio): criar UI instantanea /importador e API SSE protegida por token"
```

---

### Task 6: Cloudflare-First Launcher (`scripts/studio/start-studio.ps1` + `npm run studio`) & End-to-End Live Tunnel Verification

**Files:**
- Create: `scripts/studio/start-studio.ps1`
- Modify: `package.json`

**Interfaces:**
- Consumes: `server.js` (`STUDIO_MODE=1`, `STUDIO_TOKEN`), `scripts/studio/studio_daemon.py`, `cloudflared`
- Produces:
  - `npm run studio` command starting `studio_daemon.py` (`127.0.0.1:3334`), `server.js` (`3333`), and `cloudflared tunnel --url http://127.0.0.1:3333` (downloading official `cloudflared-windows-amd64.exe` from GitHub Releases into `.studio-bin/cloudflared.exe` if not already installed), printing and copying only the public HTTPS URL `https://<subdomain>.trycloudflare.com/importador?key=<token>`.

- [ ] **Step 1: Add `"studio"` script to `package.json` and create `scripts/studio/start-studio.ps1`**

Add `"studio": "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/studio/start-studio.ps1"` to `package.json`. In `scripts/studio/start-studio.ps1`:
- Generate a 24-char cryptographic hex `STUDIO_TOKEN`.
- Check `Get-Command cloudflared` or `.studio-bin\cloudflared.exe`; if missing, download `https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe` into `.studio-bin\cloudflared.exe`.
- Kill stale previous `studio_daemon.py` / port `3333` processes cleanly if running, start `python scripts/studio/studio_daemon.py`, wait for `http://127.0.0.1:3334/health`, start `node server.js` with `STUDIO_MODE=1` and `STUDIO_TOKEN`, start `cloudflared tunnel --no-autoupdate --url http://127.0.0.1:3333`, parse the `https://*.trycloudflare.com` URL from `cloudflared` stderr log, copy `https://<subdomain>.trycloudflare.com/importador?key=<token>` to clipboard (`Set-Clipboard`), and print the ready banner (never printing `localhost` as user link). Support `-Detach` flag so background verification or daemon startup returns cleanly once the HTTPS URL is live.

- [ ] **Step 2: Run full test suite + start live Cloudflare Tunnel and verify `401` vs `200` over public HTTPS**

Run:
```powershell
node --test scripts/studio/tests/*.js
python -m unittest scripts/studio/tests/test_daemon_parsers.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/studio/start-studio.ps1 -Detach
```
Expected:
- All unit/integration tests PASS.
- `start-studio.ps1 -Detach` outputs a live `https://<subdomain>.trycloudflare.com/importador?key=<token>` URL.
- `curl.exe -s -o NUL -w "%{http_code}" https://<subdomain>.trycloudflare.com/importador` returns `401`.
- `curl.exe -s -o NUL -w "%{http_code}" "https://<subdomain>.trycloudflare.com/importador?key=<token>"` returns `200`.
- `node scripts/validar-modelo-unico.js` passes with `ZERO ERROS EM 90 PRODUTOS`.

- [ ] **Step 3: Commit**

```powershell
git add package.json scripts/studio/start-studio.ps1
git commit -m "feat(studio): adicionar launcher Cloudflare Tunnel (npm run studio) e fechar verificacao E2E"
```
