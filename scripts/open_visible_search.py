import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(line_buffering=True)

async def main():
    print("Iniciando Playwright Chromium na tela...", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--start-maximized",
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = await browser.new_context(no_viewport=True, locale="pt-BR")
        page = await context.new_page()
        
        target_url = "https://www.tiktok.com/search?q=cadeira%20de%20praia%20mor"
        print(f"Abrindo busca no TikTok: {target_url}", flush=True)
        await page.goto(target_url, wait_until="commit")
        
        print("="*60, flush=True)
        print(">>> JANELA ABERTA NA SUA TELA! RESOLVA O CAPTCHA AÍ!", flush=True)
        print("="*60, flush=True)
        
        last_url = ""
        while True:
            try:
                curr = page.url
                if curr != last_url:
                    print(f"[Página Atual]: {curr}", flush=True)
                    last_url = curr
                await asyncio.sleep(2)
            except Exception:
                break

if __name__ == "__main__":
    asyncio.run(main())
