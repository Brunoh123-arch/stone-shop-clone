from playwright.sync_api import sync_playwright
import urllib.parse
import os

os.makedirs('temp_reviews_ml', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    
    # Busca por página de produto no Mercado Livre
    search_url = "https://lista.mercadolivre.com.br/piscina-inflavel-1000-litros"
    print("Acessando busca do ML:", search_url)
    page.goto(search_url, wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    
    # Pegar os primeiros 3 links de produtos
    prod_links = page.evaluate("""() => {
        const links = [];
        const as = document.querySelectorAll('a.poly-component__title, a.ui-search-link');
        for (const a of as) {
            if (a.href && a.href.includes('/p/MLB') || a.href.includes('MLB-')) {
                links.push(a.href);
            }
        }
        return links;
    }""")
    
    print(f"Links de produtos encontrados no ML: {len(prod_links)}")
    
    buyer_photos = []
    for plink in prod_links[:3]:
        print("Navegando no produto:", plink)
        page.goto(plink, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)
        
        # Extrair fotos da galeria de opiniões / avaliações de compradores
        photos = page.evaluate("""() => {
            const urls = [];
            // Seletores comuns de fotos de review no Mercado Livre
            const imgs = document.querySelectorAll('.ui-review-capability-comments__pictures img, .ui-pdp-reviews img, [data-testid="review-picture"] img, .review-photo img, img[src*="user_reviews"]');
            for(const img of imgs) {
                const src = img.src || img.getAttribute('data-src');
                if(src && src.startsWith('http')) urls.push(src);
            }
            return urls;
        }""")
        print(f"Fotos de compradores encontradas neste item: {len(photos)}")
        for ph in photos:
            if ph not in buyer_photos:
                buyer_photos.append(ph)
                
    print(f"Total fotos de compradores reais ML: {len(buyer_photos)}")
    for i, bp in enumerate(buyer_photos):
        print(f"[{i+1}] {bp}")
        
    browser.close()
