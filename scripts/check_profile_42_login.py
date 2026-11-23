import asyncio, os
from playwright.async_api import async_playwright

async def main():
    user_data = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data"
    print("Iniciando Playwright com Profile 42 (Max Digital)...")
    
    async with async_playwright() as p:
        try:
            # Tentar conectar no Chrome com Profile 42
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data,
                channel="chrome",
                args=["--profile-directory=Profile 42"],
                headless=True
            )
            page = await context.new_page()
            await page.goto("https://myaccount.google.com/", wait_until="domcontentloaded")
            title = await page.title()
            print("Titulo pagina Google Account:", title)
            content = await page.content()
            if "kaiobrunocastro12" in content or "Max Digital" in content:
                print("CONFIRMADO: Logado com sucesso na conta Max Digital / kaiobrunocastro12@gmail.com!")
            else:
                print("Aviso: Página carregada, mas string kaiobruno não encontrada explicitamente no HTML.")
            await context.close()
        except Exception as e:
            print("Erro ao carregar contexto persistente:", e)

asyncio.run(main())
