from bs4 import BeautifulSoup

SHARD_IDS = [80, 82, 85, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]

for pid in SHARD_IDS:
    path = f"pages/produto-{pid}.html"
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    
    btn_buy = soup.find(id="btn-buy") or soup.find(class_="btn-buy") or soup.find(id="buy-now-btn")
    btn_cart = soup.find(id="btn-add-cart") or soup.find(class_="btn-add-cart") or soup.find(id="add-to-cart-btn")
    
    buy_str = f"id={btn_buy.get('id')}, onclick={btn_buy.get('onclick')}" if btn_buy else "MISSING"
    cart_str = f"id={btn_cart.get('id')}, onclick={btn_cart.get('onclick')}" if btn_cart else "MISSING"
    
    print(f"P{pid}: Buy: [{buy_str}] | Cart: [{cart_str}]")
