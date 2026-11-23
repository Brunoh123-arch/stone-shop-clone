import re
import os

HTML_PATH = 'pages/produto-4.html'

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Slider Images to local img paths
slider_block = """    <!-- SLIDER DE IMAGENS -->
    <div class="image-slider">
      <div class="slider-track">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/jbl-boombox3-1.jpg" alt="Caixa De Som Boombox 3 Bluetooth Preta Jbl - 1" onerror="this.src='https://http2.mlstatic.com/D_NQ_NP_2X_932616-MLA99475097854_112025-F.webp'">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/jbl-boombox3-2.jpg" alt="Caixa De Som Boombox 3 Bluetooth Preta Jbl - 2" onerror="this.src='https://http2.mlstatic.com/D_NQ_NP_2X_866750-MLU74810519490_032024-F.webp'">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/jbl-boombox3-3.jpg" alt="Caixa De Som Boombox 3 Bluetooth Preta Jbl - 3" onerror="this.src='https://http2.mlstatic.com/D_NQ_NP_2X_711382-MLU74945500283_032024-F.webp'">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/jbl-boombox3-4.jpg" alt="Caixa De Som Boombox 3 Bluetooth Preta Jbl - 4" onerror="this.src='https://http2.mlstatic.com/D_NQ_NP_2X_699104-MLU74810012176_032024-F.webp'">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/jbl-boombox3-5.jpg" alt="Caixa De Som Boombox 3 Bluetooth Preta Jbl - 5" onerror="this.src='https://http2.mlstatic.com/D_NQ_NP_2X_880946-MLU75980414337_042024-F.webp'">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/jbl-boombox3-6.jpg" alt="Caixa De Som Boombox 3 Bluetooth Preta Jbl - 6" onerror="this.src='https://http2.mlstatic.com/D_NQ_NP_2X_721498-MLA74670647272_022024-F.webp'">
        <img loading="lazy" decoding="async" class="slider-img" src="../img/jbl-boombox3-7.jpg" alt="Caixa De Som Boombox 3 Bluetooth Preta Jbl - 7" onerror="this.src='https://http2.mlstatic.com/D_NQ_NP_2X_755160-MLA74670637314_022024-F.webp'">
      </div>
      <div class="slider-counter">1 / 7</div>
    </div>
    <div class="slider-dots"></div>"""

html = re.sub(r'<!-- SLIDER DE IMAGENS -->.*?<div class="slider-dots"></div>', slider_block, html, flags=re.DOTALL)

# 2. Update PRODUTO_ATUAL in script tag
produto_atual_block = """const PRODUTO_ATUAL = {
  id: 4,
  nome: 'Caixa De Som Boombox 3 Bluetooth Preta Jbl',
  preco: 149,
  img: '../img/jbl-boombox3-1.jpg',
  imagens: [
    "../img/jbl-boombox3-1.jpg",
    "../img/jbl-boombox3-2.jpg",
    "../img/jbl-boombox3-3.jpg",
    "../img/jbl-boombox3-4.jpg",
    "../img/jbl-boombox3-5.jpg",
    "../img/jbl-boombox3-6.jpg",
    "../img/jbl-boombox3-7.jpg"
  ]
};"""

html = re.sub(r'const PRODUTO_ATUAL = \{.*?\};', produto_atual_block, html, flags=re.DOTALL)

# 3. Update Ratings row
rating_row_block = """      <!-- Avaliação -->
      <div class="ratings-row" style="display: flex; align-items: center; gap: 6px; margin-bottom: 12px;">
        <div class="star-row" style="display: flex; align-items: center; gap: 4px;">
          <svg class="star-icon" viewBox="0 0 24 24" width="13" height="13" fill="#ffb800">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
          </svg>
          <span style="font-size: 13px; font-weight: 700; color: #161823;">4.9</span>
          <span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector('.reviews-section')?.scrollIntoView({behavior:'smooth'})">(3.4k)</span>
        </div>
        <span style="color: #e5e5e5; font-size: 12px; margin: 0 1px;">|</span>
        <div class="sold-count" style="font-size: 13px; color: #757575; font-weight: 400;">12.8K vendidos</div>
      </div>"""

html = re.sub(r'<!-- Avaliação -->\s*<div class="ratings-row".*?</div>\s*</div>', rating_row_block, html, flags=re.DOTALL)

