import urllib.request
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

for cat, url in [('shapewear', 'https://shop.tiktok.com/br/c/shapewear/601259'), ('vacuums', 'https://shop.tiktok.com/br/c/vacuums-floor-care/601102')]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"{cat}: Status {resp.status}, len {len(html)}")
            if "Security Check" in html:
                print("  Hit Security Check")
            else:
                imgs = re.findall(r'https://[^"\'\s]+ibyteimg\.com/[^"\'\s]+', html)
                print(f"  ibyteimg URLs found: {len(imgs)}")
                for im in list(dict.fromkeys(imgs))[:8]:
                    print("   ", im)
    except Exception as e:
        print(f"{cat}: Error", e)
