# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
print("Tem 'creators-section'?", 'creators-section' in html)
print("Tem 'videos-criadores.js'?", 'videos-criadores.js' in html)

for line in html.split('\n'):
    if 'creator' in line.lower() or 'videos-criadores' in line.lower() or 'proteção do cliente' in line.lower():
        print("LINHA:", line.strip())
