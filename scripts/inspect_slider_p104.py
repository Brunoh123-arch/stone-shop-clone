# -*- coding: utf-8 -*-
with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:120]):
    if any(k in l.lower() for k in ['slider', 'carousel', 'img', 'foto', 'slide', 'gallery']):
        print(f"{i}: {l.strip()}")
