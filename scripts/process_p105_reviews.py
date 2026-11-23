import urllib.request
import json
import os
from PIL import Image
import io

url = "https://www.mercadolivre.com.br/noindex/catalog/reviews/MLB51539641/search?limit=30"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone)'})
d = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
reviews = d.get('reviews', [])

selected_photos = []
selected_reviews = []

for r in reviews:
    comment = r.get('comment', {}).get('content', {}).get('text', '')
    media = r.get('media')
    if media:
        for m in media:
            if m.get('type') == 'photo':
                vars = m.get('variations', [])
                if vars:
                    photo_url = vars[0]['url']
                    selected_photos.append((photo_url, comment, r.get('rating', 5)))

print(f"Total photos collected: {len(selected_photos)}")

# Take first 4 unique high quality photos
os.makedirs('img', exist_ok=True)
saved_paths = []
for i, (purl, comment, rating) in enumerate(selected_photos[:4]):
    dest = f"img/review-105-real-{i+1}.jpg"
    print(f"Downloading {purl} -> {dest}")
    img_data = urllib.request.urlopen(purl).read()
    im = Image.open(io.BytesIO(img_data)).convert('RGB')
    
    # Center crop square
    w, h = im.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    im_cropped = im.crop((left, top, right, bottom)).resize((600, 600), Image.Resampling.LANCZOS)
    im_cropped.save(dest, 'JPEG', quality=88)
    print(f"Saved {dest} (600x600)")
    saved_paths.append((dest, comment, rating))

# Save review data
with open('scripts/p105_review_data.json', 'w', encoding='utf-8') as f:
    json.dump(saved_paths, f, indent=2, ensure_ascii=False)
