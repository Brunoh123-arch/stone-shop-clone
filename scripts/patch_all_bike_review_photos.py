import re
import urllib.request
import os
from PIL import Image
import io

with open('pages/produto-6.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all review-photo src in reviews-section
idx_start = text.find('class="reviews-section"')
if idx_start == -1:
    idx_start = text.find('reviews-section')
idx_end = text.find('<!-- PRODUTOS RELACIONADOS', idx_start)

reviews_html = text[idx_start:idx_end]
photo_urls = re.findall(r'class="review-photo"\s+src="([^"]+)"', reviews_html)
print(f"Total review-photos found: {len(photo_urls)}")

url_map = {}
count = 1
for u in photo_urls:
    if u.startswith('http'):
        dest_filename = f"review-6-c{count}-1.jpg"
        dest_path = os.path.join('img', dest_filename)
        
        # Download and convert
        try:
            req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req, timeout=15).read()
            img = Image.open(io.BytesIO(data))
            img = img.convert('RGB')
            img.save(dest_path, 'JPEG', quality=88)
            print(f"[{count}] Baixado {u[:60]}... -> {dest_path}")
            url_map[u] = f"../img/{dest_filename}"
            count += 1
        except Exception as e:
            print(f"Erro ao baixar {u}: {e}")

print("Downloaded", len(url_map), "images.")

# Now replace in produto-6.html
new_text = text
for orig_url, local_rel in url_map.items():
    new_text = new_text.replace(orig_url, local_rel)

with open('pages/produto-6.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("pages/produto-6.html atualizado com sucesso!")
