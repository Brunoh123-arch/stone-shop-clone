import re

with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, line in enumerate(lines, 1):
    if 'susercontent' in line:
        print(f"L#{idx}: {line.strip()[:150]}")
