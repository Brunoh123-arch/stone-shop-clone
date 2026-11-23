# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright
import urllib.request
import os

url = "https://www.mercadolivre.com.br/mochila-escolar-rebecca-bonbon-preto-com-ziper-compartimento-notebook/p/MLB63115237"

async def extract_reviews_p42():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )
        page = await ctx.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        # Rola ate as opinioes
        await page.evaluate("window.scrollBy(0, 3500)")
        await page.wait_for_timeout(2500)
        
        imgs = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('img')).map(i => i.src);
        }''')
        print(f"Total fotos: {len(imgs)}")
        
        ml_imgs = [i for i in imgs if 'mlstatic.com' in i and ('-O.' in i or '-I.' in i or '-V.' in i)]
        print(f"Fotos mlstatic: {len(ml_imgs)}")
        for idx, src in enumerate(ml_imgs[:6], 1):
            print(f"  [{idx}] {src}")
            dest = f"img/review-28-preta-{idx}.jpg"
            hi = src.replace('-I.webp', '-O.jpg').replace('-V.webp', '-O.jpg').replace('-I.jpg', '-O.jpg')
            try:
                urllib.request.urlretrieve(hi, dest)
                print(f"      [+] Salvo: {dest} ({os.path.getsize(dest)} bytes)")
            except Exception as e:
                print(f"      [-] Erro: {e}")
                
        await ctx.close()

if __name__ == '__main__':
    asyncio.run(extract_reviews_p42())
