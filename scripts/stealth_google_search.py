import asyncio
import urllib.parse
from playwright.async_api import async_playwright

async def search_google(query):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled'
            ]
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            locale='pt-BR'
        )
        page = await context.new_page()
        encoded = urllib.parse.quote(query)
        url = f"https://www.google.com/search?q={encoded}&num=20"
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(3000)
        
        all_hrefs = await page.evaluate("Array.from(document.querySelectorAll('a')).map(a => a.href)")
        tt_links = []
        for h in all_hrefs:
            if 'tiktok.com' in h and not 'google.com' in h:
                tt_links.append(h)
                
        print(f"Total de links do TikTok encontrados ({query}): {len(tt_links)}")
        for l in set(tt_links):
            print("  ->", l)
            
        await browser.close()
        return list(set(tt_links))

if __name__ == "__main__":
    asyncio.run(search_google('site:tiktok.com piscina inflavel 1000 litros'))
