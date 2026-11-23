import os, re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Lista de IDs perigosos (ban no ads, violacao copyright, pirataria, defunto pesado)
DANGEROUS_IDS = {100, 52, 55, 53, 59, 36, 65, 10, 27, 29, 9, 50, 82, 101, 102, 56, 94, 20, 6, 25}

# Padrao de card no recommended-grid:
# <a class="product-card-rec" ... data-id="X" ...>...</a>
# Vamos remover ou ocultar esses cards
count_removed = 0

for pid in DANGEROUS_IDS:
    # Procura por data-id="X" ou href="pages/produto-X.html"
    pattern1 = rf'<a[^>]*class="product-card-rec"[^>]*data-id="{pid}"[^>]*>.*?</a>'
    pattern2 = rf'<a[^>]*href="pages/produto-{pid}\.html"[^>]*class="product-card-rec"[^>]*>.*?</a>'
    
    # Substituir por vazio se encontrar
    matches = len(re.findall(pattern1, html, flags=re.DOTALL))
    if matches > 0:
        html = re.sub(pattern1, '', html, flags=re.DOTALL)
        count_removed += matches
    else:
        matches2 = len(re.findall(pattern2, html, flags=re.DOTALL))
        if matches2 > 0:
            html = re.sub(pattern2, '', html, flags=re.DOTALL)
            count_removed += matches2

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Cards removidos com sucesso: {count_removed}")
