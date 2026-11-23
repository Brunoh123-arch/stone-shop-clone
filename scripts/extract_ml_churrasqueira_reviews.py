import urllib.request
import json
import os

url = "https://www.mercadolivre.com.br/noindex/catalog/reviews/MLB21455267/search?limit=50"
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MercadoLibre/10.320.0',
    'Accept': 'application/json, text/plain, */*'
}

req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode('utf-8'))

reviews = data.get('reviews', [])
print(f"Total reviews no payload: {len(reviews)}")

all_photos = []
for idx, r in enumerate(reviews):
    media = r.get('media', [])
    content = r.get('content', '')
    title = r.get('title', '')
    author = r.get('author', {})
    rating = r.get('rating', 5)
    
    if media:
        print(f"\n--- Review com foto #{idx+1} (Nota {rating}) ---")
        print(f"Autor: {author}")
        print(f"Texto: {title} - {content[:100]}...")
        for m in media:
            img_url = m.get('url') or m.get('uri') or m.get('original_url') or m.get('image_url')
            print(f"  Foto: {img_url}")
            all_photos.append({
                'url': img_url,
                'author': author,
                'content': content,
                'title': title,
                'rating': rating,
                'media_obj': m
            })

os.makedirs('temp_ml_churrasqueira', exist_ok=True)
with open('temp_ml_churrasqueira/reviews_photos.json', 'w', encoding='utf-8') as f:
    json.dump(all_photos, f, indent=2, ensure_ascii=False)

print(f"\nTotal de fotos de compradores encontradas: {len(all_photos)}")
