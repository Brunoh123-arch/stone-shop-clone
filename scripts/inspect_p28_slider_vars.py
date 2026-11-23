# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    txt = f.read()

import re
print("=== SLIDER P28 ===")
track = re.search(r'<div class="slider-track"[^>]*>(.*?)</div>', txt, re.DOTALL)
if track:
    print(track.group(1).strip())

counter = re.search(r'<div class="slider-counter">([^<]+)</div>', txt)
if counter:
    print("Counter:", counter.group(1))

print("\n=== VARIAÇÕES / SKUS P28 ===")
for l in txt.split('\n'):
    if any(k in l.lower() for k in ['preto metalizado', 'rosa soft', 'var-btn', 'option', 'variation', 'cor:', 'selecione']):
        print(" ", l.strip()[:140])
