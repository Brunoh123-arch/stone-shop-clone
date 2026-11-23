import urllib.request
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Search Mercado Livre item for Arke Vitta Smart 5
ml_search = "https://lista.mercadolivre.com.br/churrasqueira-eletrica-arke-vitta-smart-5-espetos"
req = urllib.request.Request(ml_search, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    # Find item ids like MLB-xxxx or MLBxxxx
    mlb_ids = re.findall(r'MLB-?(\d{8,12})', html)
    print(f"Found {len(mlb_ids)} MLB IDs:", list(dict.fromkeys(mlb_ids))[:5])
    
    # Let's take the first MLB ID and check reviews API
    for mlb in list(dict.fromkeys(mlb_ids))[:3]:
        api_url = f"https://api.mercadolibre.com/reviews/item/MLB{mlb}?limit=10"
        print("Checking API:", api_url)
        try:
            req_api = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req_api, timeout=5) as r:
                data = json.loads(r.read().decode('utf-8'))
            reviews = data.get('reviews', [])
            print(f"  MLB{mlb} has {len(reviews)} reviews")
            for rev in reviews:
                media = rev.get('media', [])
                if media:
                    print("  Found media in review:", media)
        except Exception as e:
            print(f"  Error on MLB{mlb}:", e)
except Exception as e:
    print("Error ML:", e)
