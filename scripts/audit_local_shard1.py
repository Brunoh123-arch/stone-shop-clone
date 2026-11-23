import re
import os
from bs4 import BeautifulSoup

SHARD_1_IDS = [4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

competitor_patterns = [
    re.compile(r'\bshopee\b', re.I),
    re.compile(r'\bmercado\s*livre\b', re.I),
    re.compile(r'\bmeli\b', re.I),
    re.compile(r'\baliexpress\b', re.I),
    re.compile(r'\bamazon\b', re.I),
    re.compile(r'\bmagalu\b', re.I),
    re.compile(r'\bshein\b', re.I)
]

print("=== LOCAL AUDIT OF SHARD 1 PAGES ===")

for pid in SHARD_1_IDS:
    path = f"pages/produto-{pid}.html"
    if not os.path.exists(path):
        print(f"[ERROR] {path} does not exist!")
        continue
        
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
        
    soup = BeautifulSoup(html, "html.parser")
    
    # Title
    h1 = soup.find("h1")
    title = h1.get_text(strip=True) if h1 else "SEM H1"
    
    # 1. Image checks: check all local img src
    missing_imgs = []
    all_imgs = soup.find_all("img")
    for img in all_imgs:
        src = img.get("src", "")
        if not src:
            missing_imgs.append(("EMPTY_SRC", img.get("alt", "")))
            continue
        # Check local path
        if not src.startswith("http") and not src.startswith("//") and not src.startswith("data:"):
            # Normalize path relative to repo root
            # in pages/produto-X.html, ../ points to root
            cleaned = src.split("?")[0].split("#")[0]
            if cleaned.startswith("../"):
                local_path = cleaned[3:]
            elif cleaned.startswith("./"):
                local_path = "pages/" + cleaned[2:]
            elif cleaned.startswith("/"):
                local_path = cleaned[1:]
            else:
                local_path = "pages/" + cleaned
                
            if not os.path.exists(local_path):
                missing_imgs.append((src, local_path))
                
    # 2. Creators section
    creators_div = soup.find(id="creators-section")
    creators_info = "NO_DIV"
    if creators_div:
        style = creators_div.get("style", "")
        classes = creators_div.get("class", [])
        creators_info = f"EXISTS (style='{style}', class='{classes}')"
        
    # 3. Product video block
    video_block = soup.find("div", class_="product-video-block")
    tt_vid = soup.find(id="tt-product-video")
    vid_info = "NO_VIDEO"
    if video_block or tt_vid:
        v_tag = tt_vid or (video_block.find("video") if video_block else None)
        v_src = v_tag.get("src", "") if v_tag else "NO_SRC"
        vid_info = f"SRC: {v_src}"
        
    # 4. Review checks: competitor mentions and images
    comp_found = []
    reviews = soup.find_all("div", class_="review-card")
    for idx, r in enumerate(reviews):
        text = r.get_text()
        for pat in competitor_patterns:
            m = pat.findall(text)
            if m:
                comp_found.append(f"Rev #{idx+1} ({m})")
                
    # Also check whole page text for competitor mentions (outside of script/style)
    # Exclude code or comments
    body = soup.find("body")
    body_text = body.get_text() if body else ""
    page_comp = []
    for pat in competitor_patterns:
        m = pat.findall(body_text)
        if m:
            page_comp.append(f"{m[0]}:{len(m)}")
            
    # 5. Buttons
    buy_btn = soup.find(id="buy-now-btn") or soup.find("button", class_=re.compile(r"buy", re.I)) or soup.find("a", class_=re.compile(r"buy", re.I))
    cart_btn = soup.find(id="add-to-cart-btn") or soup.find("button", class_=re.compile(r"cart", re.I)) or soup.find("a", class_=re.compile(r"cart", re.I))
    
    btns_ok = bool(buy_btn) and bool(cart_btn)
    
    print(f"P{pid:02d} | Title: {title[:32]:<32} | MissingImgs: {len(missing_imgs)} | Creators: {creators_info} | Video: {vid_info[:35]} | RevComp: {comp_found} | PageComp: {page_comp} | Btns: {btns_ok}")
    if missing_imgs:
        for m in missing_imgs[:3]:
            print(f"   -> Missing: {m}")
