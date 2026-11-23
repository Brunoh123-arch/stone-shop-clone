import os
import time
import urllib.request
import re
from playwright.sync_api import sync_playwright

SEARCHES = {
    39: "secador philco psc3500 4 em 1",
    91: "pipoqueira classic retro philco ppi04v",
    92: "conjunto panelas ferro fundido esmaltado 10 pecas",
    95: "maquina de gelo portatil 12kg",
    96: "aparelho jantar oxford ryo maresia 30 pecas",
    97: "jogo jantar canyon porcelana 20 pecas",
    98: "copos cristal long drink 490ml",
    74: "camisa selecao brasil 2026",
    99: "camisa selecao portugal",
    100: "apple iphone 15 128gb"
}

os.makedirs('temp_ml_unboxing', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 800}
    )
    page = context.new_page()

    for pid, query in SEARCHES.items():
        print(f"\n--- Searching P{pid}: {query} ---")
        search_url = f"https://lista.mercadolivre.com.br/{urllib.request.quote(query)}"
        try:
            page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2500)

            # Get top 3 product links
            links = page.evaluate("""() => {
                const links = [];
                const els = document.querySelectorAll('a.poly-component__title, a.ui-search-link, a.ui-search-item__group__element');
                for (const el of els) {
                    if (el.href && (el.href.includes('/p/MLB') || el.href.includes('MLB-') || el.href.includes('produto.mercadolivre.com.br'))) {
                        links.push(el.href);
                    }
                }
                return Array.from(new Set(links)).slice(0, 3);
            }""")
            print(f"P{pid} found {len(links)} links")

            found_photos = []
            for link in links:
                try:
                    page.goto(link, wait_until="domcontentloaded", timeout=20000)
                    page.wait_for_timeout(2500)
                    
                    # Scroll down to reviews
                    page.evaluate("window.scrollBy(0, 2000)")
                    page.wait_for_timeout(1000)

                    photos = page.evaluate("""() => {
                        const urls = [];
                        const imgs = document.querySelectorAll('.ui-review-capability-comments__pictures img, .ui-pdp-reviews img, [data-testid="review-picture"] img, .review-photo img, img[src*="user_reviews"], img[src*="user-reviews"], img[src*="MLA"]');
                        for (const img of imgs) {
                            const src = img.src || img.getAttribute('data-src') || '';
                            if (src.includes('http') && (src.includes('MLA') || src.includes('user_review')) && !src.includes('profile')) {
                                urls.push(src);
                            }
                        }
                        return urls;
                    }""")
                    for ph in photos:
                        # Clean to full high res 2X
                        high_res = re.sub(r'D_NQ_NP_.*?(\d+-MLA\d+_\d+-F)', r'D_NQ_NP_2X_\1', ph)
                        if high_res not in found_photos and 'static.mercadolivre' not in high_res:
                            found_photos.append(high_res)
                    if len(found_photos) >= 4:
                        break
                except Exception as e:
                    print(f"Error visiting link: {e}")

            print(f"P{pid} extracted {len(found_photos)} buyer photos: {found_photos[:4]}")
            
            # Download up to 4 photos for this product
            headers = {'User-Agent': 'Mozilla/5.0'}
            for i, photo_url in enumerate(found_photos[:4]):
                dest = f"img/review-{pid}-real-{i+1}.jpg"
                try:
                    req = urllib.request.Request(photo_url, headers=headers)
                    with urllib.request.urlopen(req, timeout=10) as resp, open(dest, 'wb') as out_f:
                        out_f.write(resp.read())
                    print(f"  Saved {dest} from {photo_url}")
                except Exception as e:
                    print(f"  Failed to download {photo_url}: {e}")

        except Exception as e:
            print(f"Search failed for P{pid}: {e}")

    browser.close()
