import urllib.request

for i in range(1, 16):
    url = f'https://stoneshopclone.vercel.app/img/reviews-avatars/mulheres_validadas/mulher_{i}.jpg'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            print(f"mulher_{i}.jpg: HTTP {resp.status}, Bytes: {len(data)}")
    except Exception as e:
        print(f"mulher_{i}.jpg: ERRO {e}")
