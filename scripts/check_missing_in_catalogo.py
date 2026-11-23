import re, json

with open('js/catalogo.js', 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# Buscar produtos no catalogo.js
missing_ids = [6, 9, 20, 25, 36, 50, 53, 55, 56, 59, 65, 82, 89, 94, 96, 97, 100, 101, 102, 106, 107, 118, 119, 120, 121, 122, 123, 124]

print(f"Total a checar: {len(missing_ids)}")
for pid in missing_ids:
    m = re.search(r'\{\s*id:\s*' + str(pid) + r'\b(.*?)\}', c, re.DOTALL)
    if m:
        block = m.group(0)
        # extrair campos principais
        nome = re.search(r'nome:\s*["\']([^"\']+)["\']', block)
        preco = re.search(r'preco:\s*["\']?([^"\',]+)["\']?', block)
        img = re.search(r'imagem:\s*["\']([^"\']+)["\']', block)
        print(f"P#{pid:03d}: {nome.group(1)[:40] if nome else 'SEM NOME'} | R$ {preco.group(1) if preco else 'N/A'} | {img.group(1)[:40] if img else 'SEM IMG'}")
    else:
        print(f"P#{pid:03d}: NAO ENCONTRADO NO CATALOGO.JS")
