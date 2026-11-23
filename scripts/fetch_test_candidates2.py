import urllib.request
import urllib.parse
import json
import time
import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

candidates = [
    ("raniisilvaa", "https://www.tiktok.com/@raniisilvaa/video/7702271671826140434"),
    ("achadinhos.da.kak2", "https://www.tiktok.com/@achadinhos.da.kak2/video/7646738571507911957"),
    ("maariadanielle", "https://www.tiktok.com/@maariadanielle/video/7564055933937126663"),
    ("tassos.shop", "https://www.tiktok.com/@tassos.shop/video/7701261264659565832"),
    ("laguardiaindica", "https://www.tiktok.com/@laguardiaindica/video/7704087253286505746"),
    ("cassia_hair", "https://www.tiktok.com/@cassia_hair/video/7680586982313200917"),
    ("milenarauujoo", "https://www.tiktok.com/@milenarauujoo/video/7630804808617774356"),
    ("josilaineballand", "https://www.tiktok.com/@josilaineballand/video/7703764223611964693")
]

headers = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('temp_test2', exist_ok=True)

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
                vpath = f"temp_test2/{name}.mp4"
                fpath = f"temp_test2/{name}.jpg"
                with urllib.request.urlopen(req2, timeout=15) as r2, open(vpath, 'wb') as f:
                    f.write(r2.read())
                subprocess.run(['ffmpeg', '-y', '-ss', '00:00:03', '-i', vpath, '-vframes', '1', fpath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  Downloaded and frame extracted: {fpath}")
                with open(f"temp_test2/{name}.json", 'w', encoding='utf-8') as jf:
                    json.dump(d, jf, ensure_ascii=False, indent=2)
            else:
                print(f"  Error: {res.get('msg')}")
    except Exception as e:
        print(f"  Exception: {e}")
    time.sleep(2)
