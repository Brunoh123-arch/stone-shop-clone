import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

queries = [
    'site:tiktok.com elgin air fryer',
    'site:tiktok.com air fryer elgin',
    'site:tiktok.com visio fry',
    'site:tiktok.com fritadeira elgin',
    'site:tiktok.com elgin visio fry',
    'site:tiktok.com air fryer 5l',
    'site:tiktok.com fritadeira eletrica 5l',
    'site:tiktok.com air fryer visio'
]

unique_vids = set()

for q in queries:
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8')
            raw_links = re.findall(r'uddg=([^&]+)', html)
            for l in raw_links:
                dec = urllib.parse.unquote(l)
                m = re.search(r'(https://www\.tiktok\.com/@[^/]+/video/\d+)', dec)
                if m:
                    unique_vids.add(m.group(1))
    except Exception as e:
        print(f"Error {q}: {e}")

print(f"Found {len(unique_vids)} unique TikTok video URLs:")
for v in unique_vids:
    print(v)

with open('temp_tiktok_links.json', 'w') as f:
    json.dump(list(unique_vids), f, indent=2)
