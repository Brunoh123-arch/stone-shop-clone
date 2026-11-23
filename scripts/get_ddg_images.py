import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def ddg_image_search(query):
    print(f"\n--- DDG Search: {query} ---")
    url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            # find links
            print(f"HTML size: {len(html)}")
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    # Use DuckDuckGo JSON image search API:
    # 1. get vqd token
    q = "body modelador cinta compressao efeito lipo"
    req = urllib.request.Request(f"https://duckduckgo.com/?q={urllib.parse.quote(q)}", headers=headers)
    with urllib.request.urlopen(req) as r:
        html = r.read().decode('utf-8')
        vqd = re.search(r'vqd=([0-9-]+)', html)
        if not vqd:
            vqd = re.search(r'vqd=\"([^\"]+)\"', html)
        print("VQD:", vqd.group(1) if vqd else "None")
        if vqd:
            vqd_val = vqd.group(1)
            api_url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(q)}&vqd={vqd_val}&f=,,,&p=1"
            req2 = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req2) as r2:
                data = json.loads(r2.read().decode('utf-8'))
                results = data.get('results', [])
                print(f"Results: {len(results)}")
                for res in results[:10]:
                    print("Image:", res.get('image'))
