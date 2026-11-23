# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
# Procura review-28-real-3.jpg
if 'review-28-real-3.jpg' in html:
    html = html.replace('review-28-real-3.jpg', 'review-28-unboxing-pacote.jpg?v=20261121_unbox_fix')
    with open('pages/produto-28.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("[+] pages/produto-28.html atualizado! Foto da menina duplicada removida e substituida por unboxing do pacote!")
else:
    print("[-] review-28-real-3.jpg nao encontrado!")
