import re

with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

consts = re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*\[', text)
print(f"Total de arrays de criadores definidos: {len(consts)}")
for c in consts:
    print(" ", c)
