import os
import re
from bs4 import BeautifulSoup

shard2_ids = [26, 28, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 45, 46, 47, 48, 49, 50]

for pid in shard2_ids:
    filepath = f"pages/produto-{pid}.html"
    if not os.path.exists(filepath):
        print(f"[{pid}] NOT FOUND")
        continue

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Title
    title_el = soup.find("h1") or soup.find("title")
    title = title_el.get_text(strip=True) if title_el else "NO TITLE"

    # Creators section
    creators_sec = soup.find(id="creators-section")
    creators_info = "NONE"
    if creators_sec:
        style = creators_sec.get("style", "")
        children = len(creators_sec.find_all(recursive=False))
        creators_info = f"Found (style='{style}', children={children})"

    # Video description
    video_blocks = soup.select(".product-video-block, #tt-product-video, video")
    video_info = []
    for vb in video_blocks:
        src = vb.get("src") or (vb.find("source").get("src") if vb.find("source") else None)
        video_info.append(f"{vb.name}#{vb.get('id', '')}.{'.'.join(vb.get('class', []))} src={src}")

    # Buy / Cart buttons
    btn_buy = soup.find(id=re.compile(r"buy|comprar", re.I)) or soup.select(".btn-buy, .buy-button, .btn-primary")
    btn_cart = soup.find(id=re.compile(r"cart|carrinho", re.I)) or soup.select(".btn-cart, .cart-button")

    # Competitor mentions
    competitors = re.findall(r"(shopee|mercado\s*livre|aliexpress|amazon|magalu)", html, re.I)

    # Images
    images = soup.find_all("img")
    empty_src_imgs = [img.get("src") for img in images if not img.get("src")]

    print(f"=== ID {pid}: {title[:50]} ===")
    print(f"  Creators Section: {creators_info}")
    print(f"  Videos: {video_info}")
    print(f"  Competitor mentions: {set(competitors)}")
    print(f"  Total Images: {len(images)}, Empty src: {len(empty_src_imgs)}")
    print(f"  Buttons: Buy={bool(btn_buy)}, Cart={bool(btn_cart)}")
