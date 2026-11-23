import urllib.request
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# Busca direta na API pública de busca do Mercado Livre Brasil
search_url = "https://api.mercadolibre.com/sites/MLB/search?q=Forno%20Eletrico%20HQ%2048%20Litros%20HQ48D"

req = urllib.request.Request(search_url, headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        results = data.get('results', [])
        print(f"Total ML items: {len(results)}")
        for r in results[:4]:
            item_id = r.get('id')
            title = r.get('title')
            price = r.get('price')
            thumb = r.get('thumbnail')
            print(f"[{item_id}] {title} | R$ {price} | {thumb}")
            
            # Pega as fotos full em alta resolução do item
            item_url = f"https://api.mercadolibre.com/items/{item_id}"
            try:
                with urllib.request.urlopen(urllib.request.Request(item_url, headers=headers)) as item_resp:
                    item_data = json.loads(item_resp.read().decode('utf-8'))
                    pics = item_data.get('pictures', [])
                    print(f"  Total pictures: {len(pics)}")
                    for p in pics[:6]:
                        print(f"    PIC: {p.get('secure_url')}")
            except Exception as e:
                print(f"  Erro ao puxar fotos: {e}")
except Exception as e:
    print(f"Erro na busca: {e}")
