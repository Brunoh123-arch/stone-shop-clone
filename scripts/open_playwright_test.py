import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(line_buffering=True)

async def main():
    print("Iniciando Playwright Chromium visível...", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized", "--no-sandbox"]
        )
        context = await browser.new_context(no_viewport=True)
        page = await context.new_page()
        
        print("Navegando para o Google...", flush=True)
        await page.goto("https://www.google.com", timeout=30000)
        print(">>> GOOGLE ABERTO NA SUA TELA COM SUCESSO!", flush=True)
        print(">>> A janela vai ficar aberta aqui pra você ver e usar!", flush=True)
        
        # Manter aberto para o usuário ver na tela
        while True:
            await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
