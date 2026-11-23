import os

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
                txt = fh.read()
                if 'sobre esta loja' in txt.lower():
                    print("Found 'sobre esta loja' in:", p)
                if 'sobre a loja' in txt.lower():
                    print("Found 'sobre a loja' in:", p)
                if 'perfil do vendedor' in txt.lower():
                    print("Found 'perfil do vendedor' in:", p)
                if 'seller-profile' in txt.lower():
                    print("Found 'seller-profile' in:", p)
