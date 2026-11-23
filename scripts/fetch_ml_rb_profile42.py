# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright
import urllib.request
import os

async def extract_ml_photos_profile42():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )
        page = await ctx.new_page()
        url = "https://lista.mercadolivre.com.br/mochila-rebecca-bonbon"
        print("Acessando com Profile 42:", url)
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Pega links de produtos
        links = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('a'))
                .map(a => a.href)
                .filter(h => h && (h.includes('/p/MLB') || (h.includes('MLB-') && h.includes('rebecca'))))
                .slice(0, 5);
        }''')
        print(f"Links encontrados: {len(links)}")
        
        photos = []
        for l in links:
            print("Abrindo produto:", l[:70])
            try:
                await page.goto(l, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(3000)
                
                # Procura fotos da galeria de opinioes
                p_imgs = await page.evaluate('''() => {
                    return Array.from(document.querySelectorAll('img'))
                        .map(i => i.src)
                        .filter(s => s && s.includes('http2.mlstatic.com/D_NQ_NP_') && (s.includes('-O.jpg') || s.includes('-I.jpg') || s.includes('-F.jpg')));
                }''')
                # Filtra apenas imagens que aparecem na secao de opinioes se possivel
                op_imgs = await page.evaluate('''() => {
                    const reviewSec = document.querySelector('#reviews, .ui-pdp-reviews, .ui-review-capability-comments');
                    if (!reviewSec) return [];
                    return Array.from(reviewSec.querySelectorAll('img')).map(i => i.src);
                }''')
                print(f"  [+] Fotos da secao de opinioes: {len(op_imgs)}")
                if op_imgs:
                    photos.extend(op_imgs)
                elif p_imgs:
                    # Fotos de catálogo
                    pass
            except Exception as e:
                print("  [-] Erro:", e)
            if len(photos) >= 4:
                break
                
        print(f"Total fotos opinioes: {len(photos)}")
        os.makedirs('temp_reviews_rb', exist_ok=True)
        for idx, pu in enumerate(photos[:4], 1):
            dest = f"temp_reviews_rb/review_rb_{idx}.jpg"
            urllib.request.urlretrieve(pu, dest)
            print(f"[+] Baixado: {dest} ({os.path.getsize(dest)} bytes)")
            
        await ctx.close()

if __name__ == '__main__':
    asyncio.run(extract_ml_photos_profile42())
