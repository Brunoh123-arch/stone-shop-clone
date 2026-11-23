import asyncio
import os
import sys
import json
import urllib.parse
from playwright.async_api import async_playwright

sys.stdout.reconfigure(line_buffering=True)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
SCREENSHOT_PATH = os.path.join(DATA_DIR, "current_live_screen.png")
OUT_JSON = os.path.join(DATA_DIR, "cadeira_praia_tiktok_extracted.json")
STOP_FILE = os.path.join(DATA_DIR, "stop_browser.flag")

if os.path.exists(STOP_FILE):
    try:
        os.remove(STOP_FILE)
    except Exception:
        pass

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    print("="*70, flush=True)
    print(">>> INICIANDO CHROME PERSISTENTE E VISÍVEL (PROFILE 42)", flush=True)
    print(">>> O NAVEGADOR VAI FICAR ABERTO NA SUA TELA SEM FECHAR!", flush=True)
    print("="*70, flush=True)

    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=False,
            args=[
                "--profile-directory=Profile 42",
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            no_viewport=True
        )

        page = await context.new_page()

        # Abrir direto a busca no Google pela Cadeira de Praia Mor no TikTok Shop
        search_url = "https://www.google.com/search?q=site:shop.tiktok.com/pdp+cadeira+de+praia+mor"
        print(f"Navegando para: {search_url}", flush=True)
        await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)

        last_url = ""
        pdp_extracted = False

        print("\n>>> Monitorando navegador (janela mantida aberta permanentemente)...", flush=True)

        while not os.path.exists(STOP_FILE):
            try:
                current_url = page.url
                if current_url != last_url:
                    print(f"[URL Atualizada]: {current_url}", flush=True)
                    last_url = current_url
                    await page.screenshot(path=SCREENSHOT_PATH)

                # Se estiver em um PDP oficial do TikTok Shop (e NÃO for página de busca do Google)
                is_real_pdp = ("shop.tiktok.com" in current_url and "/pdp/" in current_url) or \
                              ("tiktok.com" in current_url and "/product/" in current_url)

                if is_real_pdp and not pdp_extracted and "google.com" not in current_url:
                    print("\n>>> DETECTADO PRODUTO OFICIAL DO TIKTOK SHOP! EXTRAINDO DADOS...", flush=True)
                    await page.wait_for_timeout(3000)
                    
                    # Scroll suave para renderizar reviews e fotos
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
                    await page.wait_for_timeout(2000)
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await page.wait_for_timeout(2000)

                    # Extrair dados completos
                    data = await page.evaluate('''() => {
                        const h1 = document.querySelector('h1') || document.querySelector('[class*="title"]');
                        const priceEl = document.querySelector('[class*="price"]') || document.querySelector('[data-e2e="pdp-price"]');
                        const soldEl = document.querySelector('[class*="sold"]');
                        const descEl = document.querySelector('[class*="desc"]') || document.querySelector('[class*="specification"]');
                        
                        const imgs = Array.from(document.querySelectorAll('img'))
                            .map(img => img.src || img.getAttribute('data-src'))
                            .filter(Boolean)
                            .filter(src => src.includes('tiktokcdn') || src.includes('ibyteimg') || src.includes('tos-maliva'));

                        const reviews = [];
                        document.querySelectorAll('[class*="review-card"], [class*="review_item"], [class*="comment-item"], [data-e2e*="review"]').forEach(card => {
                            const author = card.querySelector('[class*="author"], [class*="name"], [class*="user"]')?.innerText?.trim() || "";
                            const comment = card.querySelector('[class*="content"], [class*="text"], [class*="comment"]')?.innerText?.trim() || "";
                            const dateSku = card.querySelector('[class*="sku"], [class*="spec"], [class*="time"], [class*="date"]')?.innerText?.trim() || "";
                            const revImgs = Array.from(card.querySelectorAll('img')).map(i => i.src).filter(s => !s.includes('avatar') && !s.includes('icon'));
                            const avatar = card.querySelector('[class*="avatar"] img')?.src || "";
                            if (comment || revImgs.length > 0) {
                                reviews.push({ author, comment, dateSku, avatar, photos: revImgs });
                            }
                        });

                        return {
                            url: window.location.href,
                            title: document.title,
                            product_name: h1 ? h1.innerText.trim() : "",
                            price: priceEl ? priceEl.innerText.trim() : "",
                            sold_count: soldEl ? soldEl.innerText.trim() : "",
                            description: descEl ? descEl.innerText.trim() : "",
                            images: imgs,
                            reviews: reviews
                        };
                    }''')

                    with open(OUT_JSON, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    
                    print(f"[EXTRAÇÃO COMPLETA] Dados salvos em {OUT_JSON}", flush=True)
                    print(f"- Produto: {data.get('product_name')}", flush=True)
                    print(f"- Fotos: {len(data.get('images', []))}", flush=True)
                    print(f"- Reviews: {len(data.get('reviews', []))}", flush=True)
                    pdp_extracted = True

                await asyncio.sleep(2)
            except Exception as e:
                print(f"[Loop info]: {e}", flush=True)
                await asyncio.sleep(2)

        print("Encerrando navegador a pedido...", flush=True)
        await context.close()

if __name__ == "__main__":
    asyncio.run(main())
