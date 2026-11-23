import urllib.request
import json
import re

def search_ml(query):
    encoded = urllib.parse.quote(query)
    url = f"https://api.mercadolibre.com/sites/MLB/search?q={encoded}&limit=5"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            items = []
            for r in data.get('results', [])[:3]:
                item_id = r.get('id')
                item_url = f"https://api.mercadolibre.com/items/{item_id}"
                req_item = urllib.request.Request(item_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_item) as resp_item:
                    item_data = json.loads(resp_item.read().decode('utf-8'))
                    pics = [p.get('secure_url') for p in item_data.get('pictures', [])]
                    items.append({
                        'id': item_id,
                        'title': item_data.get('title'),
                        'pictures': pics
                    })
            return items
    except Exception as e:
        print(f"Error searching ML for '{query}':", e)
        return []

print("--- SABALA DR-909 ---")
sabala_items = search_ml("Sabala DR-909")
for item in sabala_items:
    print("Item:", item['title'])
    for p in item['pictures'][:6]:
        print("  ", p)

print("\n--- POCO X7 PRO ---")
poco_items = search_ml("Poco X7 Pro 5G Amarelo")
for item in poco_items:
    print("Item:", item['title'])
    for p in item['pictures'][:6]:
        print("  ", p)
