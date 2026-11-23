import re

with open('pages/produto-26.html', 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'window\.PRODUTO_ATUAL\s*=\s*(\{.*?\});', c, re.DOTALL)
if not m:
    m = re.search(r'const PRODUTO_ATUAL\s*=\s*(\{.*?\});', c, re.DOTALL)
if m:
    print(m.group(0)[:1000])
else:
    print("PRODUTO_ATUAL não encontrado!")
