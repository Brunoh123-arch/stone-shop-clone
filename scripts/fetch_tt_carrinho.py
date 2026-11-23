import urllib.request
import urllib.parse
import json
import time
import subprocess
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

candidates = [
    ("layporttt", "https://www.tiktok.com/@layporttt/video/7699276722205723925"),
    ("dicas_da_nanda", "https://www.tiktok.com/@dicas.da.nanda/video/7697029889337117973"),
    ("daniellaaribeiro", "https://www.tiktok.com/@daniellaaribeiro/video/7681767361292029202")
]

headers = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('temp_tt_candidates', exist_ok=True)

for name, url in candidates:
    print(f"Testing {name} ({url})...")
    api = f"https://www.tikwm.com/api/?url={urllib.parse.quote(url)}"
    try:
        req = urllib.request.Request(api, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            res = json.loads(r.read().decode('utf-8'))
            if res.get('code') == 0:
                d = res['data']
                author = d.get('author', {})
                print(f"  SUCCESS!")
                print(f"  Author: {author.get('nickname')} (@{author.get('unique_id')})")
                print(f"  Avatar: {author.get('avatar')}")
                print(f"  Title: {d.get('title')}")
                print(f"  Duration: {d.get('duration')}s")
                play_url = d.get('play')
                # Download video
                vpath = f"temp_tt_candidates/{name}.mp4"
                fpath = f"temp_tt_candidates/{name}.jpg"
                req2 = urllib.request.Request(play_url, headers=headers)
                with urllib.request.urlopen(req2, timeout=15) as r2, open(vpath, 'wb') as f:
                    f.write(r2.read())
                # Extract frame at 0.2s and 3s
                subprocess.run(['ffmpeg', '-y', '-ss', '00:00:00.2', '-i', vpath, '-vframes', '1', fpath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"  Downloaded: {vpath} ({os.path.getsize(vpath)} bytes)")
                with open(f"temp_tt_candidates/{name}.json", 'w', encoding='utf-8') as jf:
                    json.dump(d, jf, ensure_ascii=False, indent=2)
            else:
                print(f"  Error TikWM: {res.get('msg')}")
    except Exception as e:
        print(f"  Exception: {e}")
    time.sleep(2)
