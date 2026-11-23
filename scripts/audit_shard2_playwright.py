import asyncio
import json
from playwright.async_api import async_playwright

shard2_ids = [26, 28, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 45, 46, 47, 48, 49, 50]

async def audit_product(page, pid):
    url = f"https://stoneshopclone.vercel.app/pages/produto-{pid}.html?test=1"
    report = {
        "id": pid,
        "url": url,
        "status": None,
        "broken_images": [],
        "creators_section": {},
        "description_video": {},
        "buttons": {},
        "errors": []
    }
    
    try:
        response = await page.goto(url, wait_until="networkidle", timeout=30000)
        report["status"] = response.status if response else "no_response"
        
        # Wait a moment for dynamic scripts to run (e.g. videos-criadores.js)
        await page.wait_for_timeout(2000)
        
        # 1. Broken images
        broken_imgs = await page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs.filter(img => {
                // If src is empty or naturalWidth === 0 and complete
                if (!img.getAttribute('src')) return true;
                return img.complete && img.naturalWidth === 0;
            }).map(img => ({
                src: img.getAttribute('src'),
                class: img.className,
                id: img.id,
                parent: img.parentElement ? img.parentElement.className : ''
            }));
        }''')
        report["broken_images"] = broken_imgs
        
        # 2. Creators section
        creators_info = await page.evaluate('''() => {
            const el = document.getElementById('creators-section');
            if (!el) return { exists: false };
            const style = window.getComputedStyle(el);
            const rect = el.getBoundingClientRect();
            const childCards = el.querySelectorAll('.creator-card, .creator-preview-card, video');
            return {
                exists: true,
                display: style.display,
                visibility: style.visibility,
                height: rect.height,
                width: rect.width,
                cardsCount: childCards.length,
                innerHTML: el.innerHTML.trim() ? el.innerHTML.trim().substring(0, 150) : ''
            };
        }''')
        report["creators_section"] = creators_info
        
        # 3. Description video
        desc_video = await page.evaluate('''() => {
            const block = document.querySelector('.product-video-block');
            const vid = document.querySelector('#tt-product-video');
            if (!vid && !block) return { exists: false };
            return {
                exists: true,
                hasBlock: !!block,
                blockDisplay: block ? window.getComputedStyle(block).display : null,
                vidSrc: vid ? (vid.getAttribute('src') || (vid.querySelector('source') ? vid.querySelector('source').getAttribute('src') : null)) : null,
                vidDisplay: vid ? window.getComputedStyle(vid).display : null
            };
        }''')
        report["description_video"] = desc_video
        
        # 4. Buttons
        btn_info = await page.evaluate('''() => {
            const buyBtn = document.querySelector('#btn-buy, .btn-buy, .buy-now, [data-action="buy"]');
            const cartBtn = document.querySelector('#btn-cart, .btn-cart, .add-to-cart, [data-action="cart"]');
            return {
                buyExists: !!buyBtn,
                cartExists: !!cartBtn,
                buyVisible: buyBtn ? window.getComputedStyle(buyBtn).display !== 'none' : false,
                cartVisible: cartBtn ? window.getComputedStyle(cartBtn).display !== 'none' : false
            };
        }''')
        report["buttons"] = btn_info
        
    except Exception as e:
        report["errors"].append(str(e))
        
    return report

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Create an isolated/anonymous context
        context = await browser.new_context(
            viewport={"width": 412, "height": 915},
            user_agent="Mozilla/5.0 (Linux; Android 13; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36"
        )
        page = await context.new_page()
        
        results = []
        for pid in shard2_ids:
            print(f"Auditing ID {pid}...")
            res = await audit_product(page, pid)
            results.append(res)
            print(f"ID {pid}: Status={res['status']}, BrokenImgs={len(res['broken_images'])}, CreatorsDisplay={res['creators_section'].get('display')}, Cards={res['creators_section'].get('cardsCount')}, DescVid={res['description_video'].get('vidSrc')}")
            
        with open("scripts/shard2_playwright_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
