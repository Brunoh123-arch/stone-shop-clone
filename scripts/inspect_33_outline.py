with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

import re
print("TOTAL LINES 33:", len(lines))
for i, l in enumerate(lines):
    if '<!--' in l and any(k in l.upper() for k in ['SEÇÃO', 'BLOCO', 'VÍDEO', 'AVALIA', 'PROTEÇÃO', 'SOBRE', 'RELACIONADO', 'LOJA', 'STORE']):
        print(f"Line {i+1}: {l.strip()}")
