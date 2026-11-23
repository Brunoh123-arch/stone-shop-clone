import urllib.request
import urllib.parse
import json
import time
import subprocess
import os

candidates = [
    ("michellypontess", "https://www.tiktok.com/@michellypontess/video/7663515849726233876"),
    ("loyslanetoledo", "https://www.tiktok.com/@loyslanetoledo/video/7531009860641623302"),
    ("anarecomendaa", "https://www.tiktok.com/@anarecomendaa/video/7679810671202012424"),
    ("milenarauujoo", "https://www.tiktok.com/@milenarauujoo/video/7630804808617774356"),
    ("raquel.hsn", "https://www.tiktok.com/@raquel.hsn/video/7677748532681461010"),
    ("dudapjdicas", "https://www.tiktok.com/@dudapjdicas/video/7670182729660632340"),
    ("thaisgodynha", "https://www.tiktok.com/@thaisgodynha/video/7657962583017671944")
]

headers = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('temp_test', exist_ok=True)

for name, url in candidates:
    print(f"Testing {name}...")
    api = f"https://www.tikwm.com/api/?url={urllib.parse.quote(url)}"
    try:
        req = urllib.request.Request(api, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read().decode('utf-8'))
            if res.get('code') == 0:
                d = res['data']
                author = d.get('author', {})
                print(f"  FOUND: {author.get('nickname')} (@{author.get('unique_id')})")
                print(f"  Title: {d.get('title')}")
                play_url = d.get('play')
                # Download
                req2 = urllib.request.Request(play_url, headers=headers)
                vpath = f"temp_test/{name}.mp4"
                fpath = f"temp_test/{name}.jpg"
                with urllib.request.urlopen(req2, timeout=15) as r2, open(vpath, 'wb') as f:
                    f.write(r2.read())
                subprocess.run(['ffmpeg', '-y', '-ss', '00:00:03', '-i', vpath, '-vframes', '1', fpath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  Downloaded and frame extracted: {fpath}")
                # Save metadata
                with open(f"temp_test/{name}.json", 'w', encoding='utf-8') as jf:
                    json.dump(d, jf, ensure_ascii=False, indent=2)
            else:
                print(f"  Error: {res.get('msg')}")
    except Exception as e:
        print(f"  Exception: {e}")
    time.sleep(2)
