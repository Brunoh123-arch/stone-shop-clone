import os
import re
import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

SHARD_IDS = [80, 82, 85, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]

def audit_local_file(pid):
    filepath = f"pages/produto-{pid}.html"
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}"}
    
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("title").text.strip() if soup.find("title") else "NO_TITLE"
    
    # 1. Slider images
    slider_imgs = []
    # check swiper or slider container
    slider_container = soup.find(class_=re.compile(r"swiper|slider|gallery|carousel"))
    for img in soup.find_all("img"):
        parent_classes = " ".join(img.find_parent().get("class", [])) if img.find_parent() else ""
        img_classes = " ".join(img.get("class", []))
        if any(k in parent_classes.lower() or k in img_classes.lower() for k in ["slide", "gallery", "thumb", "main-img"]):
            slider_imgs.append(img.get("src", ""))
    
    # 2. Creators section
    creators_el = soup.find(id="creators-section")
    creators_html_style = creators_el.get("style", "") if creators_el else None
    creators_present = creators_el is not None
    
    # 3. Product video block
    video_block = soup.find(class_=re.compile(r"product-video-block"))
    tt_video = soup.find(id="tt-product-video")
    video_src = ""
    if tt_video:
        video_src = tt_video.get("src", "")
    elif video_block:
        v = video_block.find("video")
        if v:
            video_src = v.get("src", "")
    
    # 4. Reviews
    reviews = []
    review_cards = soup.find_all(class_=re.compile(r"review-card|comment-card"))
    for rc in review_cards:
        author_el = rc.find(class_=re.compile(r"author|name|user"))
        author_name = author_el.text.strip() if author_el else ""
        avatar_img = rc.find(class_=re.compile(r"avatar"))
        avatar_src = avatar_img.get("src", "") if avatar_img else ""
        comment_el = rc.find(class_=re.compile(r"text|content|comment-body"))
        comment_text = comment_el.text.strip() if comment_el else ""
        imgs = [img.get("src") for img in rc.find_all("img") if img != avatar_img and img.get("src")]
        reviews.append({
            "author": author_name,
            "avatar": avatar_src,
            "text": comment_text[:80],
            "images": imgs
        })
    
    # 5. Buttons
    buy_now = soup.find(id=re.compile(r"buy-now|btn-buy", re.I)) or soup.find(class_=re.compile(r"buy-now|btn-buy", re.I))
    add_cart = soup.find(id=re.compile(r"add-to-cart|btn-cart", re.I)) or soup.find(class_=re.compile(r"add-to-cart|btn-cart", re.I))
    
    return {
        "pid": pid,
        "title": title,
        "slider_imgs_count": len(slider_imgs),
        "slider_imgs": slider_imgs,
        "creators_present": creators_present,
        "creators_html_style": creators_html_style,
        "video_block_present": video_block is not None,
        "video_src": video_src,
        "reviews_count": len(reviews),
        "review_images_count": sum(len(r["images"]) for r in reviews),
        "reviews_sample": reviews[:3],
        "has_buy_now": buy_now is not None,
        "has_add_cart": add_cart is not None
    }

print("Running local audit for 20 products...")
local_results = {}
for pid in SHARD_IDS:
    local_results[pid] = audit_local_file(pid)

with open("scripts/local_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(local_results, f, indent=2, ensure_ascii=False)

print("Local audit saved to scripts/local_audit_results.json")
