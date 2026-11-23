import glob
import re

pages = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group()))

no_photos = []
with_photos = []

for p in pages:
    pid = int(re.search(r'\d+', p).group())
    txt = open(p, encoding='utf-8').read()
    if 'Redirecionando para a versão oficial' in txt or len(txt) < 1000:
        continue # skip redirect stubs

    reviews = re.findall(r'class="review-card\b', txt)
    photos = re.findall(r'<img[^>]+class=["\'][^"\']*review-img[^"\']*["\']', txt)
    # also check if photos are in review-photos or similar
    if not photos:
        photos = re.findall(r'<div class="review-photos"[^>]*>([\s\S]*?)</div>', txt)
        # filter out empty review-photos
        photos = [ph for ph in photos if '<img' in ph]

    if not photos or len(photos) == 0:
        no_photos.append((pid, len(reviews)))
    else:
        with_photos.append((pid, len(reviews), len(photos)))

print(f"Total active products: {len(no_photos) + len(with_photos)}")
print(f"Products with unboxing photos in reviews: {len(with_photos)}")
print(f"Products with ZERO unboxing photos: {len(no_photos)}")
print("\nZero unboxing photo PIDs:")
for pid, rev_count in no_photos:
    print(f"  P{pid} ({rev_count} reviews)")
