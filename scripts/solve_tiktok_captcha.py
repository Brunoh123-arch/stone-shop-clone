import urllib.request
import cv2
import numpy as np
import time
import json
from playwright.sync_api import sync_playwright

def get_gap_x(bg_url, slice_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    req_bg = urllib.request.Request(bg_url, headers=headers)
    req_sl = urllib.request.Request(slice_url, headers=headers)
    
    with urllib.request.urlopen(req_bg) as r:
        bg_bytes = np.frombuffer(r.read(), np.uint8)
    with urllib.request.urlopen(req_sl) as r:
        sl_bytes = np.frombuffer(r.read(), np.uint8)
        
    bg_img = cv2.imdecode(bg_bytes, cv2.IMREAD_COLOR)
    sl_img = cv2.imdecode(sl_bytes, cv2.IMREAD_UNCHANGED) # RGBA
    
    # Extract alpha channel of slice
    if sl_img.shape[2] == 4:
        alpha = sl_img[:, :, 3]
        sl_gray = cv2.cvtColor(sl_img[:, :, :3], cv2.COLOR_BGR2GRAY)
        sl_gray = cv2.bitwise_and(sl_gray, sl_gray, mask=alpha)
    else:
        sl_gray = cv2.cvtColor(sl_img, cv2.COLOR_BGR2GRAY)
        
    bg_gray = cv2.cvtColor(bg_img, cv2.COLOR_BGR2GRAY)
    
    # Canny edges
    bg_edges = cv2.Canny(bg_gray, 100, 200)
    sl_edges = cv2.Canny(sl_gray, 100, 200)
    
    res = cv2.matchTemplate(bg_edges, sl_edges, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    
    print(f"Match confidence: {max_val:.3f}, best X: {max_loc[0]}")
    return max_loc[0], bg_img.shape[1] # raw gap x, raw bg width

print("OpenCV solver function ready.")
