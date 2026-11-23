import urllib.request
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

urls = [
    'https://produto.mercadolivre.com.br/MLB-5532075156-tnis-kappa-pulse-rx-unissex-corrida-conforto-_JM',
    'https://www.mercadolivre.com.br/tenis-kappa-pulse-rx-unissex-corrida-conforto/up/MLBU4011669970'
]

for url in urls:
    print('Fetching:', url)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f'Fetched {len(html)} bytes')
            # Look for reviews or review photos
            reviews = re.findall(r'<p class="ui-review-capability-comments__comment__content">([^<]+)</p>', html)
            print(f'Found {len(reviews)} review texts')
            for r in reviews[:5]:
                print('  Review:', r.strip())
            
            # Look for photos
            photos = re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^"]+', html)
            print(f'Found {len(photos)} mlstatic photos')
            
            # Check for JSON-LD or state
            state_match = re.search(r'__PRELOADED_STATE__\s*=\s*({.+?});', html)
            if state_match:
                print('Found __PRELOADED_STATE__')
    except Exception as e:
        print('Error:', e)
