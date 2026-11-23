import asyncio
from playwright.async_api import async_playwright

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data"
    print("Iniciando Chrome visivel com Playwright no Profile 42...")
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=False,
            args=[
                "--profile-directory=Profile 42",
                "--no-sandbox",
                "--start-maximized"
            ],
            no_viewport=True
        )
        page = browser.pages[0] if browser.pages else await browser.new_page()
        print("Navegando para o Google...")
        await page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=30000)
        print("Google aberto com sucesso na tela!")
        
        # Manter aberto por 30 segundos ou navegar
        await page.wait_for_timeout(30000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
