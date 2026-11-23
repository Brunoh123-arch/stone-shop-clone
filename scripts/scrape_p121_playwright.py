import asyncio
import re
import urllib.request
import io
import os
from PIL import Image
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        direct_urls = [
            "https://www.mercadolivre.com.br/travesseiro-cervical-ortopedico-com-espuma-viscoelastica/p/MLB28795796",
            "https://www.mercadolivre.com.br/travesseiro-ortopedico-cervical-espuma-viscoelastica/p/MLB28114644",
            "https://lista.mercadolivre.com.br/travesseiro-cervical-ortopedico"
        ]

        for url in direct_urls:
            print(f"[*] Testando: {url}")
            try:
                resp = await page.goto(url, wait_until="domcontentloaded", timeout=15000)
                await page.wait_for_timeout(3000)
                title = await page.title()
                print(f"  Titulo retornado: {title}")
                content = await page.content()
                
                # Buscar imagens do mlstatic
                mlstatic_imgs = re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^\s"\'<>]+\.webp', content)
                if not mlstatic_imgs:
                    mlstatic_imgs = re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^\s"\'<>]+\.jpg', content)
                
                print(f"  Total imagens mlstatic encontradas: {len(mlstatic_imgs)}")
                if mlstatic_imgs:
                    for img in set(mlstatic_imgs[:8]):
                        print("    ->", img)
                    break
            except Exception as e:
                print("  Erro:", e)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
