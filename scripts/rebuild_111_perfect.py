import os
import re
import json

with open('pages/produto-108.html', 'r', encoding='utf-8') as f:
    template = f.read()

p = {
    'id': 111,
    'title': 'Projetor LED Natalino 16 Desenhos Temáticos USB Bivolt Decoração Casa e Jardim',
    'short_title': 'Projetor LED Natalino 16 Desenhos',
    'meta_desc': 'Projetor LED Natalino com 16 Desenhos Temáticos em Alta Definição. Rotação 360°, USB Bivolt. 75% OFF no 11.11. Apenas R$ 49,90. Frete grátis.',
    'discount_badge': '-75%',
    'price_int': '49',
    'price_cents': ',90',
    'price_str': '49,90',
    'price_float': 49.90,
    'price_orig': '199,90',
    'price_orig_float': 199.90,
    'discount_amount': '150',
    'installment_text': '6x de R$ 8,32',
    'rating': '4.9',
    'reviews_count': '1.840',
    'sold_count': '5.180',
    'images': [
        '../img/produto-111-1.jpg',
        '../img/produto-111-2.jpg',
        '../img/produto-111-3.jpg',
        '../img/produto-111-4.jpg',
        '../img/produto-111-5.jpg'
    ],
    'options_thumbs': [
        '../img/produto-111-preto.jpg',
        '../img/produto-111-branco.jpg'
    ],
    'options_count_text': '2 Cores (Preto e Branco) · USB Bivolt',
    'variacoes_js': {
        'cor': {
            'com_imagem': True,
            'label': 'Cor do Projetor',
            'opcoes': [
                {'nome': 'Preto Clássico', 'preco': 49.90, 'imagem': '../img/produto-111-preto.jpg'},
                {'nome': 'Branco Neve', 'preco': 49.90, 'imagem': '../img/produto-111-branco.jpg'}
            ]
        },
        'alimentacao': {
            'label': 'Alimentação',
            'opcoes': ['USB Bivolt (Cabo Incluso)']
        }
    },
    'creators': [
        {'name': 'Gabriel Mattos', 'user': 'gabriel.mattoos', 'poster': '../videosprodutos/posters/poster-produto-111.jpg', 'avatar': '../img/creators-auto/avatar-gabriel.mattoos.jpg'},
        {'name': 'Maya | Shop Creator', 'user': 'maya.shopcreator', 'poster': '../videosprodutos/posters/poster-produto-111-criadora2.jpg', 'avatar': '../img/creators-auto/avatar-maya.shopcreator.jpg'},
        {'name': 'Rô', 'user': 'terapiaepapel', 'poster': '../videosprodutos/posters/poster-produto-111-criadora3.jpg', 'avatar': '../img/creators-auto/avatar-terapiaepapel.jpg'},
        {'name': 'Mari Gimenes', 'user': 'mariannegimenes', 'poster': '../videosprodutos/posters/poster-produto-111-criadora4.jpg', 'avatar': '../img/creators-auto/avatar-mariannegimenes.jpg'}
    ],
    'reviews': [
        {
            'user': 'Luciana Ferraz',
            'avatar': '../img/reviews-avatars/review-user-4.jpg',
            'date': 'Ontem às 19:15 · Preto Clássico / USB Bivolt',
            'comment': 'Gente, que coisa mais linda! As projeções na parede e no teto parecem filme de Natal! As crianças ficaram encantadas vendo o Papai Noel e os flocos girando. Super fácil de ligar no carregador do celular ou power bank.'
        },
        {
            'user': 'Patricia Albuquerque',
            'avatar': '../img/reviews-avatars/review-user-5.jpg',
            'date': 'Há 2 dias · Branco Neve / USB Bivolt',
            'comment': 'Chegou super rápido, bem embalado e funcionando perfeitamente. A rotação das imagens é suave e bem nítida no escuro. Coloquei na janela apontado pra sala e ficou maravilhoso!'
        },
        {
            'user': 'Renato Silveira',
            'avatar': '../img/reviews-avatars/review-user-1.jpg',
            'date': 'Há 3 dias · Preto Clássico / USB Bivolt',
            'comment': 'Produto top demais! Material resistente e o cabo USB é comprido. Testei na fachada de casa e cobriu a parede inteira com os desenhos natalinos em movimento. Valeu cada centavo.'
        },
        {
            'user': 'Camila Ramos',
            'avatar': '../img/reviews-avatars/review-user-2.jpg',
            'date': 'Há 4 dias · Branco Neve / USB Bivolt',
            'comment': 'Melhor compra que fiz pro Natal! Silencioso, não esquenta nada e os 16 desenhos em movimento são muito fofos. Meus sobrinhos amaram.'
        },
        {
            'user': 'Marcelo Nogueira',
            'avatar': '../img/reviews-avatars/review-user-3.jpg',
            'date': 'Há 5 dias · Preto Clássico / USB Bivolt',
            'comment': 'Excelente custo-benefício! Muito fácil de instalar, só apoiar e ligar. Deu um toque mágico na nossa sala de estar. Recomendo muito a loja pelo envio rápido!'
        }
    ],
    'desc_html': '''<strong>🎄✨ Projetor LED Natalino 16 Desenhos Temáticos USB Bivolt</strong><br><br>
Transforme a sua casa, sala ou fachada no verdadeiro espírito mágico do Natal! O projetor festivo ilumina tetos e paredes com 16 estampas natalinas dinâmicas em alta definição e movimento 360° contínuo.<br><br>
<strong>Destaques do Projetor:</strong><br>
• <strong>16 Desenhos Temáticos em Alta Resolução:</strong> Papai Noel no trenó, bonecos de neve, árvore natalina, renas, sinos, caixas de presentes e flocos de neve coloridos.<br>
• <strong>Mecanismo Rotativo Suave e Silencioso:</strong> Movimento fluido sem ruídos, perfeito para noites tranquilas em família.<br>
• <strong>Alimentação USB Bivolt Universal:</strong> Conecte diretamente no carregador do celular, computador, power bank ou adaptador USB.<br>
• <strong>LED de Alta Eficiência e Segurança:</strong> Baixo consumo de energia, não esquenta e pode ficar ligado a noite toda com total tranquilidade.<br>
• <strong>Base Articulada Ajustável:</strong> Ajuste o ângulo de projeção facilmente para o teto, parede, chão ou jardim.<br><br>
<strong>Especificações Técnicas:</strong><br>
• Alcance de projeção: Até 8 metros com nitidez cristalina<br>
• Padrões: 16 projeções dinâmicas coloridas (Luz RGB)<br>
• Cores disponíveis: Preto Clássico e Branco Neve<br>
• Alimentação: USB 5V Bivolt Plug & Play (Cabo Incluso)<br>
• Conteúdo da Embalagem: 1x Projetor LED Natalino, 1x Cabo USB, 1x Base de Apoio Articulada, 1x Manual de Instruções.'''
}

