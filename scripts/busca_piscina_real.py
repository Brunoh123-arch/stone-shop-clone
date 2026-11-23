from playwright.sync_api import sync_playwright
import urllib.parse
import urllib.request
import os

queries = [
    "piscina inflavel 1000 litros avaliacao fotos clientes compradores",
    "piscina inflavel borda 1000 l montada quintal foto real cliente",
    "piscina inflavel redonda 1000 litros opiniao comprador foto",
    "piscina inflavel 1000 litros desdobrada chao montando foto"
]

os.makedirs('temp_piscina_real', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    all_urls = []
    for q in queries:
        url = f"https://br.images.search.yahoo.com/search/images?p={urllib.parse.quote(q)}"
        page.goto(url)
        page.wait_for_timeout(2000)
        data = page.evaluate("""() => {
            const anchors = Array.from(document.querySelectorAll('a[href*="imgurl="]'));
            return anchors.map(a => a.href);
        }""")
        for href in data:
            parsed = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
            orig = parsed.get('imgurl', [''])[0]
            if orig and orig.startswith('http') and orig not in all_urls:
                all_urls.append(orig)
    browser.close()

print(f"Total de URLs encontradas: {len(all_urls)}")
# Baixar as primeiras 30 para inspecionar
for i, u in enumerate(all_urls[:35]):
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
        fpath = os.path.join('temp_piscina_real', f"cand_{i+1:02d}.jpg")
        with open(fpath, 'wb') as f:
            f.write(data)
        print(f"[OK] {i+1}: {u}")
    except Exception as e:
        pass
