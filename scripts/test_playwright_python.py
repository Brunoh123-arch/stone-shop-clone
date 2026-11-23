import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        print("Navegando no Mercado Livre...")
        await page.goto("https://lista.mercadolivre.com.br/bola-campo-penalty-bravo-xxv", wait_until="domcontentloaded")
        print("Página carregada:", await page.title())
        
        # Pegar os primeiros produtos
        links = await page.query_selector_all("a.poly-component__title, a.ui-search-link")
        print(f"Links encontrados: {len(links)}")
        
        for i, link in enumerate(links[:5]):
            href = await link.get_attribute("href")
            text = await link.inner_text()
            print(f"[{i+1}] {text.strip()} -> {href[:80]}...")
            
        await browser.close()

asyncio.run(main())
