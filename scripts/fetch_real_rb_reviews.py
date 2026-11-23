# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright
import urllib.request
import os

async def extract_ml_photos():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        # Busca no ML com aspas
        url = "https://lista.mercadolivre.com.br/mochila-rebecca-bonbon#D[A:mochila%20rebecca%20bonbon]"
        print("Acessando:", url)
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Pega os links dos produtos
        links = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('a.poly-component__title, a.ui-search-link'))
                .map(a => a.href)
                .filter(h => h && h.includes('MLB'))
                .slice(0, 5);
        }''')
        print(f"Produtos achados: {len(links)}")
        
        found_photos = []
        for l in links:
            print("Entrando no produto:", l[:60])
            try:
                await page.goto(l, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(2500)
                
                # Procura fotos de opinioes / reviews
                imgs = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('button[class*="gallery"] img, div[class*="review"] img, .ui-review-capability-comments__gallery img'))
                        .map(i => i.src)
                        .filter(s => s && s.includes('http') && !s.includes('avatar') && !s.includes('icon'));
                }''')
                if imgs:
                    print(f"  [+] Achou {len(imgs)} fotos de avaliacao!")
                    found_photos.extend(imgs)
            except Exception as e:
                print("  [-] Erro:", e)
            if len(found_photos) >= 6:
                break
                
        print(f"Total de fotos de compradores encontradas: {len(found_photos)}")
        os.makedirs('temp_ml_reviews', exist_ok=True)
        for idx, pu in enumerate(found_photos[:6], 1):
            # Formata pra alta resolucao se for ML (troca -I.jpg por -O.jpg)
            hi_res = pu.replace('-I.jpg', '-O.jpg').replace('-V.jpg', '-O.jpg')
            dest = f"temp_ml_reviews/rb_review_{idx}.jpg"
            urllib.request.urlretrieve(hi_res, dest)
            print(f"[+] Baixado: {dest} ({os.path.getsize(dest)} bytes)")
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(extract_ml_photos())
