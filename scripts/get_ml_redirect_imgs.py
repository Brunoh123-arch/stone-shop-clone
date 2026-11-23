# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright
import urllib.request
import os

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEy75GZYnkOZ-rkbJhAMRcKWHMI_tboFjPQnaQUS9Hf54voVlayvMO-aYWmqegHNu__HXe8CRA_gneRQEFyOghygfTURpKb2xrDaqfKBPYEyamq19_w4FbI9HSMQj6XcXFngZ_hzWV0XmPqcixi6cBjialrNnUGxQ2IzMAxeqnwkqRk23fZQzOuVnIRcqvCQ9XPymH5G199qT3HOFwdxaKy286_zRMhfP7K"

async def extract():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        print("Navegando...")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        print("URL final:", page.url)
        
        # Pega todas as imagens de review da pagina
        imgs = await page.evaluate('''() => {
            const allImgs = Array.from(document.querySelectorAll('img')).map(i => i.src);
            return allImgs.filter(s => s.includes('mlstatic.com') && !s.includes('avatar') && !s.includes('icon'));
        }''')
        print(f"Total de imagens mlstatic achadas: {len(imgs)}")
        for i in imgs[:10]:
            print(" ", i)
            
        # Pega especificamente opinioes
        rev_imgs = await page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button img')).map(i => i.src);
            return btns;
        }''')
        print("Imagens em botoes (galeria de reviews):", rev_imgs)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(extract())
