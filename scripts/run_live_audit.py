import json
import time
from playwright.sync_api import sync_playwright

SHARD_IDS = [80, 82, 85, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 375, "height": 812}) # Mobile viewport standard
    page = context.new_page()
    
    for pid in SHARD_IDS:
        url = f"https://stoneshopclone.vercel.app/pages/produto-{pid}.html?test=1"
        print(f"Auditing P{pid}...")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(2000) # allow scripts to initialize
            
            data = page.evaluate("""() => {
                const title = document.title;
                
                // 1. Broken images (filter out hidden elements like modal templates)
                const allImgs = Array.from(document.querySelectorAll('img'));
                const brokenImgs = [];
                for (const img of allImgs) {
                    // Check if img is in a hidden container
                    const isVisible = img.offsetParent !== null || img.offsetWidth > 0 || img.offsetHeight > 0;
                    // If complete and naturalWidth === 0
                    if (img.complete && img.naturalWidth === 0) {
                        // ignore the uninitialized video modal avatar if hidden
                        if (img.id === 'tt-action-avatar') continue;
                        brokenImgs.push({
                            src: img.src,
                            alt: img.alt,
                            className: img.className,
                            parent: img.parentElement ? img.parentElement.className : '',
                            isVisible: isVisible
                        });
                    }
                }
                
                // 2. Creators section
                const creatorsSec = document.getElementById('creators-section');
                let creatorsInfo = { found: false, display: 'none', cardCount: 0, videoUrls: [] };
                if (creatorsSec) {
                    const style = window.getComputedStyle(creatorsSec);
                    const cards = creatorsSec.querySelectorAll('.creator-card');
                    const vids = Array.from(creatorsSec.querySelectorAll('video, [data-video-src]')).map(v => v.src || v.getAttribute('data-video-src'));
                    creatorsInfo = {
                        found: true,
                        display: style.display,
                        cardCount: cards.length,
                        videoUrls: vids.filter(Boolean)
                    };
                }
                
                // 3. Product video block
                const vidEl = document.querySelector('#tt-product-video, .product-video-block video');
                let videoInfo = { found: false, src: '' };
                if (vidEl) {
                    videoInfo = {
                        found: true,
                        src: vidEl.src || vidEl.getAttribute('src') || ''
                    };
                }
                
                // 4. Reviews summary
                const reviewCards = document.querySelectorAll('.review-card, .comment-card');
                const reviewImgs = document.querySelectorAll('.review-card img, .comment-card img');
                
                // 5. Buttons
                const buyBtn = document.querySelector('#buy-now-btn, .buy-now, #btn-comprar, [onclick*="buy"], [data-action="buy"]');
                const cartBtn = document.querySelector('#add-to-cart-btn, .add-to-cart, #btn-carrinho, [onclick*="cart"], [data-action="cart"]');
                
                return {
                    title: title,
                    brokenImgs: brokenImgs,
                    creatorsInfo: creatorsInfo,
                    videoInfo: videoInfo,
                    reviewCount: reviewCards.length,
                    reviewImgsCount: reviewImgs.length,
                    hasBuyBtn: buyBtn !== null,
                    hasCartBtn: cartBtn !== null
                };
            }""")
            
            # test click buy button
            buy_btn_works = False
            try:
                btn = page.query_selector('#buy-now-btn, .buy-now, #btn-comprar, [data-action="buy"], .btn-buy-now')
                if btn and btn.is_visible():
                    # don't actually submit checkout, just check if clickable
                    buy_btn_works = True
            except Exception as e:
                buy_btn_works = False
            
            data["buyBtnClickable"] = buy_btn_works
            results[pid] = data
            print(f"  P{pid}: Broken imgs={len(data['brokenImgs'])}, Creators display={data['creatorsInfo']['display']}, cards={data['creatorsInfo']['cardCount']}, Vid={data['videoInfo']['src'][:30] if data['videoInfo']['src'] else 'None'}")
            
        except Exception as e:
            print(f"  Error auditing P{pid}: {e}")
            results[pid] = {"error": str(e)}

    browser.close()

with open("scripts/live_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nAudit finished! Saved to scripts/live_audit_results.json")
