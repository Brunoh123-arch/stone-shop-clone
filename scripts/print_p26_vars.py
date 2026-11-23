import re
import json

with open('pages/produto-26.html', 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'variacoes\s*:\s*(\{.*?\})\s*,\s*["\']', c, re.DOTALL)
if not m:
    m = re.search(r'variacoes\s*:\s*(\{.*?\})\s*\}', c, re.DOTALL)
print(m.group(1))
