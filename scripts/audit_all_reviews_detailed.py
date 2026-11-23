import glob
import re

pages = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group()))

review_stats = []

for p in pages:
    pid = int(re.search(r'\d+', p).group())
    txt = open(p, encoding='utf-8').read()
    if 'Redirecionando para a versão oficial' in txt or len(txt) < 1000:
        continue

    # count review cards
    cards = re.findall(r'class="review-card\b', txt)
    photos = re.findall(r'<div class="review-photos"[^>]*>([\s\S]*?)</div>', txt)
    # count how many img tags in photos
    img_count = sum(len(re.findall(r'<img\b', ph)) for ph in photos)
    review_stats.append((pid, len(cards), img_count))

print(f"{'PID':<5} | {'Reviews':<8} | {'Photos':<8}")
print("-" * 25)
for pid, revs, photos in review_stats:
    if revs < 20 or photos < 3:
        print(f"P{pid:<4} | {revs:<8} | {photos:<8} <-- Needs upgrade")

print("-" * 25)
print(f"Total active products: {len(review_stats)}")
low_revs = [x for x in review_stats if x[1] < 15]
print(f"Products with < 15 reviews: {len(low_revs)} -> {[x[0] for x in low_revs]}")
