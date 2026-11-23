import asyncio
import os
import sys
import json
import re
from playwright.async_api import async_playwright

sys.stdout.reconfigure(line_buffering=True)

OUT_HTML = "forno_hq_full.html"
OUT_JSON = "forno_hq_data.json"

target_url = "https://www.tiktok.com/view/product/1731951345748051223?_d=f69d064b00b1f5&_svg=1&crm_type=share"

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    print("="*70, flush=True)
    print(">>> PLAYWRIGHT VISÍVEL - CAPTURANDO FORNO HQ 48L", flush=True)
    print("="*70, flush=True)

    captured_apis = []

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

        async def on_response(response):
            try:
                u = response.url
                if any(k in u for k in ["pdp", "product", "item", "rating", "review", "detail", "seller", "comment"]):
                    ct = response.headers.get("content-type", "")
                    if "json" in ct:
                        try:
                            body = await response.json()
                            captured_apis.append({"url": u, "data": body})
                            print(f"[API] {u[:80]}", flush=True)
                        except Exception:
                            pass
            except Exception:
                pass

        page.on("response", on_response)

        print(f"[Navegando] {target_url}", flush=True)
        try:
            # wait_until commit não trava esperando domcontentloaded pesado
            await page.goto(target_url, wait_until="commit", timeout=45000)
            print("[Commit disparado, aguardando 8s para renderizar UI...]", flush=True)
            await page.wait_for_timeout(8000)

            # Rola para baixo para ativar lazy loading de imagens, specs e reviews
            for s in range(5):
                await page.evaluate("window.scrollBy(0, 600)")
                await page.wait_for_timeout(1500)

            html = await page.content()
            with open(OUT_HTML, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"[HTML salvo com sucesso: {OUT_HTML} - {len(html)} bytes]", flush=True)

            with open(OUT_JSON, "w", encoding="utf-8") as f:
                json.dump(captured_apis, f, ensure_ascii=False, indent=2)
            print(f"[APIs salvas: {len(captured_apis)}]", flush=True)

        except Exception as e:
            print(f"[Erro no acesso]: {e}", flush=True)

        print("Aguardando 10s no navegador visível...", flush=True)
        await page.wait_for_timeout(10000)
        await browser.close()
        print("Finalizado!")

if __name__ == "__main__":
    asyncio.run(main())
