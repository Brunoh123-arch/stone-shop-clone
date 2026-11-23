# -*- coding: utf-8 -*-
"""
Acessa o TikTok / TikTok Shop no Profile 42 e intercepta fotos oficiais de catalogo
da Mochila Rebecca Bonbon.
"""
import asyncio
from playwright.async_api import async_playwright
import json
import os

async def get_tiktok_rb_catalog():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    os.makedirs('scripts/data', exist_ok=True)
    os.makedirs('img/produto-28-catalog', exist_ok=True)
    
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )
        page = await ctx.new_page()
        
        captured_images = []
        async def handle_response(response):
            url = response.url
            if any(k in url for k in ['product', 'pdp', 'search', 'detail', 'item_list']):
                try:
                    ct = response.headers.get('content-type', '')
                    if 'application/json' in ct:
                        data = await response.json()
                        # Extrai imagens de produtos da resposta da API do TikTok Shop
                        text_data = json.dumps(data)
                        import re
                        # Pega URLs de imagens do TikTok CDN (tos-alisg-i-aphluv4xwc-sg ou similar)
                        found = re.findall(r'https://[^"\'\s]+\.tiktokcdn\.com/[^"\'\s]+|https://[^"\'\s]+\.ibyteimg\.com/[^"\'\s]+', text_data)
                        for f in found:
                            if any(ext in f for ext in ['.jpg', '.jpeg', '.webp', '.png', '~tplv']):
                                if f not in captured_images:
                                    captured_images.append(f)
                except:
                    pass
                    
        page.on('response', handle_response)
        
        search_url = "https://www.tiktok.com/search?q=mochila%20rebecca%20bonbon"
        print("Acessando TikTok Search com Profile 42...")
        await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)
        
        # Clica na aba de Produtos (TikTok Shop) se existir
        shop_tab = await page.query_selector('text="Produtos"') or await page.query_selector('text="Shop"')
        if shop_tab:
            print("Clicando na aba de Produtos / Shop...")
            await shop_tab.click()
            await page.wait_for_timeout(3000)
            
        print(f"Total de imagens coletadas da API do TikTok: {len(captured_images)}")
        with open('scripts/data/p28_tiktok_images.json', 'w', encoding='utf-8') as f:
            json.dump(captured_images, f, indent=2)
            
        await ctx.close()

if __name__ == '__main__':
    asyncio.run(get_tiktok_rb_catalog())
