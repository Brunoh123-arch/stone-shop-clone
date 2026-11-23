# -*- coding: utf-8 -*-
import re

html = open('pages/produto-82.html', 'r', encoding='utf-8').read()

# 1. Descrição
desc_matches = re.findall(r'<div[^>]*class=["\'][^"\']*(?:description|desc|about-product)[^"\']*["\'][^>]*>[\s\S]*?</div>', html)
print(f"Total desc matches: {len(desc_matches)}")
for i, m in enumerate(desc_matches[:3]):
    print(f"--- Desc Match {i} ---")
    print(m[:500])

# Procura o bloco com 'id="desc-content-text"' ou similar
m_desc = re.search(r'id=["\']desc-content-text["\'][^>]*>([\s\S]*?)</div>', html)
if m_desc:
    print("\n=== DESC-CONTENT-TEXT ===")
    print(m_desc.group(1)[:1000])
else:
    print("\n=== NOT FOUND desc-content-text ===")
    # Procura por "Sobre este item" ou "Descrição"
    idx = html.find('Sobre este item')
    if idx == -1: idx = html.find('Descrição do produto')
    if idx == -1: idx = html.find('Sobre o produto')
    if idx != -1:
        print(html[idx:idx+1000])
