with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    h104 = f.read()

with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    h33 = f.read()

import re

print("--- COMPARAÇÃO DETALHADA P104 vs P33 ---")

# 1. Carrossel de imagens principais
slides_104 = len(re.findall(r'class="slide"', h104))
slides_33 = len(re.findall(r'class="slide"', h33))
print(f"Slides do Carrossel Principal: P104={slides_104} | P33={slides_33}")

# 2. Variações / SKU
options_104 = len(re.findall(r'class="sku-option|class="variation-item', h104))
options_33 = len(re.findall(r'class="sku-option|class="variation-item', h33))
print(f"Variações SKU: P104={options_104} | P33={options_33}")

# 3. Creators dataset
creators_104 = len(re.findall(r'video:\s*["\']', h104))
print(f"Vídeos inline em P104: {creators_104}")

# 4. Reviews count e média
rev_header_104 = re.findall(r'Avaliações dos clientes \((.*?)\)', h104)
rev_header_33 = re.findall(r'Avaliações dos clientes \((.*?)\)', h33)
print(f"Header de Avaliações: P104={rev_header_104} | P33={rev_header_33}")

# 5. Review cards
rev_cards_104 = len(re.findall(r'class="review-card"', h104))
rev_cards_33 = len(re.findall(r'class="review-card"', h33))
print(f"Review cards renderizados: P104={rev_cards_104} | P33={rev_cards_33}")

# 6. Detalhes
details_104 = len(re.findall(r'class="detail-row', h104))
details_33 = len(re.findall(r'class="detail-row', h33))
print(f"Linhas de Detalhes: P104={details_104} | P33={details_33}")

# 7. Descrição tamanho
desc_104 = len(re.findall(r'class="description-text', h104))
print(f"Tem description-text: P104={desc_104 > 0} | P33={len(re.findall(r'class=\"description-text', h33)) > 0}")
