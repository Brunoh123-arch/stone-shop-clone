# -*- coding: utf-8 -*-
"""
Acessa o Mercado Livre pelo Profile 42, abre o anuncio oficial da Rebecca Bonbon
e extrai todas as fotos oficiais de catalogo em Full HD do carrossel.
"""
import asyncio
from playwright.async_api import async_playwright
import json
import os
import urllib.request

async def get_rb_catalog():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    os.makedirs('img/produto-28-catalog', exist_ok=True)
    
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )
        page = await ctx.new_page()
        
        search_url = "https://lista.mercadolivre.com.br/mochila-rebecca-bonbon-kit-escolar"
        print("Buscando no ML:", search_url)
        await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3500)
        
        # Pega o link do primeiro produto
        prod_link = await page.evaluate('''() => {
            const el = document.querySelector('a.poly-component__title') || document.querySelector('a.ui-search-link') || document.querySelector('.ui-search-result__content-wrapper a');
            return el ? el.href : null;
        }''')
        print("Link do produto encontrado:", prod_link)
        
        if not prod_link:
            # Fallback direto para uma URL de produto
            prod_link = "https://www.mercadolivre.com.br/mochila-escolar-rebecca-bonbon-preto-com-ziper-compartimento-notebook/p/MLB63115237"
            
        await page.goto(prod_link, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)
        
        # Extrai todas as imagens da galeria oficial do produto
        gallery_imgs = await page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll('.ui-pdp-gallery img, .ui-pdp-gallery figure img, span.ui-pdp-gallery__wrapper img'));
            const urls = [];
            for (const img of imgs) {
                const src = img.getAttribute('data-zoom') || img.getAttribute('data-src') || img.src;
                if (src && src.includes('http') && !urls.includes(src)) {
                    urls.push(src);
                }
            }
            return urls;
        }''')
        print(f"Fotos oficiais na galeria do produto: {len(gallery_imgs)}")
        
        # Converte para alta resolucao (-O.webp ou -O.jpg)
        high_res_urls = []
        for u in gallery_imgs:
            # Transforma qualquer miniatura em imagem full oficial
            import re
            full_u = re.sub(r'-[A-Z]\.(webp|jpg|jpeg)', r'-O.webp', u)
            if full_u not in high_res_urls:
                high_res_urls.append(full_u)
                
        print(f"Total fotos Full HD: {len(high_res_urls)}")
        for idx, u in enumerate(high_res_urls[:8], 1):
            print(f"  [{idx}] {u}")
            dest = f"img/produto-28-catalog/slide-{idx}.webp"
            try:
                res = await ctx.request.get(u)
                if res.status == 200:
                    body = await res.body()
                    with open(dest, 'wb') as f:
                        f.write(body)
                    print(f"      [+] Baixado: {dest} ({len(body)} bytes)")
            except Exception as e:
                print(f"      [-] Erro ao baixar {u}: {e}")
                
        with open('scripts/data/p28_catalog_urls.json', 'w', encoding='utf-8') as jf:
            json.dump(high_res_urls[:8], jf, indent=2)
            
        await ctx.close()

if __name__ == '__main__':
    asyncio.run(get_rb_catalog())
