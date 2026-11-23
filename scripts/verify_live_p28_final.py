# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 412, 'height': 915})
        print("Abrindo pagina de producao...")
        await page.goto('https://stoneshopclone.vercel.app/pages/produto-28?test=1', wait_until='domcontentloaded')
        await page.wait_for_timeout(2500)
        
        cards = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('#creators-section .creator-card')).map(c => {
                const vid = c.querySelector('video');
                const name = c.querySelector('.creator-name')?.textContent;
                return {
                    name: name,
                    src: vid ? vid.src : null,
                    poster: vid ? vid.poster : null
                };
            });
        }''')
        print(f"Total de cards renderizados ao vivo: {len(cards)}")
        for i, c in enumerate(cards, 1):
            print(f"Card {i}: {c['name']} | Poster: {c['poster']} | Video: {c['src']}")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
