import urllib.request
import urllib.parse
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def search_ddg_images(query, count=8):
    req = urllib.request.Request(f"https://duckduckgo.com/?q={urllib.parse.quote(query)}", headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            html = r.read().decode('utf-8')
            vqd = re.search(r'vqd=([0-9-]+)', html)
            if not vqd:
                vqd = re.search(r'vqd=\"([^\"]+)\"', html)
            if vqd:
                vqd_val = vqd.group(1)
                api_url = f"https://duckduckgo.com/i.js?l=us-en&o=json&q={urllib.parse.quote(query)}&vqd={vqd_val}&f=,,,&p=1"
                req2 = urllib.request.Request(api_url, headers=headers)
                with urllib.request.urlopen(req2) as r2:
                    data = json.loads(r2.read().decode('utf-8'))
                    results = data.get('results', [])
                    imgs = [res.get('image') for res in results if res.get('image') and not res.get('image').endswith('.gif')]
                    return imgs[:count]
    except Exception as e:
        print(f"Error searching {query}: {e}")
    return []

if __name__ == '__main__':
    q1 = "escova secadora 5 em 1 modeladora cabelo profissional multifuncional"
    imgs1 = search_ddg_images(q1, 8)
    print(f"--- Escova 5 em 1 ({len(imgs1)} images) ---")
    for img in imgs1:
        print(img)

    q2 = "modelador de cachos automatico sem fio ceramica recarregavel usb portatil"
    imgs2 = search_ddg_images(q2, 8)
    print(f"\n--- Auto Curler ({len(imgs2)} images) ---")
    for img in imgs2:
        print(img)
