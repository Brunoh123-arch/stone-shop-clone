import asyncio
import json
import re
from playwright.async_api import async_playwright

SHARD_1_IDS = [4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
BASE_URL = "https://stoneshopclone.vercel.app/pages/produto-{}.html?test=1"

COMPETITOR_TERMS = [
    r'\bshopee\b', r'\bmercado\s*livre\b', r'\bmeli\b', r'\baliexpress\b',
    r'\bamazon\b', r'\bmagalu\b', r'\bshein\b', r'\bcasas\s*bahia\b',
    r'\bamericanas\b'
]

async def audit_product(browser, pid):
    url = BASE_URL.format(pid)
    page = await browser.new_page(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    )
    
    console_errors = []
    page_errors = []
    failed_requests = []
    
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
    page.on("requestfailed", lambda req: failed_requests.append(f"{req.url} ({req.failure})"))
    
    result = {
        "id": pid,
        "url": url,
        "status": None,
        "title": None,
        "broken_images": [],
        "slider_images": [],
        "creators_section": {},
        "desc_video": {},
        "competitor_mentions": [],
        "review_summary": {},
        "buttons": {},
        "console_errors": console_errors,
        "page_errors": page_errors,
        "failed_requests": failed_requests,
    }
    
    try:
        resp = await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        result["status"] = resp.status if resp else "no_response"
        result["title"] = await page.title()
        
        # Give JS time for videos-criadores.js and UI hydration
        await page.wait_for_timeout(2500)
        
        # 1. Broken images check & slider images
        img_data = await page.evaluate('''() => {
            const allImgs = Array.from(document.querySelectorAll('img'));
            const broken = [];
            const sliderImgs = [];
            
            allImgs.forEach(img => {
                const src = img.currentSrc || img.src || img.getAttribute('src') || '';
                const isBroken = img.complete && img.naturalWidth === 0;
                const isSlider = !!img.closest('.slider-track, .swiper-wrapper, .product-gallery, .gallery, .slider, .carousel');
                const isReview = !!img.closest('.review-card, .reviews-section, .reviews-container');
                
                if (isSlider) {
                    sliderImgs.push({
                        src: src,
                        naturalWidth: img.naturalWidth,
                        naturalHeight: img.naturalHeight,
                        isBroken: isBroken
                    });
                }
                
                if (isBroken) {
                    broken.push({
                        src: src,
                        alt: img.alt || '',
                        className: img.className || '',
                        isSlider: isSlider,
                        isReview: isReview,
                        parentElement: img.parentElement ? img.parentElement.tagName + '.' + img.parentElement.className : 'unknown'
                    });
                }
            });
            
            return { broken, sliderImgs };
        }''')
        
        result["broken_images"] = img_data["broken"]
        result["slider_images"] = img_data["sliderImgs"]
        
        # 2. Creators Section inspection
        creators_info = await page.evaluate('''() => {
            const el = document.getElementById('creators-section');
            if (!el) return { exists: false };
            
            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();
            const cards = el.querySelectorAll('.creator-card, video');
            
            return {
                exists: true,
                display: style.display,
                visibility: style.visibility,
                opacity: style.opacity,
                height: rect.height,
                width: rect.width,
                cardCount: cards.length,
                innerHTMLTrimmed: el.innerHTML.trim().length,
                hasGap: rect.height > 10 && cards.length === 0 && style.display !== 'none'
            };
        }''')
        result["creators_section"] = creators_info
        
        # 3. Description Video inspection
        video_info = await page.evaluate('''() => {
            const block = document.querySelector('.product-video-block');
            const vid = document.getElementById('tt-product-video') || (block ? block.querySelector('video') : null);
            
            if (!vid && !block) return { exists: false };
            
            const src = vid ? (vid.currentSrc || vid.src || vid.getAttribute('src') || '') : '';
            const poster = vid ? (vid.poster || vid.getAttribute('poster') || '') : '';
            
            return {
                exists: true,
                hasBlock: !!block,
                hasVideoTag: !!vid,
                src: src,
                poster: poster,
                paused: vid ? vid.paused : null
            };
        }''')
        result["desc_video"] = video_info
        
        # 4. Review inspection (cards, competitor mentions, unboxing photos)
        review_info = await page.evaluate('''() => {
            const cards = Array.from(document.querySelectorAll('.review-card'));
            const reviewData = [];
            
            cards.forEach((card, idx) => {
                const authorEl = card.querySelector('.review-user-name, .author-name, .review-author');
                const commentEl = card.querySelector('.review-comment, .comment, .review-text');
                const varEl = card.querySelector('.review-variation, .variation, [data-author-variation]');
                const photos = Array.from(card.querySelectorAll('img.review-photo, .review-photos img'));
                
                reviewData.push({
                    index: idx,
                    author: authorEl ? authorEl.textContent.trim() : '',
                    comment: commentEl ? commentEl.textContent.trim() : '',
                    variation: varEl ? varEl.textContent.trim() : '',
                    photoCount: photos.length,
                    photos: photos.map(p => ({
                        src: p.currentSrc || p.src,
                        naturalWidth: p.naturalWidth,
                        naturalHeight: p.naturalHeight,
                        isBroken: p.complete && p.naturalWidth === 0
                    }))
                });
            });
            
            return {
                totalReviews: cards.length,
                reviews: reviewData
            };
        }''')
        
        result["review_summary"] = {
            "totalReviews": review_info["totalReviews"],
            "reviewsWithPhotos": sum(1 for r in review_info["reviews"] if r["photoCount"] > 0),
            "totalPhotos": sum(r["photoCount"] for r in review_info["reviews"]),
        }
        
        # Search for competitor mentions in reviews & body text
        body_text = await page.evaluate("() => document.body.innerText")
        for comp_pattern in COMPETITOR_TERMS:
            matches = re.findall(comp_pattern, body_text, re.IGNORECASE)
            if matches:
                result["competitor_mentions"].append({
                    "pattern": comp_pattern,
                    "matches": matches
                })
        
        # 5. Buttons inspection (Comprar agora & Adicionar ao carrinho)
        buttons_info = await page.evaluate('''() => {
            const buyNow = document.getElementById('btn-buy') || document.querySelector('.btn-buy, .buy-now, #buy-now-btn');
            const addCart = document.getElementById('btn-add-cart') || document.querySelector('.btn-add-cart, .add-to-cart, #add-to-cart-btn');
            
            const getBtnState = (el, name) => {
                if (!el) return { name, exists: false };
                const style = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();
                return {
                    name,
                    exists: true,
                    tagName: el.tagName,
                    id: el.id,
                    className: el.className,
                    text: el.textContent.trim(),
                    display: style.display,
                    visibility: style.visibility,
                    disabled: el.disabled || el.getAttribute('aria-disabled') === 'true',
                    width: rect.width,
                    height: rect.height,
                    isVisible: style.display !== 'none' && style.visibility !== 'hidden' && rect.height > 0
                };
            };
            
            return {
                buyNow: getBtnState(buyNow, 'Buy Now'),
                addCart: getBtnState(addCart, 'Add to Cart')
            };
        }''')
        result["buttons"] = buttons_info
        
        # Test clicking buy now / add to cart to see if modal/action triggers
        btn_action_test = await page.evaluate('''() => {
            const buyNow = document.getElementById('btn-buy') || document.querySelector('.btn-buy');
            if (!buyNow) return { buyClicked: false, modalOpened: false };
            
            try {
                buyNow.click();
                const modal = document.querySelector('.sku-modal, .checkout-modal, .modal, #sku-modal, #checkout-modal, .buy-modal');
                const modalVisible = modal && window.getComputedStyle(modal).display !== 'none';
                return { buyClicked: true, modalFound: !!modal, modalVisible: !!modalVisible };
            } catch (e) {
                return { buyClicked: true, error: e.toString() };
            }
        }''')
        result["button_action_test"] = btn_action_test
        
    except Exception as e:
        result["error"] = str(e)
    finally:
        await page.close()
        
    return result

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        print("Playwright launched in isolated headless mode.")
        
        batch_size = 4
        all_results = []
        for i in range(0, len(SHARD_1_IDS), batch_size):
            batch = SHARD_1_IDS[i:i+batch_size]
            print(f"Auditing batch: {batch}...")
            tasks = [audit_product(browser, pid) for pid in batch]
            batch_results = await asyncio.gather(*tasks)
            all_results.extend(batch_results)
            
        await browser.close()
        
        with open("scripts/shard1_audit_results.json", "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
            
        print("\n================== SHARD 1 LIVE AUDIT REPORT ==================")
        for res in all_results:
            pid = res["id"]
            title = (res.get("title") or "N/A")[:32]
            status = res.get("status")
            broken = len(res.get("broken_images", []))
            creators = res.get("creators_section", {})
            c_disp = creators.get("display") if creators.get("exists") else "NO_DIV"
            c_cards = creators.get("cardCount", 0)
            c_gap = creators.get("hasGap", False)
            vid = res.get("desc_video", {})
            vid_src = (vid.get("src") or "")[:25]
            comp = len(res.get("competitor_mentions", []))
            rev_cnt = res.get("review_summary", {}).get("totalReviews", 0)
            rev_pics = res.get("review_summary", {}).get("reviewsWithPhotos", 0)
            bn = res.get("buttons", {}).get("buyNow", {}).get("isVisible", False)
            ac = res.get("buttons", {}).get("addCart", {}).get("isVisible", False)
            btn_act = res.get("button_action_test", {})
            m_open = btn_act.get("modalVisible", False)
            errs = len(res.get("console_errors", [])) + len(res.get("page_errors", []))
            
            print(f"ID {pid:02d} [{status}]: {title:<32} | BrokenImg: {broken} | Creators: disp={c_disp}, cards={c_cards}, gap={c_gap} | Vid: {vid_src:<25} | Comp: {comp} | Rev: {rev_cnt} ({rev_pics} w/pics) | Btns: Buy={bn}, Cart={ac}, Modal={m_open} | Errs: {errs}")

if __name__ == "__main__":
    asyncio.run(main())
