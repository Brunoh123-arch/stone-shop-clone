# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def verify_reviews():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 412, "height": 915})
        print("Acessando produto-28...")
        await page.goto("https://stoneshopclone.vercel.app/pages/produto-28?test=1", wait_until="domcontentloaded")
        await page.wait_for_timeout(2500)
        
        # Pega as fotos dos unboxings nas reviews
        rev_imgs = await page.evaluate('''() => {
            const rev = document.querySelector('.reviews-section');
            if (!rev) return [];
            return Array.from(rev.querySelectorAll('img'))
                .map(i => i.src)
                .filter(s => !s.includes('avatar') && !s.includes('star') && !s.includes('icon'));
        }''')
        print(f"Fotos de unboxing encontradas nas avaliacoes ao vivo: {len(rev_imgs)}")
        for i, u in enumerate(rev_imgs[:6], 1):
            print(f"  Foto {i}: {u}")
            
        # Tira screenshot da secao de avaliacoes
        rev_el = await page.query_selector('.reviews-section')
        if rev_el:
            await rev_el.scroll_into_view_if_needed()
            await page.wait_for_timeout(1000)
            await rev_el.screenshot(path=r'C:\Users\Dell\.gemini\antigravity\brain\626aa811-f9a0-4dad-af48-4ab6e56722e5\live_p28_reviews_verified.png')
            print("Screenshot de avaliacoes salvo com sucesso!")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify_reviews())
