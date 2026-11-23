# -*- coding: utf-8 -*-
import re

html = open('pages/produto-87.html', 'r', encoding='utf-8').read()

terms = ['tabela', 'guia', 'medida', 'size', 'cintura', 'quadril']
for t in terms:
    matches = [m.start() for m in re.finditer(t, html, re.IGNORECASE)]
    print(f"Term '{t}': {len(matches)} matches")
    for idx in matches[:3]:
        snippet = html[max(0, idx-80):min(len(html), idx+120)].replace('\n', ' ')
        print(f"   [{idx}]: ...{snippet}...")
