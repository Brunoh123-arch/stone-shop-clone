import urllib.request
import re

urls = [
    'https://shop.tiktok.com/br/pdp/cinta-modeladora-cos-alto-media-compressao/1731311480963368117',
    'https://shop.tiktok.com/br/pdp/short-cinta-modeladora-alta-compressao-efeito-empina-barbatanas-antienrolamento-forro-antibacteri/1737541224990213779',
    'https://shop.tiktok.com/br/pdp/body-modelador-compressao-abdominal-fecho-frontal/1733651206797493907',
    'https://shop.tiktok.com/br/pdp/body-modelador-feminino-fio-compressao-e-conforto/1734383629760562835'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

for url in urls:
    print(f"\nFetching: {url}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"Status: {resp.status}, Length: {len(html)}")
            title = re.search(r'<title>([^<]+)</title>', html)
            print("Title:", title.group(1) if title else "N/A")
            
            # Check for reviews/ratings
            reviews = re.findall(r'(\d+[\d.,]*\s*avaliações)', html, re.IGNORECASE)
            print("Reviews text:", reviews[:3])
            
            # Check for buyers/comments
            verified = re.findall(r'Compras verificadas', html)
            print(f"Verified count: {len(verified)}")
            
            # Check for ibyteimg
            imgs = re.findall(r'https://[^"\'\s<>]+ibyteimg\.com/[^"\'\s<>]+', html)
            print(f"ibyteimg count: {len(imgs)}")
            for im in list(dict.fromkeys(imgs))[:5]:
                print("  IMG:", im)
                
            # Check for avatars
            avatars = re.findall(r'https://[^"\'\s<>]+tiktokcdn\.com/[^"\'\s<>]+', html)
            print(f"Avatar count: {len(avatars)}")
            for av in list(dict.fromkeys(avatars))[:3]:
                print("  AVATAR:", av)
    except Exception as e:
        print("Error:", e)
