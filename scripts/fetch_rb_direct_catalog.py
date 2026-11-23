# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright
import json
import os
import re

url = "https://www.mercadolivre.com.br/mochila-escolar-rebecca-bonbon-preto-com-ziper-compartimento-notebook/p/MLB63115237"

async def get_direct_catalog():
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
        print("Acessando diretamente a pagina oficial do produto no ML...")
        await page.goto(url, wait_until="domcontentloaded", timeout=40000)
        await page.wait_for_timeout(4000)
        
        # Pega todas as fotos da galeria
        imgs = await page.evaluate('''() => {
            const list = [];
            const els = document.querySelectorAll('.ui-pdp-gallery__column img, .ui-pdp-gallery figure img, .ui-pdp-gallery img');
            for (const el of els) {
                const src = el.getAttribute('data-zoom') || el.src;
                if (src && src.includes('http') && !list.includes(src)) {
                    list.push(src);
                }
            }
            return list;
        }''')
        print(f"Fotos coletadas do DOM: {len(imgs)}")
        
        # Se nao achou pelo seletor, pega do HTML completo via regex
        if not imgs:
            content = await page.content()
            found = re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^"\'\s]+', content)
            # Limpa e filtra
            for f in set(found):
                f_clean = f.split(')')[0].split('"')[0].split("'")[0]
                if '-O.' in f_clean or '-F.' in f_clean or '-V.' in f_clean:
                    imgs.append(f_clean)
            print(f"Fotos coletadas via regex no HTML: {len(imgs)}")
            
        # Converte para alta resolucao
        hi_res = []
        for src in imgs:
            full = re.sub(r'-[A-Z]\.(webp|jpg|jpeg)', r'-O.webp', src)
            if full not in hi_res:
                hi_res.append(full)
                
        print(f"Total fotos Full HD: {len(hi_res)}")
        saved = []
        for idx, u in enumerate(hi_res[:8], 1):
            dest = f"img/produto-28-catalog/slide-{idx}.webp"
            try:
                res = await ctx.request.get(u)
                if res.status == 200:
                    body = await res.body()
                    with open(dest, 'wb') as f:
                        f.write(body)
                    print(f"  [+] Salvo slide-{idx}.webp ({len(body)} bytes) <- {u}")
                    saved.append(dest)
            except Exception as e:
                print(f"  [-] Erro ao baixar {u}: {e}")
                
        with open('scripts/data/p28_saved_slides.json', 'w', encoding='utf-8') as jf:
            json.dump(saved, jf, indent=2)
            
        await ctx.close()
        print("[+] Concluido com sucesso!")

if __name__ == '__main__':
    asyncio.run(get_direct_catalog())
