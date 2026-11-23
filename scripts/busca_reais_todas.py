from playwright.sync_api import sync_playwright
import urllib.parse
import urllib.request
import os

os.makedirs('temp_reviews_reais', exist_ok=True)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

queries = [
    'piscina inflavel 1000 litros "avaliações de clientes" fotos',
    'piscina borda inflavel 1000 montada casa quintal foto',
    'piscina inflavel 1000 l no quintal foto real',
    'piscina 1000 litros inflavel "comprei" foto',
]

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

print(f"Total coletadas: {len(all_urls)}")
downloaded = []
for i, u in enumerate(all_urls[:40]):
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
        fpath = os.path.join('temp_reviews_reais', f"real_{i+1:02d}.jpg")
        with open(fpath, 'wb') as f:
            f.write(data)
        downloaded.append((fpath, u))
        print(f"[OK] {i+1}: {u[:80]}")
    except Exception as e:
        pass
