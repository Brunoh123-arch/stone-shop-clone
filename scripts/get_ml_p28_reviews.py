# -*- coding: utf-8 -*-
"""
Busca avaliacoes reais de compradores de Mochila Rebecca Bonbon no Mercado Livre
via Playwright para obter unboxings de clientes totalmente distintos.
"""
import asyncio
import json
import urllib.request
import os
from playwright.async_api import async_playwright

async def get_ml_reviews():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        # Busca no ML por mochila rebecca bonbon
        url = "https://lista.mercadolivre.com.br/mochila-rebecca-bonbon-kit"
        print("Buscando no Mercado Livre:", url)
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Pega o link do primeiro produto mais vendido
        prod_link = await page.evaluate('''() => {
            const a = document.querySelector('a.poly-component__title, a.ui-search-link');
            return a ? a.href : null;
        }''')
        print("Link do produto achado:", prod_link)
        
        if prod_link:
            await page.goto(prod_link, wait_until="domcontentloaded", timeout=30000)
            await page.wait_for_timeout(3000)
            
            # Pega as fotos de opinioes com fotos
            imgs = await page.evaluate('''() => {
                const photos = Array.from(document.querySelectorAll('.ui-review-capability-comments__gallery img, .reviews-gallery img, .ui-pdp-gallery img, button[class*="gallery"] img')).map(i => i.src);
                return photos;
            }''')
            print("Fotos encontradas:", len(imgs), imgs[:5])
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(get_ml_reviews())
