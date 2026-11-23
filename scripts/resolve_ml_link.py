import urllib.request
import re
import json
import os
from PIL import Image
import io

url = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGSlTMR9FFa0LAVLFsy5kqI6d92bRqyV7edBK0tdAHaqHIfDAjPUKYtQ9NsilXV55wurDGsm-GeReTIk0Vwiu25AlpWwnp_uKks7nvs2LRJ4kPnUB9nZoTHdY-jmDc_EaYEZNHc0BGm1WH8ZPMEJzQbHinZRYiP54z4kRpDo5OG1EuOOfgWFITw24rsxxd1DFfJN4KV7mfMGUAlRw=="

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        final_url = resp.geturl()
        print("Resolved URL:", final_url)
        html = resp.read().decode('utf-8', errors='ignore')
    
    # Check for review images on ML
    # Typically in http2.mlstatic.com/D_NQ_NP_...
    imgs = re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^\"]+\.jpg', html)
    print(f"Found {len(imgs)} ML images")
    
    # Also find customer review images
    rev_imgs = re.findall(r'https://http2\.mlstatic\.com/D_NQ_NP_[^\"]*REVIEW[^\"]*\.jpg', html)
    print(f"Found {len(rev_imgs)} review images")
    
    # Save a few
    os.makedirs('temp_ml_arke', exist_ok=True)
    for i, im_u in enumerate(list(dict.fromkeys(imgs))[:10]):
        try:
            r = urllib.request.Request(im_u, headers=headers)
            with urllib.request.urlopen(r, timeout=5) as ir:
                data = ir.read()
            im = Image.open(io.BytesIO(data))
            fn = f"temp_ml_arke/ml_img_{i}.jpg"
            with open(fn, 'wb') as f:
                f.write(data)
            print(f"Saved {fn} {im.size}")
        except Exception as e:
            pass
except Exception as e:
    print("Error:", e)
