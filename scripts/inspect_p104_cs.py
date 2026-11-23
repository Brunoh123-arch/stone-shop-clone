# -*- coding: utf-8 -*-
with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    txt = f.read()

import re
m = re.search(r'<div[^>]*id=["\']creators-section["\'][^>]*>(.*?)</div\s*>', txt, re.DOTALL)
if m:
    print("Conteudo de #creators-section no P104 canônico:")
    print(repr(m.group(1)))
else:
    print("Nao achou tag fechada direta, buscando linha...")
    for l in txt.split('\n'):
        if 'creators-section' in l:
            print(l)
