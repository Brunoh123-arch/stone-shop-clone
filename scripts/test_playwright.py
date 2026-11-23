from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    url = "https://stoneshopclone.vercel.app/pages/produto-104.html?test=1"
    print("Navigating to", url)
    page.goto(url, wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(2500)
    print("Page title:", page.title())
    
    # check broken images
    broken_imgs = page.evaluate("""() => {
        const imgs = Array.from(document.querySelectorAll('img'));
        return imgs.filter(img => img.complete && img.naturalWidth === 0).map(img => img.src);
    }""")
    print("Broken images count:", len(broken_imgs))
    if broken_imgs:
        print("Broken images:", broken_imgs[:5])
    
    # check creators-section
    creators_info = page.evaluate("""() => {
        const el = document.getElementById('creators-section');
        if (!el) return { found: false };
        const style = window.getComputedStyle(el);
        const cards = el.querySelectorAll('.creator-card');
        return {
            found: true,
            display: style.display,
            visibility: style.visibility,
            cardCount: cards.length
        };
    }""")
    print("Creators info:", creators_info)
    browser.close()
