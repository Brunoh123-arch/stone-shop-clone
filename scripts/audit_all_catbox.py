import re
import urllib.request
import json
import concurrent.futures

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js = f.read()

urls = sorted(list(set(re.findall(r'https?://files\.catbox\.moe/[a-zA-Z0-9_\-]+\.mp4', js))))
print(f'Total unique catbox URLs in videos-criadores.js: {len(urls)}')

def check_url(u):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0', 'Range': 'bytes=0-10'})
        with urllib.request.urlopen(req, timeout=7) as r:
            cl = r.headers.get('Content-Length', '0')
            cr = r.headers.get('Content-Range', '')
            data = r.read()
            return u, r.status, len(data), cl, cr
    except Exception as e:
        return u, 'ERR', 0, str(e), ''

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(check_url, u) for u in urls]
    for fut in concurrent.futures.as_completed(futures):
        results.append(fut.result())

zero_byte_urls = [r[0] for r in results if r[2] == 0 or r[1] != 200]
valid_urls = [r[0] for r in results if r[2] > 0 and r[1] == 200]

print(f'Valid video URLs (>0 bytes): {len(valid_urls)}')
print(f'Zero-byte / broken video URLs: {len(zero_byte_urls)}')

with open('scripts/catbox_audit_results.json', 'w', encoding='utf-8') as f:
    json.dump({
        'valid_urls': valid_urls,
        'zero_byte_urls': zero_byte_urls,
        'details': results
    }, f, indent=2)

print('Zero-byte URLs sample:')
for u in zero_byte_urls[:10]:
    print('  ', u)
