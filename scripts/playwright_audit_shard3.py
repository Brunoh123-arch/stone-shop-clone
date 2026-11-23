import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

shard3_ids = [52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 68, 70, 72, 73, 74, 75, 76]
results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 390, 'height': 844}, # iPhone / Mobile viewport
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1'
    )
    page = context.new_page()

    for pid in shard3_ids:
        url = f"https://stoneshopclone.vercel.app/pages/produto-{pid}.html?test=1"
        res_info = {
            'pid': pid,
            'url': url,
            'status': None,
            'title': '',
            'broken_images': [],
            'slider_broken': [],
            'reviews_broken': [],
            'creators_section': {},
            'video_desc': {},
            'reviews_audit': {},
            'buttons': {},
            'errors': []
        }
        
        try:
            resp = page.goto(url, wait_until='networkidle', timeout=30000)
            res_info['status'] = resp.status if resp else None
            time.sleep(1) # allow scripts to settle
            
            res_info['title'] = page.title()

            # 1. Inspect Images
            images_data = page.evaluate("""() => {
                const imgs = Array.from(document.querySelectorAll('img'));
                return imgs.map(img => {
                    const isBroken = img.complete && img.naturalWidth === 0;
                    const inSlider = !!img.closest('.image-slider, .slider-track, .swiper');
                    const inReview = !!img.closest('.reviews-section, .review-card, .review-photos');
                    return {
                        src: img.src,
                        isBroken,
                        inSlider,
                        inReview,
                        naturalWidth: img.naturalWidth,
                        naturalHeight: img.naturalHeight,
                        className: img.className
                    };
                });
            }""")
            
            broken = [img for img in images_data if img['isBroken']]
            res_info['broken_images'] = broken
            res_info['slider_broken'] = [img for img in broken if img['inSlider']]
            res_info['reviews_broken'] = [img for img in broken if img['inReview']]

            # 2. Inspect Creators Section (#creators-section)
            cs_data = page.evaluate("""() => {
                const el = document.getElementById('creators-section');
                if (!el) return { exists: false };
                const style = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return {
                    exists: true,
                    display: style.display,
                    visibility: style.visibility,
                    height: rect.height,
                    width: rect.width,
                    childCount: el.children.length,
                    hasCards: !!el.querySelector('.creator-card, .creator-item'),
                    innerHTML: el.innerHTML.trim().slice(0, 150)
                };
            }""")
            res_info['creators_section'] = cs_data

            # 3. Inspect Video Desc
            vid_data = page.evaluate("""() => {
                const block = document.querySelector('.product-video-block, #product-desc-video-block');
                const vid = document.querySelector('#tt-product-video, .product-video-player, video');
                return {
                    blockExists: !!block,
                    vidExists: !!vid,
                    src: vid ? vid.currentSrc || vid.src : null,
                    paused: vid ? vid.paused : null,
                    readyState: vid ? vid.readyState : null
                };
            }""")
            res_info['video_desc'] = vid_data

            # 4. Inspect Reviews
            rev_data = page.evaluate("""() => {
                const cards = Array.from(document.querySelectorAll('.review-card'));
                const photos = Array.from(document.querySelectorAll('.review-photo, .review-photos img'));
                const comments = cards.map(c => c.getAttribute('data-author-comment') || c.querySelector('.review-comment')?.innerText || '');
                
                const competitorRegex = /\\b(shopee|shope|aliexpress|ali express|amazon|mercado livre|mercadolivre|magalu|lojas americanas)\\b/i;
                const flaggedComments = comments.filter(c => competitorRegex.test(c));
                
                return {
                    totalCards: cards.length,
                    totalPhotos: photos.length,
                    photoSources: photos.map(p => p.src),
                    flaggedComments: flaggedComments
                };
            }""")
            res_info['reviews_audit'] = rev_data

            # 5. Inspect Buttons
            btn_data = page.evaluate("""() => {
                const buyBtn = document.querySelector('.action-btn.buy-now, .btn-buy-now, [onclick*="openDrawer"], [onclick*="handleBuyNow"], [onclick*="openCheckout"]');
                const cartBtn = document.querySelector('.action-btn.add-cart, .btn-add-cart, [onclick*="handleAddToCart"], [onclick*="addToCart"]');
                return {
                    buyBtnExists: !!buyBtn,
                    buyBtnVisible: buyBtn ? (buyBtn.offsetWidth > 0 && buyBtn.offsetHeight > 0) : false,
                    cartBtnExists: !!cartBtn,
                    cartBtnVisible: cartBtn ? (cartBtn.offsetWidth > 0 && cartBtn.offsetHeight > 0) : false,
                };
            }""")
            res_info['buttons'] = btn_data

        except Exception as e:
            res_info['errors'].append(str(e))
            
        results[pid] = res_info
        print(f"Audited P{pid}: status={res_info['status']} | broken_imgs={len(res_info['broken_images'])} | cs_display={res_info['creators_section'].get('display')} | vid={res_info['video_desc'].get('src')} | reviews={res_info['reviews_audit'].get('totalCards')}")

    browser.close()

with open('scripts/audit_shard3_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\nAudit Shard 3 finished! Results saved to scripts/audit_shard3_results.json")