html = template

# 1. Title & Meta
html = re.sub(r'<title>.*?</title>', f'<title>{p["title"]} - Stone Shop</title>', html)
html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{p["meta_desc"]}">', html)

# 2. Slider Images
slider_imgs_html = ''
for idx, img_src in enumerate(p['images']):
    load_attr = 'fetchpriority="high"' if idx == 0 else 'loading="lazy"'
    slider_imgs_html += f'        <img {load_attr} decoding="async" class="slider-img" src="{img_src}" alt="{p["short_title"]} - {idx+1}" onerror="this.style.display=\'none\'">\n'

html = re.sub(r'<div class="slider-track">.*?</div>', f'<div class="slider-track">\n{slider_imgs_html}      </div>', html, flags=re.DOTALL)

# 3. Preço
html = re.sub(r'<div class="discount-badge-white">.*?</div>', f'<div class="discount-badge-white">{p["discount_badge"]}</div>', html)
html = re.sub(r'<div class="price-current">.*?</div>', f'<div class="price-current">{p["price_int"]}<span class="price-cents">{p["price_cents"]}</span></div>', html)
html = re.sub(r'<div class="price-original">.*?</div>', f'<div class="price-original">R$ {p["price_orig"]}</div>', html)

# 4. Parcelamento
html = re.sub(
    r'(<div class="installment-row".*?<span style="font-weight: 500;">).*?(</span>\s*<span style="color: #df3564; font-weight: 400; margin-left: 2px;">sem juros</span>)',
    rf'\g<1>{p["installment_text"]}\g<2>',
    html,
    flags=re.DOTALL
)

# 5. Cupom
html = re.sub(r'<span>Desconto de R\$\s*\d+</span>', f'<span>Desconto de R$ {p["discount_amount"]}</span>', html)

# 6. H1 Product Title
html = re.sub(
    r'<h1 class="product-title"[^>]*>.*?</h1>',
    f'<h1 class="product-title" style="font-size: 16px; font-weight: 700; color: #161823; line-height: 1.35; margin: 0; flex: 1;">\n          {p["title"]}\n        </h1>',
    html,
    flags=re.DOTALL
)

# 7. Ratings e Sold count
html = re.sub(r'<span style="font-size: 13px; font-weight: 700; color: #161823;">.*?</span>', f'<span style="font-size: 13px; font-weight: 700; color: #161823;">{p["rating"]}</span>', html, count=1)
html = re.sub(r'<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;".*?>\(.*?\)</span>', f'<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector(\'.reviews-section\')?.scrollIntoView({{behavior:\'smooth\'}});">({p["reviews_count"]})</span>', html)
html = re.sub(r'<div class="sold-count".*?>.*?</div>', f'<div class="sold-count" style="font-size: 13px; color: #757575; font-weight: 400;">{p["sold_count"]} vendidos</div>', html)

# 8. Opções Disponíveis
thumbs_html = ''
for t_src in p['options_thumbs']:
    thumbs_html += f'''                <div style="width:34px; height:34px; border-radius:4px; border:1px solid #e8e8e8; background:#f0f0f0; overflow:hidden; flex-shrink:0;">
                  <img loading="lazy" decoding="async" src="{t_src}" style="width:100%; height:100%; object-fit:cover; display:block;">
                </div>\n'''

