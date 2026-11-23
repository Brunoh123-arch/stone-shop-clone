import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        failed = []
        page.on("response", lambda resp: failed.append((resp.url, resp.status)) if resp.status >= 400 else None)
        
        url = "https://stoneshopclone.vercel.app/pages/produto-14.html?test=1"
        await page.goto(url, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)
        
        print("Failed responses for produto-14:")
        for u, s in failed:
            print(f"  {s}: {u}")
            
        await browser.close()

asyncio.run(run())
