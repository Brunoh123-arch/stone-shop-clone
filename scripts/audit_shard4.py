import os
import re
from bs4 import BeautifulSoup

SHARD_IDS = [80, 82, 85, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]

results = []

for pid in SHARD_IDS:
    filepath = f"pages/produto-{pid}.html"
    if not os.path.exists(filepath):
        print(f"ERROR: {filepath} NOT FOUND!")
        continue
    
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    title_el = soup.find("title")
    title = title_el.text.strip() if title_el else "NO TITLE"
    
    # H1 title or product title
    h1 = soup.find("h1")
    h1_text = h1.text.strip() if h1 else ""
    
    # Check #creators-section
    creators_sec = soup.find(id="creators-section")
    creators_status = "Not Found"
    if creators_sec:
        style = creators_sec.get("style", "")
        classes = creators_sec.get("class", [])
        creators_status = f"Present (style='{style}', classes={classes})"
    
    # Check #tt-product-video / .product-video-block
    vid_block = soup.find(class_=re.compile(r"product-video-block|video-block"))
    tt_vid = soup.find(id="tt-product-video")
    any_vid = soup.find_all("video")
    vid_srcs = [v.get("src") or (v.find("source").get("src") if v.find("source") else None) for v in any_vid]
    
    # Check reviews
    reviews = soup.find_all(class_=re.compile(r"review-card|customer-review|comment-card"))
    review_imgs = soup.find_all(class_=re.compile(r"review-img|review-photo|comment-img"))
    
    # Check size guide or other specific elements
    print(f"\n==================== PRODUTO {pid} ====================")
    print(f"Title: {title}")
    print(f"H1: {h1_text[:60]}")
    print(f"Creators Section: {creators_status}")
    print(f"Video block: {'YES' if vid_block else 'NO'}, tt-vid: {'YES' if tt_vid else 'NO'}")
    print(f"Videos: {vid_srcs}")
    print(f"Reviews count: {len(reviews)}, Review images count: {len(review_imgs)}")

