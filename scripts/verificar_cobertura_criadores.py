import re

with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

# Achar todas as menções de prodId === X ou case X:
pids_handled = set()

# Cases
cases = re.findall(r'case\s+(\d+):', text)
for c in cases:
    pids_handled.add(int(c))

# Ifs: prodId === X
ifs = re.findall(r'prodId\s*===?\s*(\d+)', text)
for i in ifs:
    pids_handled.add(int(i))

print(f"Total de Product IDs atendidos em js/videos-criadores.js: {len(pids_handled)}")
print("IDs atendidos:", sorted(list(pids_handled)))

# Comparar com o catálogo oficial
catalog_file = 'js/catalogo.js'
with open(catalog_file, 'r', encoding='utf-8') as f:
    cat_text = f.read()

items_raw = re.findall(r'\{\s*id:\s*(\d+)\s*,\s*nome:\s*[\'"]([^\'"]+)[\'"]', cat_text)
cat_pids = set([int(pid) for pid, nome in items_raw])

missing = cat_pids - pids_handled
print(f"\nProdutos do catálogo ({len(cat_pids)}) NÃO atendidos por videos-criadores.js ({len(missing)}):")
print("IDs faltantes:", sorted(list(missing)))
