# -*- coding: utf-8 -*-
import re

# 1. Atualizar pages/produto-28.html
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    p28 = f.read()

for i in [2, 3, 4, 5]:
    old_str = f'../videosprodutos/posters/poster-produto-28-c{i}.jpg'
    new_str = f'../videosprodutos/posters/poster-rebecca-28-c{i}.jpg?v=20261121_p28_fix'
    p28 = p28.replace(old_str, new_str)

with open('pages/produto-28.html', 'w', encoding='utf-8') as f:
    f.write(p28)
print("[+] pages/produto-28.html atualizado!")

# 2. Atualizar js/videos-criadores.js e js/videos-criadores-v3.js
for js_file in ['js/videos-criadores.js', 'js/videos-criadores-v3.js']:
    with open(js_file, 'r', encoding='utf-8') as f:
        js_txt = f.read()
    
    for i in [2, 3, 4, 5]:
        old_str = f'videosprodutos/posters/poster-produto-28-c{i}.jpg'
        new_str = f'videosprodutos/posters/poster-rebecca-28-c{i}.jpg?v=20261121_p28_fix'
        js_txt = js_txt.replace(old_str, new_str)
        
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(js_txt)
    print(f"[+] {js_file} atualizado!")

