import os
from bs4 import BeautifulSoup

SHARD_1_IDS = [4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

for pid in SHARD_1_IDS:
    path = f"pages/produto-{pid}.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    
    related = soup.find_all("a", class_="related-card")
    if not related:
        # Check if there is a script or container
        rel_sec = soup.find(class_=lambda c: c and "related" in c)
        print(f"P{pid:02d}: {len(related)} related cards. Section: {rel_sec.get('class') if rel_sec else 'NONE'}")
    else:
        # Check if any related img is broken
        broken = []
        for a in related:
            img = a.find("img")
            if img:
                src = img.get("src", "")
                if not src.startswith("http"):
                    local = src.replace("../", "")
                    if not os.path.exists(local):
                        broken.append((a.get("href"), src))
        print(f"P{pid:02d}: {len(related)} related cards. Broken local imgs: {broken}")
