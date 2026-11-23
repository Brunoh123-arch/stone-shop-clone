# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright
import urllib.request
import os

url = "https://www.mercadolivre.com.br/mochila-escolar-rebecca-bonbon-preto-com-ziper-compartimento-notebook/p/MLB63115237"

async def extract_reviews():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Rola ate as opinioes
        await page.evaluate("window.scrollBy(0, 3000)")
        await page.wait_for_timeout(2000)
        
        # Pega todas as fotos com D_NQ_NP
        all_imgs = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('img'))
                .map(i => i.src)
                .filter(s => s && s.includes('http2.mlstatic.com/D_NQ_NP_'));
        }''')
        print(f"Total fotos achadas: {len(all_imgs)}")
        
        # Filtra imagens de alta resolucao
        unboxing_imgs = []
        for src in all_imgs:
            if any(k in src for k in ['-O.webp', '-O.jpg', '-F.webp', '-F.jpg', '-V.webp']):
                if src not in unboxing_imgs:
                    unboxing_imgs.append(src)
                    
        print(f"Fotos candidatas: {len(unboxing_imgs)}")
        for idx, u in enumerate(unboxing_imgs[:5], 1):
            print(f"  [{idx}] {u}")
            # Baixa
            dest = f"img/review-28-preta-{idx}.jpg"
            # Converte webp pra jpg ou baixa direto
            hi = u.replace('-V.webp', '-O.jpg').replace('-V.jpg', '-O.jpg').replace('-F.webp', '-O.jpg')
            try:
                urllib.request.urlretrieve(hi, dest)
                print(f"      [+] Baixou {dest} ({os.path.getsize(dest)} bytes)")
            except Exception as e:
                print(f"      [-] Erro {e}")
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(extract_reviews())
