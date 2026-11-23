with open('pages/produto-115.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re
print("TOTAL LINES 115:", len(lines))
# print headers / major comments
for i, l in enumerate(lines):
    if '<!--' in l and any(k in l.upper() for k in ['SEÇÃO', 'BLOCO', 'VÍDEO', 'AVALIA', 'PROTEÇÃO', 'SOBRE', 'RELACIONADO', 'LOJA', 'STORE']):
        print(f"Line {i+1}: {l.strip()}")
