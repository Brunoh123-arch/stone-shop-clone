import urllib.request
import re
import json

u = 'https://shop.tiktok.com/br/pdp/projetor-natalino-3d-16-desenhos-bivolt-portatil-decorativo/1737826901271938502'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8',
}

req = urllib.request.Request(u, headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

# Procura SIGI_STATE ou blocos script de dados
m = re.search(r'<script id="SIGI_STATE" type="application/json">(.*?)</script>', html, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    print("SIGI_STATE top keys:", list(data.keys()))
    with open('scratch/sigi_state_sample.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Saved scratch/sigi_state_sample.json")
else:
    print("No <script id=\"SIGI_STATE\">, searching all scripts")
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    for idx, s in enumerate(scripts):
        if 'review' in s.lower() or 'rating' in s.lower():
            print(f"Script {idx} has review/rating: len {len(s)}")
            print(s[:500])
