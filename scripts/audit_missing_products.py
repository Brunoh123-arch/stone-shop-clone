import glob, os, re

# 1. Listar todos os arquivos produto-*.html
html_files = glob.glob('pages/produto-*.html')
html_ids = set()
for f in html_files:
    m = re.search(r'produto-(\d+)\.html', f)
    if m:
        html_ids.add(int(m.group(1)))

print(f"Total de arquivos pages/produto-*.html encontrados: {len(html_ids)}")
sorted_ids = sorted(list(html_ids))
print(f"Menor ID: {sorted_ids[0]} | Maior ID: {sorted_ids[-1]}")

# 2. Verificar buracos na sequencia
missing_in_range = []
for i in range(sorted_ids[0], sorted_ids[-1] + 1):
    if i not in html_ids:
        missing_in_range.append(i)

print(f"IDs ausentes na faixa {sorted_ids[0]} a {sorted_ids[-1]}: {missing_in_range} (Total: {len(missing_in_range)})")

# 3. Verificar produtos no catalogo.js
with open('js/catalogo.js', 'r', encoding='utf-8', errors='ignore') as f:
    cat_content = f.read()

cat_ids = set(int(x) for x in re.findall(r'id:\s*(\d+)', cat_content))
print(f"Total produtos definidos em js/catalogo.js: {len(cat_ids)}")

# Verificar se ha produtos no catalogo sem HTML
cat_without_html = [cid for cid in sorted(cat_ids) if cid not in html_ids]
print(f"Produtos no catalogo.js SEM arquivo HTML correspondente: {cat_without_html}")

# Verificar se ha HTMLs sem entrada no catalogo.js
html_without_cat = [hid for hid in sorted(html_ids) if hid not in cat_ids]
print(f"Arquivos HTML que NAO estao no catalogo.js: {html_without_cat}")

# 4. Verificar index.html
with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    idx_content = f.read()

index_links = set(int(x) for x in re.findall(r'produto-(\d+)\.html', idx_content))
print(f"Total produtos linkados no index.html: {len(index_links)}")
index_without_html = [iid for iid in sorted(index_links) if iid not in html_ids]
print(f"Links no index.html que NAO possuem HTML: {index_without_html}")
