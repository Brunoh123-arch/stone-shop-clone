import re

with open('pages/produto-111.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Atualizar ratings-row com (3)
html = re.sub(
    r'(<div class="ratings-row"[^>]*>.*?<span style="color:#666;font-size:12px;">)\(\d+\)(</span>)',
    r'\g<1>(3)\g<2>',
    html,
    flags=re.DOTALL
)

# 2. Atualizar reviews-header com (3)
html = re.sub(
    r'Avaliações dos clientes \(\d+\)',
    'Avaliações dos clientes (3)',
    html
)

# 3. Atualizar botao ver todas
html = re.sub(
    r'Ver todas as \d+ avaliações',
    'Ver todas as 3 avaliações',
    html
)

with open('pages/produto-111.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Produto 111 sincronizado para (3)!")