linha2_replacement = f'''<!-- Linha 2: Opções Disponíveis -->
        <div class="info-row-item info-row-opcoes" onclick="handleAddToCart()">
          <div class="info-row-left" style="display:flex; align-items:center;">
            <div class="info-row-icon" style="display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-right:8px;">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#161823" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="7" height="7" rx="1.5"></rect>
                <rect x="14" y="3" width="7" height="7" rx="1.5"></rect>
                <rect x="14" y="14" width="7" height="7" rx="1.5"></rect>
                <rect x="3" y="14" width="7" height="7" rx="1.5"></rect>
              </svg>
            </div>
            <div class="info-row-opcoes-content" style="display:flex; align-items:center; gap:8px;">
              <div style="display:flex; gap:4px; align-items:center;">
{thumbs_html}              </div>
              <span class="info-row-opcoes-count" style="font-size:12px; color:#161823; font-weight:600;">{p["options_count_text"]}</span>
            </div>
          </div>
          <svg class="info-row-arrow" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </div>'''

html = re.sub(
    r'<!-- Linha 2: Opções Disponíveis -->.*?<!-- Linha 3: Proteção do Cliente -->',
    linha2_replacement + '\n\n        <!-- Linha 3: Proteção do Cliente -->',
    html,
    flags=re.DOTALL
)

# 9. CARROSSEL DE CRIADORES PRÉ-RENDERIZADO E VISÍVEL
creators_cards_html = ''
for c_idx, c in enumerate(p['creators']):
    load_attr = 'loading="eager"' if c_idx < 2 else 'loading="lazy"'
    fetch_attr = 'fetchpriority="high"' if c_idx == 0 else ''
    creators_cards_html += f'''        <div class="creator-card" data-video-id="{c_idx}">
          <img src="{c['poster']}" alt="" {load_attr} {fetch_attr} decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box;">
            <img loading="lazy" decoding="async" src="{c['avatar']}" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">{c['name']}</span>
          </div>
        </div>\n'''

creators_section_html = f'''      <!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP (PRÉ-RENDERIZADO INSTANTÂNEO) -->
      <div id="creators-section" class="creators-section">
        <h3 class="creators-title">Vídeos de criadores ({len(p['creators'])})</h3>
        <div class="creators-carousel" id="creators-carousel-list">
{creators_cards_html}        </div>
      </div>'''

html = re.sub(
    r'<!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP.*?-->.*?<!-- AVALIAÇÕES -->',
    creators_section_html + '\n\n      <!-- AVALIAÇÕES -->',
    html,
    flags=re.DOTALL
)

# 10. AVALIAÇÕES OFICIAIS LIMPAS (FALLBACK TEXT-ONLY TIKTOK SHOP OFICIAL)
reviews_block_html = f'''      <!-- AVALIAÇÕES -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes (5)</h3>
        <div class="reviews-summary">
          <span class="review-avg">{p['rating']}</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          </div>
        </div>\n'''

for r_idx, r in enumerate(p['reviews']):
    reviews_block_html += f'''        <!-- Avaliação {r_idx+1} -->
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="{r['avatar']}" alt="{r['user']}">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">{r['user']}</div>
                <div class="review-user-stars"><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg><svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg></div>
                <div class="review-date">{r['date']}</div>
              </div>
            </div>
          </div>
          <p class="review-comment">{r['comment']}</p>
        </div>\n'''

reviews_block_html += '      </div>\n'

html = re.sub(
    r'<!-- AVALIAÇÕES -->.*?<!-- DESCRIÇÃO DO PRODUTO -->',
    reviews_block_html + '\n      <!-- DESCRIÇÃO DO PRODUTO -->',
    html,
    flags=re.DOTALL
)

# 11. Descrição
html = re.sub(
    r'<div class="description-text">.*?</div>',
    f'<div class="description-text">\n          {p["desc_html"]}\n        </div>',
    html,
    flags=re.DOTALL
)

# 12. Bottom Bar
html = re.sub(
    r'<span class="btn-line2">.*? com cupom</span>',
    f'<span class="btn-line2">R$ {p["price_str"]} com cupom</span>',
    html
)

# 13. PRODUTO_ATUAL
prod_atual = {
    'id': 111,
    'nome': p['title'],
    'preco': p['price_float'],
    'preco_antigo': p['price_orig_float'],
    'img': p['images'][0],
    'imagens': p['images'],
    'variacoes': p['variacoes_js']
}
prod_atual_str = json.dumps(prod_atual, ensure_ascii=False, indent=2)

html = re.sub(
    r'const PRODUTO_ATUAL = \{.*?\};\n',
    f'const PRODUTO_ATUAL = {prod_atual_str};\n',
    html,
    flags=re.DOTALL
)

# 14. Prewarm list
html = re.sub(
    r'const list = \[.*?\];',
    'const list = [];',
    html,
    flags=re.DOTALL
)

with open('pages/produto-111.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Produto 111 reconstruído com 100% de sucesso!')
