import urllib.request
import urllib.parse
import json
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

queries = [
    'fralda huggies supreme care pacote',
    'lencos umedecidos huggies pacote',
    'fralda pampers pants pacote',
    'combo fraldas huggies lencos'
]

# We can query duckduckgo images API
for q in queries:
    print(f"\n--- Querying: {q} ---")
    try:
        # First get token from duckduckgo
        token_url = f"https://duckduckgo.com/?q={urllib.parse.quote(q)}"
        req = urllib.request.Request(token_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode('utf-8')
        vqd_match = re.search(r'vqd=([\d-]+)', body)
        if not vqd_match:
            vqd_match = re.search(r'vqd=\"([^\"]+)\"', body)
        
        if vqd_match:
            vqd = vqd_match.group(1)
            img_api = f"https://duckduckgo.com/i.js?l=wt-wt&o=json&q={urllib.parse.quote(q)}&vqd={vqd}&f=,,,&p=1"
            req2 = urllib.request.Request(img_api, headers=headers)
            with urllib.request.urlopen(req2, timeout=10) as r2:
                data = json.loads(r2.read().decode('utf-8'))
                results = data.get('results', [])
                print(f"Found {len(results)} images")
                for item in results[:5]:
                    print("Image:", item.get('image'), "title:", item.get('title')[:60])
        else:
            print("No vqd found")
    except Exception as e:
        print("Error:", e)
