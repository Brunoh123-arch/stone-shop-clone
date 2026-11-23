import urllib.request, urllib.parse, json, re, time

queries = [
    'site:tiktok.com "chinelo" "strass"',
    'site:tiktok.com "rasteirinha" "strass"',
    'site:tiktok.com "chinelo de strass" unboxing',
    'site:tiktok.com "rasteirinha strass" comprei',
    'site:tiktok.com "chinelo no strass" tiktok shop',
    'site:tiktok.com "chinelo pedraria" nos pes',
    'site:tiktok.com "chinelo strass" review',
    'site:tiktok.com "sandalia rasteira strass"',
    'site:tiktok.com "rasteira brilho" shopee tiktok',
    'site:tiktok.com "chinelo luxo strass" provador'
]

all_links = set()

for q in queries:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            uddg_links = re.findall(r'uddg=([^&]+)', html)
            for u in uddg_links:
                dec = urllib.parse.unquote(u)
                if 'tiktok.com/@' in dec and '/video/' in dec:
                    # Clean query params from tiktok URL
                    clean_tt = dec.split('?')[0].split('#')[0]
                    all_links.add(clean_tt)
        time.sleep(0.5)
    except Exception as e:
        print(f"Erro na query '{q}': {e}")

print(f"Total de links unicos do TikTok encontrados: {len(all_links)}")
with open('scripts/chinelo_tiktok_links.json', 'w', encoding='utf-8') as f:
    json.dump(list(all_links), f, indent=2)

for l in list(all_links)[:10]:
    print(' ', l)
