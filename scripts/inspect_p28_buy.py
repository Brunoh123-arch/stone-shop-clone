# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    txt = f.read()

import re
matches = [l.strip() for l in txt.split('\n') if any(k in l.lower() for k in ['compre', 'adicionar', 'modal', 'bottom-bar', 'footer-buy'])]
for m in matches[:15]:
    print(m)
