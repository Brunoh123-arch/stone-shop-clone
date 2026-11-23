import urllib.request
import urllib.parse
import re
import json
import os
from PIL import Image
import io

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

query = 'churrasqueira arke vitta smart 5 espetos'
# First get DDG token
vqd_url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
req = urllib.request.Request(vqd_url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        content = r.read().decode('utf-8')
    m = re.search(r'vqd=([0-9-]+)', content) or re.search(r'vqd=([a-zA-Z0-9_-]+)', content)
    if m:
        vqd = m.group(1)
        print("VQD token:", vqd)
        img_api = f"https://duckduckgo.com/i.js?l=wt-wt&o=json&q={urllib.parse.quote(query)}&vqd={vqd}&f=,,,&p=1"
        req_img = urllib.request.Request(img_api, headers=headers)
        with urllib.request.urlopen(req_img, timeout=10) as ir:
            data = json.loads(ir.read().decode('utf-8'))
        results = data.get('results', [])
        print(f"Found {len(results)} images from DDG")
        os.makedirs('temp_arke_imgs', exist_ok=True)
        saved = 0
        for r in results:
            img_url = r.get('image')
            title = r.get('title', '')
            print("Candidate:", title, img_url)
            try:
                rq = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(rq, timeout=7) as imr:
                    raw = imr.read()
                im = Image.open(io.BytesIO(raw))
                w, h = im.size
                if w >= 400 and h >= 400:
                    fn = f"temp_arke_imgs/arke_{saved}.jpg"
                    with open(fn, 'wb') as f:
                        f.write(raw)
                    print(f"  -> SAVED {fn} ({w}x{h}): {title}")
                    saved += 1
                    if saved >= 8:
                        break
            except Exception as ex:
                pass
    else:
        print("VQD not found")
except Exception as e:
    print("Error:", e)
