from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 375, "height": 812})
    url = "https://stoneshopclone.vercel.app/pages/produto-92.html?test=1"
    print("Navigating to P92...")
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(3000)
    
    broken = page.evaluate("""() => {
        const allImgs = Array.from(document.querySelectorAll('img'));
        const brokenImgs = [];
        for (const img of allImgs) {
            if (img.id === 'tt-action-avatar') continue;
            if (img.complete && img.naturalWidth === 0) {
                brokenImgs.push(img.src);
            }
        }
        return brokenImgs;
    }""")
    print("P92 broken images:", len(broken), broken)
    
    creators = page.evaluate("""() => {
        const el = document.getElementById('creators-section');
        return el ? { display: window.getComputedStyle(el).display, cards: el.querySelectorAll('.creator-card').length } : null;
    }""")
    print("P92 creators:", creators)
    browser.close()
