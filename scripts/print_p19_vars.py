import re

with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'variacoes\s*:\s*(\{.*?\})\s*[,;\}]', c, re.DOTALL)
if m:
    print(m.group(0))
else:
    print("Variações não encontradas")
