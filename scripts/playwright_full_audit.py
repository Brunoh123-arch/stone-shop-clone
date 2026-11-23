import asyncio
import os, glob, re, json
from playwright.async_api import async_playwright

BASE_URL = "https://stoneshopclone.vercel.app"

async def audit_product(page, pid):
    url = f"{BASE_URL}/pages/produto-{pid}.html"
    errors = []
    console_errors = []
    failed_requests = []
    
    # Catch console errors
    page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    # Catch failed network requests
    page.on("requestfailed", lambda req: failed_requests.append(f"{req.method} {req.url} - {req.failure}"))
    
    try:
        resp = await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await page.wait_for_timeout(1000) # Wait 1s for JS execution
        
        status = resp.status if resp else "No resp"
        curr_url = page.url
        
        # Check if redirected (e.g. unified clone)
        is_redirect = curr_url != url
        if is_redirect:
            return {
                "pid": pid,
                "url": url,
                "status": status,
                "redirected_to": curr_url,
                "is_clone_redirect": True,
                "issues": []
            }
            
        # 1. Page Title & H1
        title = await page.title()
        h1 = await page.evaluate("() => document.querySelector('h1')?.innerText?.trim() || ''")
        if not h1:
            errors.append("H1 missing or empty")
            
        # 2. Check Broken Images (naturalWidth === 0)
        broken_imgs = await page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs.filter(img => img.complete && img.naturalWidth === 0 && img.src && !img.src.includes('data:'))
                       .map(img => ({ src: img.src, alt: img.alt || '', cls: img.className }));
        }""")
        if broken_imgs:
            for b in broken_imgs:
                errors.append(f"Broken image: {b['src'][:70]}")
                
        # 3. Check Creators Section
        creators_info = await page.evaluate("""() => {
            const sec = document.querySelector('#creators-section, .creators-section');
            if (!sec) return { exists: false };
            const style = window.getComputedStyle(sec);
            const isVisible = style.display !== 'none' && style.visibility !== 'hidden' && sec.offsetHeight > 0;
            const cards = Array.from(sec.querySelectorAll('.creator-card, [class*="creator"]'));
            const videos = Array.from(sec.querySelectorAll('video')).map(v => v.src);
            const titles = Array.from(sec.querySelectorAll('.creator-name, .creator-username, h3, h4')).map(el => el.innerText.trim());
            return { exists: true, isVisible, cardCount: cards.length, videos: videos.slice(0, 5), titles: titles.slice(0, 5) };
        }""")
        
        # 4. Check Description Video (#tt-product-video)
        desc_video = await page.evaluate("""() => {
            const v = document.querySelector('#tt-product-video, .product-video-player');
            if (!v) return null;
            const style = window.getComputedStyle(v);
            return { src: v.src, isVisible: style.display !== 'none' && style.visibility !== 'hidden' };
        }""")
        
        # 5. Check Reviews Section
        reviews_info = await page.evaluate("""() => {
            const sec = document.querySelector('.reviews-section, #reviews-section');
            if (!sec) return { exists: false };
            const cards = Array.from(sec.querySelectorAll('.review-card'));
            const photos = Array.from(sec.querySelectorAll('.review-photos img')).map(img => img.src);
            return { exists: true, cardCount: cards.length, photoCount: photos.length };
        }""")
        
        # 6. Check Action Buttons
        has_buy_button = await page.evaluate("""() => {
            const btn = document.querySelector('.btn-comprar, .buy-now, #buy-button, .btn-buy, button[class*="buy"], button[class*="comprar"]');
            return btn !== null;
        }""")
        if not has_buy_button:
            errors.append("No Buy / Checkout button detected")
            
        # Save screenshot if serious errors
        screenshot_path = ""
        if len(errors) > 0 or len(console_errors) > 2:
            os.makedirs(".playwright-audit-screenshots", exist_ok=True)
            screenshot_path = f".playwright-audit-screenshots/p{pid}_issue.png"
            await page.screenshot(path=screenshot_path, full_page=False)
            
        return {
            "pid": pid,
            "url": url,
            "status": status,
            "title": title[:50],
            "h1": h1[:50],
            "creators": creators_info,
            "desc_video": desc_video,
            "reviews": reviews_info,
            "broken_imgs_count": len(broken_imgs),
            "console_errors": console_errors[:3],
            "failed_requests": failed_requests[:3],
            "issues": errors,
            "screenshot": screenshot_path
        }
        
    except Exception as e:
        return {
            "pid": pid,
            "url": url,
            "error": str(e),
            "issues": [f"Exception: {str(e)[:100]}"]
        }

async def main():
    print("Iniciando auditoria visual e estrutural com Playwright em produção...")
    
    # Get all product IDs from pages/produto-*.html
    files = glob.glob("pages/produto-*.html")
    pids = sorted([int(re.search(r'produto-(\d+)\.html', f).group(1)) for f in files])
    print(f"Total de produtos a auditar: {len(pids)}")
    
    results = []
    async with async_playwright() as p:
        # Launch Chromium headless
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 390, "height": 844}, # iPhone 12/13/14 mobile viewport (padrão TikTok Shop)
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        )
        
        # Test in batches of 5 to avoid overwhelming connection
        batch_size = 5
        for i in range(0, len(pids), batch_size):
            batch = pids[i:i+batch_size]
            tasks = []
            pages = []
            for pid in batch:
                page = await context.new_page()
                pages.append(page)
                tasks.append(audit_product(page, pid))
                
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            for page in pages:
                await page.close()
                
            # Log progress
            done = min(i + batch_size, len(pids))
            print(f"  Auditados {done}/{len(pids)} produtos...")
            
        await browser.close()
        
    with open("scripts/playwright_audit_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print("\n=== RESUMO DA AUDITORIA PLAYWRIGHT ===")
    total = len(results)
    redirects = [r for r in results if r.get("is_clone_redirect")]
    with_issues = [r for r in results if r.get("issues") and len(r["issues"]) > 0]
    visible_creators = [r for r in results if r.get("creators", {}).get("isVisible")]
    hidden_creators = [r for r in results if r.get("creators", {}).get("exists") and not r.get("creators", {}).get("isVisible")]
    broken_img_prods = [r for r in results if r.get("broken_imgs_count", 0) > 0]
    
    print(f"Total de produtos verificados: {total}")
    print(f"Clones com redirecionamento limpo: {len(redirects)}")
    print(f"Produtos com carrossel de criadores visivel: {len(visible_creators)}")
    print(f"Produtos com carrossel de criadores ocultado (display:none): {len(hidden_creators)}")
    print(f"Produtos com imagens quebradas: {len(broken_img_prods)}")
    print(f"Produtos com outros problemas: {len(with_issues)}")
    
    if broken_img_prods:
        print("\n[ALERTA] Produtos com imagens quebradas:")
        for r in broken_img_prods:
            print(f"  P{r['pid']}: {r['broken_imgs_count']} imagens quebradas ({r['url']})")
            
    if with_issues:
        print("\n[ALERTA] Produtos com problemas detectados:")
        for r in with_issues[:15]:
            print(f"  P{r.get('pid')}: {r.get('issues')}")

if __name__ == "__main__":
    asyncio.run(main())
