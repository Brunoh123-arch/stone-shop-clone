import urllib.request
import json
import re

# Endpoints conhecidos de avaliações do ML
# 1. API pública v1 / v2
# 2. Frontend reviews endpoint
urls = [
    "https://api.mercadolibre.com/reviews/item/MLB7580414006",
    "https://api.mercadolibre.com/reviews/item/MLB21455267",
    "https://www.mercadolivre.com.br/noindex/catalog/reviews/MLB21455267/search?limit=20",
    "https://frontend.mercadolivre.com.br/api/v1/reviews/MLB21455267"
]

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MercadoLibre/10.320.0',
    'Accept': 'application/json, text/plain, */*'
}

for u in urls:
    req = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            print(f"Sucesso {u}: {len(data)} bytes")
            try:
                js = json.loads(data)
                print("Keys:", list(js.keys()) if isinstance(js, dict) else len(js))
            except:
                print("HTML ou texto retornado")
    except urllib.error.HTTPError as e:
        print(f"HTTPError {e.code} em {u}")
    except Exception as e:
        print(f"Erro em {u}: {e}")
