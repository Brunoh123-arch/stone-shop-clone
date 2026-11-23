import urllib.request
import re
import json

urls = [
    'https://shop.tiktok.com/br/c/vacuums-floor-care/601102',
    'https://shop.tiktok.com/br/c/usb-vacuums/803856'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

all_pdp_links = set()
all_product_ids = set()

for url in urls:
    print(f"Fetching: {url}")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"  Length: {len(html)}")
            
            # Find all PDP hrefs or paths
            pdps = re.findall(r'href=[\'"]([^\'"]*\/pdp\/[^\'"]*)[\'"]', html)
            for p in pdps:
                all_pdp_links.add(p)
            
            # Find product IDs (19 digits starting with 17)
            ids = re.findall(r'\b(173\d{16})\b', html)
            for i in ids:
                all_product_ids.add(i)
                
            # Search for JSON blocks
            json_snippets = re.findall(r'\{[^{}]*"title"[^{}]*"product_id"[^{}]*\}', html)
            print(f"  JSON snippets: {len(json_snippets)}")
    except Exception as e:
        print("  Error:", e)

print(f"\nTotal PDP links: {len(all_pdp_links)}")
for l in sorted(all_pdp_links):
    print("  Link:", l)

print(f"\nTotal Product IDs: {len(all_product_ids)}")
for i in sorted(all_product_ids):
    print("  ID:", i)
