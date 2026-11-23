from playwright.sync_api import sync_playwright

test_pids = [80, 87, 91, 95, 100, 101, 104]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for pid in test_pids:
        page = browser.new_page(viewport={"width": 375, "height": 812})
        url = f"https://stoneshopclone.vercel.app/pages/produto-{pid}.html?test=1"
        page.goto(url, wait_until="domcontentloaded", timeout=15000)
        page.wait_for_timeout(2000)
        
        # Check buttons
        btn_buy = page.query_selector('.btn-buy-now, #buy-now-btn, [data-action="buy"], .buy-now')
        btn_cart = page.query_selector('.btn-add-cart, #add-to-cart-btn, [data-action="cart"], .add-to-cart')
        
        buy_text = btn_buy.inner_text().strip() if btn_buy else "None"
        cart_text = btn_cart.inner_text().strip() if btn_cart else "None"
        
        # Test clicking buy button
        clicked_modal = False
        if btn_buy:
            btn_buy.click()
            page.wait_for_timeout(1000)
            # check if checkout drawer / modal appeared
            modal = page.query_selector('.checkout-drawer, .sku-modal, .drawer-container, #sku-selection-modal, .modal-open, .checkout-modal')
            if modal and modal.is_visible():
                clicked_modal = True
            elif 'checkout' in page.url:
                clicked_modal = True
        
        print(f"P{pid}: Buy='{buy_text}', Cart='{cart_text}', Click response: {clicked_modal}")
        page.close()
    browser.close()