# 4. Build Reviews Section with all 15 reviews with comments & local photos
reviews_data = [
    ("danilo_moraes93", "D", "31 mar. 2024", "Grave absurdo de forte! O subwoofer central dedicado dessa Boombox 3 faz tremer a casa inteira sem distorcer nada. A bateria durou o final de semana inteiro na chácara e a entrega foi em apenas 2 dias!", 1),
    ("vanessa.rocha", "V", "31 mar. 2024", "Caixa sensacional! A qualidade do som é impressionante, médios e agudos super limpos. Já usei na piscina e molhou bastante, a proteção contra água IP67 realmente funciona 100%. Recomendo demais!", 2),
    ("eduardo.costa", "E", "28 abr. 2024", "Comprei com desconto aqui e valeu cada centavo! O peso dela já entrega a qualidade da construção. Alça de metal muito resistente com acabamento emborrachado. Bateria de 24 horas comprovada!", 3),
    ("diego_alves_sp", "D", "26 mar. 2024", "Simplesmente a melhor caixa bluetooth que já tive. O grave bate no peito de verdade. Chegou super rápido, lacrada na caixa original JBL com todos os acessórios e cabo AC.", 4),
    ("aline_pinto_rj", "A", "25 jun. 2024", "Apaixonada no som dessa JBL! Muito potente, colocamos na praia e tocou o dia todo sem descarregar. Resistiu à areia e maresia perfeitamente. Entrega rápida e produto impecável!", 5),
    ("leticia_lima", "L", "21 mar. 2024", "Espetacular! Conecta super rápido no Bluetooth 5.3 com dois celulares ao mesmo tempo. O som preenche o salão de festas com facilidade. Bateria dura uma eternidade!", 6),
    ("bianca_neves", "B", "18 mai. 2024", "Entrega relâmpago, chegou antes do prazo! Caixa robusta, acabamento impecável e os radiadores passivos laterais vibram muito bonito com os graves. Melhor compra que fiz!", 7),
    ("lucas.teixeira", "L", "16 mai. 2024", "Som cristalino mesmo no volume máximo. Fiz o teste com bateria e tocou mais de 20 horas direto. À prova d'água de verdade, tomou chuva no churrasco e nem sentiu. Nota 10!", 8),
    ("tiago.barbosa", "T", "14 mai. 2024", "Pressão sonora absurda! O sistema de 3 vias acústicas faz uma diferença brutal na nitidez das músicas. Vendedor de parabéns pela agilidade no envio!", 9),
    ("marcos_souza", "M", "13 mar. 2024", "Produto 100% original JBL, som pesado e bateria monstro. O app da JBL permite equalizar perfeitamente os graves e agudos. Vale muito a pena!", 10),
    ("bruno.silva", "B", "11 mar. 2024", "Grave profundo e potente sem igual. Levei pra represa, pegou sol e água e continuou perfeita. Não troco por nenhuma outra caixa do mercado!", 11),
    ("mari_oliveira", "M", "11 abr. 2024", "Maravilhosa demais! Ficou linda na sala e substituiu qualquer aparelho de som grande. Chegou muito bem embalada em caixa reforçada. Super recomendo!", 12),
    ("isabela.fonseca", "I", "08 mai. 2024", "A bateria parece que não acaba nunca! Usei 4 dias seguidos e ainda tinha carga de sobra. Potência e graves brutais com zero distorção!", 13),
    ("bianca.costa", "B", "05 abr. 2024", "Surpreendeu todas as expectativas. A alça de transporte metálica é super firme e o som é incomparável. Entrega super rápida pelo frete grátis!", 14),
    ("isabela_moura", "I", "03 abr. 2024", "Excelente investimento! Potência pura, graves que tremem tudo e à prova d'água real. Chegou em 3 dias certinho e já estreei no churrasco de família!", 15)
]

def make_card(name, letter, date, comment, idx):
    img_src = f"../img/review-4-c{idx}-1.jpg"
    return f"""        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar"><div class="review-avatar-placeholder">{letter}</div></div>
              <div class="review-user-info">
                <div class="review-user-name">{name}</div>
                <div class="review-user-stars">★★★★★</div>
                <div class="review-date">{date} · Preto Bivolt</div>
              </div>
            </div>
          </div>
          <p class="review-comment">{comment}</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="{img_src}" alt="Caixa De Som Boombox 3 Bluetooth Preta Jbl" onerror="this.style.display='none'" onclick="openPhotoModal(this.src)">
          </div>
        </div>"""

first_5 = [make_card(*r) for r in reviews_data[:5]]
next_10 = [make_card(*r) for r in reviews_data[5:]]

reviews_block = f"""      <!-- AVALIAÇÕES -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes (3.4k)</h3>
        <div class="reviews-summary">
          <span class="review-avg">4,9</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            <svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg><svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg><svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg><svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg><svg class="review-star" fill="currentColor" viewBox="0 0 48 48" width="16" height="16"><path d="m25.22 2.72.12.06c1 .6 1.4 1.9 1.82 2.9l4.12 9.92.1.24.26.02 10.7.86c1.1.09 2.45.06 3.33.83.66.63.97 1.5.85 2.42-.19 1.2-1.36 2.01-2.22 2.76l-8.16 6.98-.2.17.06.25 2.5 10.45c.24 1.07.7 2.35.23 3.41a2.79 2.79 0 0 1-2.04 1.56c-1.2.2-2.33-.67-3.3-1.26l-9.17-5.6-.22-.13-.22.13-9.17 5.6c-.93.57-2.01 1.4-3.17 1.28a2.78 2.78 0 0 1-2.11-1.45c-.56-1.09-.09-2.44.18-3.54L12 30.13l.06-.25-.2-.17-8.15-6.98c-.84-.72-1.95-1.5-2.2-2.63-.19-.95.12-1.88.82-2.55.88-.77 2.24-.74 3.33-.83l10.7-.86.26-.02.1-.24 4.12-9.91c.44-1.05.85-2.42 1.94-2.97a2.8 2.8 0 0 1 2.44 0Z"/></svg>
          </div>
        </div>

{chr(10).join(first_5)}

        <div id="mais-reviews-4" style="display:none">
{chr(10).join(next_10)}
        </div>
        <button class="ver-mais-btn" id="ver-mais-btn-4" onclick="verMaisReviews('mais-reviews-4','ver-mais-btn-4',10)">Ver mais avaliações (10 restantes) <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0; margin-left: auto;"><polyline points="9 18 15 12 9 6"></polyline></svg></button>
      </div>"""

html = re.sub(r'<!-- AVALIAÇÕES -->\s*<div class="reviews-section">.*?<button class="ver-mais-btn".*?</button>\s*</div>', reviews_block, html, flags=re.DOTALL)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("pages/produto-4.html atualizado com sucesso!")
