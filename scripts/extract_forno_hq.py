import asyncio
import os
import sys
import json
import re
from playwright.async_api import async_playwright

sys.stdout.reconfigure(line_buffering=True)

OUT_FILE = "forno_hq_extracted.json"
INTERCEPT_LOG = "forno_hq_apis.json"

captured_data = {
    "product_id": "1731951345748051223",
    "title": "",
    "price": None,
    "images": [],
    "description": "",
    "specs": {},
    "reviews": [],
    "api_responses": []
}

async def handle_response(response):
    try:
        url = response.url
        ct = response.headers.get("content-type", "")
        if "application/json" in ct or "text/json" in ct:
            if any(k in url for k in ["pdp", "product", "review", "detail", "shop", "item", "rating", "comment"]):
                try:
                    data = await response.json()
                    captured_data["api_responses"].append({"url": url, "data": data})
                    with open(INTERCEPT_LOG, "w", encoding="utf-8") as f:
                        json.dump(captured_data["api_responses"], f, ensure_ascii=False, indent=2)
                    print(f"[API Interceptada] {url[:90]}...", flush=True)
                except Exception:
                    pass
    except Exception:
        pass

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    print("="*70, flush=True)
    print(">>> INICIANDO PLAYWRIGHT VISÍVEL NO PROFILE 42 (MAX DIGITAL)", flush=True)
    print(">>> NAVEGANDO PARA O FORNO ELÉTRICO HQ 48L NO TIKTOK SHOP", flush=True)
    print("="*70, flush=True)

    target_urls = [
        "https://www.tiktok.com/view/product/1731951345748051223",
        "https://shop.tiktok.com/pdp/1731951345748051223"
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
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

        page = browser.pages[0] if browser.pages else await browser.new_page()
        page.on("response", handle_response)

        for url in target_urls:
            print(f"\n[Navegando] {url}", flush=True)
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=35000)
                await page.wait_for_timeout(5000)
                
                # Rolar a página para carregar imagens e avaliações
                for scroll_step in range(6):
                    await page.evaluate("window.scrollBy(0, 800)")
                    await page.wait_for_timeout(1500)
                
                # Snapshot do HTML
                html_content = await page.content()
                with open("forno_hq_page.html", "w", encoding="utf-8") as f:
                    f.write(html_content)
                print("[HTML salvo com sucesso: forno_hq_page.html]", flush=True)
                break
            except Exception as e:
                print(f"[Falha na navegação para {url}]: {e}", flush=True)

        print("\n>>> Aguardando 15s para você inspecionar a tela visível...", flush=True)
        await page.wait_for_timeout(15000)
        await browser.close()
        print(">>> Navegador fechado com sucesso!", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
