# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 412, 'height': 915})
        await page.goto('https://stoneshopclone.vercel.app/pages/produto-28', wait_until='networkidle')
        print('URL FINAL:', page.url)
        print('TITULO:', await page.title())
        
        has_creators_id = await page.query_selector('#creators-section')
        has_creators_class = await page.query_selector('.creators-section')
        print('Achou #creators-section?', bool(has_creators_id))
        print('Achou .creators-section?', bool(has_creators_class))
        
        if has_creators_id:
            disp = await page.evaluate("() => window.getComputedStyle(document.getElementById('creators-section')).display")
            print("Computed display de #creators-section:", disp)
            
        await page.screenshot(path=r'C:\Users\Dell\.gemini\antigravity\brain\626aa811-f9a0-4dad-af48-4ab6e56722e5\live_full_p28.png', full_page=True)
        print("Full page screenshot gravado em live_full_p28.png")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect())
