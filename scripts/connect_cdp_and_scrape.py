import asyncio
import json
import os
import urllib.request
from playwright.async_api import async_playwright

async def main():
    print("Tentando conectar via CDP em http://127.0.0.1:9222...")
    async with async_playwright() as p:
        try:
            browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
            print(">>> CONECTADO AO CHROME COM SUCESSO! <<<")
            
            contexts = browser.contexts
            pages = []
            for c in contexts:
                pages.extend(c.pages)
            print(f"Total de abas abertas no seu Chrome: {len(pages)}")
            
            target_page = None
            for idx, page in enumerate(pages):
                url = page.url
                title = await page.title()
                print(f"Aba {idx + 1}: {title[:60]} | URL: {url[:80]}")
                if "tiktok.com" in url or "shop" in url:
                    target_page = page
                    
            if not target_page and pages:
                target_page = pages[0]
                
            if target_page:
                print(f"\n>>> Piloto automatico ativo na aba: {target_page.url}")
                await target_page.screenshot(path="scripts/cdp_active_tab.png")
                print("Screenshot da sua tela capturada em scripts/cdp_active_tab.png")
                
                # Puxar informacoes de avaliacoes se estiver na pagina de produto
                reviews_data = await target_page.evaluate("""() => {
                    const cards = document.querySelectorAll('[class*="review"], [class*="comment"], [data-e2e*="review"]');
                    const results = [];
                    cards.forEach(c => {
                        const text = c.innerText;
                        const imgs = Array.from(c.querySelectorAll('img')).map(i => i.src);
                        if (text.length > 10) results.push({ text, imgs });
                    });
                    return {
                        title: document.title,
                        url: window.location.href,
                        reviewsCount: results.length,
                        reviews: results
                    };
                }""")
                
                with open("scripts/live_extracted_pdp.json", "w", encoding="utf-8") as f:
                    json.dump(reviews_data, f, indent=2, ensure_ascii=False)
                print(f"Extraidos {reviews_data.get('reviewsCount', 0)} blocos da pagina oficial!")
                
        except Exception as e:
            print("Ainda aguardando Chrome abrir na porta 9222... Erro:", e)

if __name__ == "__main__":
    asyncio.run(main())
