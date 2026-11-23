import sys
sys.stdout.reconfigure(encoding='utf-8')

cards = [
    {
        "id": 110,
        "cat": "Calçados",
        "nome": "tenis kappa pulse rx masculino feminino amortecimento corrida caminhada",
        "vendas": "6520",
        "vendas_txt": "6.5K",
        "img": "img/produto-110-1.jpg",
        "title": "Tênis Kappa Pulse RX Masculino e Feminino Amortecimento Corrida e Caminhada",
        "short_title": "Tênis Kappa Pulse RX",
        "desc_perc": "-73%",
        "rating": "4.9",
        "price": "69,90",
        "price_old": "259,90"
    },
    {
        "id": 111,
        "cat": "Casa",
        "nome": "projetor de arvore de natal hd usb com 6 cenas festivas 3d rotativo",
        "vendas": "5180",
        "vendas_txt": "5.1K",
        "img": "img/produto-111-1.jpg",
        "title": "Projetor de Árvore de Natal HD USB com 6 Cenas Festivas 3D Rotativo",
        "short_title": "Projetor Natalino 3D USB",
        "desc_perc": "-75%",
        "rating": "4.9",
        "price": "49,90",
        "price_old": "199,90"
    },
    {
        "id": 112,
        "cat": "Brinquedos",
        "nome": "caminhao de bombeiros 2 em 1 montanha russa de patinhos bate volta led musical",
        "vendas": "3890",
        "vendas_txt": "3.8K",
        "img": "img/produto-112-1.jpg",
        "title": "Caminhão de Bombeiros 2 em 1 Montanha-Russa de Patinhos Bate-Volta Led Musical",
        "short_title": "Caminhão Bombeiro Patinhos 2 em 1",
        "desc_perc": "-73%",
        "rating": "4.9",
        "price": "44,90",
        "price_old": "169,90"
    },
    {
        "id": 113,
        "cat": "Pet",
        "nome": "comedouro cachorro gato elevado duplo acrilico transparente anti engasgo",
        "vendas": "7340",
        "vendas_txt": "7.3K",
        "img": "img/produto-113-1.jpg",
        "title": "Comedouro Cachorro e Gato Elevado Duplo em Acrílico Transparente Anti-Engasgo",
        "short_title": "Comedouro Pet Duplo Elevado",
        "desc_perc": "-69%",
        "rating": "4.9",
        "price": "39,90",
        "price_old": "129,90"
    },
    {
        "id": 114,
        "cat": "Games",
        "nome": "controle arcade 7 em 1 stick retro multiplataforma ps4 ps3 xbox pc switch celular",
        "vendas": "2950",
        "vendas_txt": "2.9K",
        "img": "img/produto-114-1.jpg",
        "title": "Controle Arcade 7 em 1 Stick Retrô Multiplataforma PS4 PS3 Xbox PC Switch Celular",
        "short_title": "Controle Arcade 7 em 1 Stick Retrô",
        "desc_perc": "-74%",
        "rating": "4.9",
        "price": "89,90",
        "price_old": "349,90"
    }
]

cards_html = ""
for c in cards:
    cards_html += f"""              <!-- PRODUTO {c['id']} -->
              <a class="product-card-rec" href="pages/produto-{c['id']}.html" data-cat="{c['cat']}" data-nome="{c['nome']}" data-vendas="{c['vendas']}" data-id="{c['id']}" style="text-decoration: none; color: inherit;">
                <div class="card-inner-box">
                  <img src="{c['img']}" alt="{c['short_title']}" loading="lazy" class="card-thumb-img">
                  <div class="card-details-col">
                    <div class="card-top-info">
                      <h3 class="product-name">{c['title']}</h3>
                      <div class="badge-flash-tag" style="display: inline-flex !important; align-items: stretch !important; height: 18px !important; border-radius: 9px !important; overflow: hidden !important; margin: 3px 0 2px 0 !important; width: fit-content !important; box-sizing: border-box !important;">
                        <span style="background: #ff4800 !important; color: #ffffff !important; display: inline-flex !important; align-items: center !important; gap: 3px !important; padding: 0 6px 0 6px !important; font-size: 9.5px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important;">
                          <svg viewBox="0 0 24 24" width="10" height="10" fill="#ffffff" style="flex-shrink: 0 !important;"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" /></svg>
                          Oferta Relâmpago
                        </span>
                        <span style="background: #ffebe5 !important; color: #ff4800 !important; display: inline-flex !important; align-items: center !important; justify-content: center !important; padding: 0 6px !important; font-size: 9.5px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important; font-variant-numeric: tabular-nums !important;">19:46:50</span>
                      </div>
                      <div class="card-badges-row">
                        <span class="badge-frete-gratis">Frete grátis</span>
                        <span class="related-discount" style="background: #fff0f2; color: #fe2c55; border: 1px solid #ffd8e0; font-size: 9px; font-weight: 700; padding: 0.5px 3px; border-radius: 2px; line-height: 1.2;">{c['desc_perc']}</span>
                      </div>
                    </div>
                    <div class="card-rating-row"><span class="star-yellow">★</span> <span class="rating-num">{c['rating']}</span> <span class="rating-pipe">|</span> <span class="sales-count-txt">{c['vendas_txt']} vendido(s)</span></div>
                    <div class="card-bottom-action-row">
                      <div class="price-stack-col">
                        <div class="price-current-txt"><span class="currency">R$</span> {c['price']}</div>
                        <div class="price-old-txt">R$ {c['price_old']}</div>
                      </div>
                      <div class="btn-cart-circle" style="width: 32px !important; height: 32px !important; min-width: 32px !important; min-height: 32px !important; border-radius: 50% !important; background: #ffe8ee !important; display: flex !important; align-items: center !important; justify-content: center !important; cursor: pointer !important; border: none !important; flex-shrink: 0 !important;" aria-label="Adicionar ao carrinho">
                        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fe2c55" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                          <circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>
              </a>\n\n"""

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    idx_content = f.read()

anchor = 'id="recommended-grid">'
if anchor in idx_content:
    if 'pages/produto-110.html' not in idx_content:
        idx_content = idx_content.replace(anchor, anchor + "\n" + cards_html, 1)
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(idx_content)
        print("Cards 110-114 inserted in index.html successfully!")
    else:
        print("Cards 110-114 already in index.html!")
else:
    print("ERROR: could not find recommended-grid anchor")
