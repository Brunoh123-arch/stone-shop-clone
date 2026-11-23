import re

print("Fazendo upgrade cirúrgico do Produto 15 (Churrasqueira Portátil Biscuitt)...")

# 1. ATUALIZAR js/videos-criadores.js
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

creators_data_15 = [
    {"name": "Churrasco no Apê", "username": "churrasconoape", "likes": 32000, "comments": 44, "shares": 510, "title": "Churrasqueira Portátil Biscuitt Steak Master: acende em 3 minutos com cooler USB! 🔥"},
    {"name": "Gourmet Prático", "username": "gourmetpratico_br", "likes": 19500, "comments": 28, "shares": 240, "title": "Zero fumaça real! O carvão fica no compartimento fechado e a gordura não pinga na brasa."},
    {"name": "Campistas Raiz", "username": "campistas.raiz", "likes": 27300, "comments": 39, "shares": 380, "title": "Levamos a churrasqueira Biscuitt pro acampamento na bag térmica. Praticidade nota 10!"},
    {"name": "Review de Cozinha", "username": "reviewdecozinha", "likes": 16400, "comments": 22, "shares": 190, "title": "Testamos na varanda: picanha e queijo coalho prontos em 15 minutos sem sujeira."},
    {"name": "Achados de Casa", "username": "achadosdecasa.br", "likes": 41000, "comments": 78, "shares": 890, "title": "A famosa churrasqueira alemã com cooler a pilha/USB na promoção da Stone Shop!"},
    {"name": "Dicas de Churrasco", "username": "dicasdechurras", "likes": 23800, "comments": 35, "shares": 310, "title": "Como controlar a intensidade do fogo com o botão do ventilador interno."},
    {"name": "Apartamento 402", "username": "apezinho.402", "likes": 18200, "comments": 31, "shares": 220, "title": "Fazendo churrasco de sexta-feira na bancada da cozinha. Vizinho nem desconfia!"},
    {"name": "Varanda & Sabor", "username": "varandaesabor", "likes": 29600, "comments": 52, "shares": 460, "title": "Economia bizarra de carvão: 200g de carvão assam carne pra 4 pessoas."},
    {"name": "Chef Rodrigo", "username": "chefrodrigo_bbq", "likes": 35400, "comments": 67, "shares": 620, "title": "Costela no bafo e ancho com crosta perfeita na Biscuitt Smoke & Fire."},
    {"name": "Vida Prática", "username": "vidapratica.oficial", "likes": 14700, "comments": 19, "shares": 160, "title": "Grelha antiaderente e cuba de inox: desmonta inteira pra lavar na pia em 2 minutos."},
    {"name": "Casal na Estrada", "username": "casalnaestrada.br", "likes": 22100, "comments": 41, "shares": 330, "title": "Nossa companheira de praia e viagens: compacta, leve e super potente."},
    {"name": "Churrasco Sem Segredo", "username": "churrascosemsegredo", "likes": 38900, "comments": 82, "shares": 740, "title": "Fogo forte com apenas um punhado de carvão e acendedor em gel."},
    {"name": "Guia Tech & Lar", "username": "guiatechlar", "likes": 17800, "comments": 26, "shares": 210, "title": "Funciona no powerbank ou com pilhas AA. Portabilidade absoluta!"},
    {"name": "Espeto & Brasa", "username": "espetoebrasa.br", "likes": 31200, "comments": 59, "shares": 480, "title": "Churrasco premium em qualquer lugar. A bag térmica facilita muito o transporte."},
    {"name": "Receitas de Domingo", "username": "receitasdomingo", "likes": 20400, "comments": 33, "shares": 270, "title": "Linguiça cuiabana e pão de alho sem queimar por fora. Temperatura uniforme."},
    {"name": "Apê Decor & Grill", "username": "apedecorgrill", "likes": 26700, "comments": 48, "shares": 390, "title": "A churrasqueira portátil mais elegante que já vi. Design moderno e seguro."},
    {"name": "Achados Incríveis", "username": "achadosincriveis.sp", "likes": 44500, "comments": 91, "shares": 950, "title": "Preço de Black Friday imperdível na Stone Shop. Vale cada centavo!"},
    {"name": "Bbq em Família", "username": "bbqemfamilia", "likes": 19900, "comments": 37, "shares": 290, "title": "Crianças por perto sem perigo: a parte externa não esquenta nada!"},
    {"name": "Dicas do Assador", "username": "dicasdoassador", "likes": 33100, "comments": 63, "shares": 530, "title": "Ponto da fraldinha selada por fora e vermelhinha por dentro na Biscuitt."},
    {"name": "Meu Primeiro Apê", "username": "meuprimeiroape.br", "likes": 15900, "comments": 24, "shares": 180, "title": "Compramos na Black Friday e já virou o xodó do nosso cantinho."},
    {"name": "Papo na Brasa", "username": "paponabrasa", "likes": 28400, "comments": 50, "shares": 410, "title": "O segredo do sistema de ventilação forçada que não deixa subir fumaça."},
    {"name": "Cozinha sem Complicação", "username": "cozinhasemcomplicacao", "likes": 18700, "comments": 29, "shares": 230, "title": "Sem sujeira de fuligem na parede ou cheiro impregnado nas cortinas."},
    {"name": "Casal Gastrô", "username": "casalgastro.br", "likes": 24800, "comments": 43, "shares": 350, "title": "Tomahawk grelhado na perfeição com o controle de ar ajustável."},
    {"name": "Piquenique & Sol", "username": "piqueniquesol", "likes": 16500, "comments": 21, "shares": 170, "title": "Fizemos churrasco no parque com autorização porque não tem brasa voando!"},
    {"name": "Review Express", "username": "reviewexpress.br", "likes": 30200, "comments": 57, "shares": 460, "title": "Unboxing completo mostrando todos os acessórios e a bag de transporte."},
    {"name": "Churrascada Boa", "username": "churrascadaboa", "likes": 36800, "comments": 74, "shares": 680, "title": "Carne suculenta com o verdadeiro sabor defumado do carvão vegetal."},
    {"name": "Cantinho do Guerreiro", "username": "cantinhodoguerreiro", "likes": 22900, "comments": 38, "shares": 320, "title": "Melhor presente de fim de ano que eu poderia me dar. Stone Shop entregou voando!"},
    {"name": "Mundo BBQ", "username": "mundobbq.oficial", "likes": 40100, "comments": 85, "shares": 810, "title": "Diferença entre churrasqueira comum e a Biscuitt: controle térmico incomparável."},
    {"name": "Vida de Apê", "username": "vidadeapezinho", "likes": 17300, "comments": 27, "shares": 200, "title": "Testada e super aprovada pelo síndico e pelos vizinhos. Zero cheiro!"},
    {"name": "Ofertas Validadas", "username": "ofertasvalidadas.br", "likes": 42700, "comments": 88, "shares": 870, "title": "Promoção Black Friday da Stone Shop tá insana. Corre antes de esgotar!"}
]

items_code_15 = []
for i, c in enumerate(creators_data_15):
    catbox_url = "https://files.catbox.moe/p7r4vc.mp4" if (i % 2 == 0) else "https://files.catbox.moe/ac2l43.mp4"
    items_code_15.append(f"""  {{
    "name": "{c['name']}",
    "username": "{c['username']}",
    "avatar": "../img/reviews-avatars/review-user-{(i % 12) + 1}.jpg",
    "poster": "../img/review-15-c{(i % 4) + 1}-1.jpg",
    "video": "{catbox_url}",
    "localVideo": "../videosprodutos/video-produto-15.mp4",
    "startTime": 0.2,
    "likes": {c['likes']},
    "comments": {c['comments']},
    "shares": {c['shares']},
    "saves": {c['likes'] // 10},
    "title": "{c['title']}"
  }}""")

new_dataset_15 = "const CREATORS_CHURRASQUEIRA_BISCUITT_15 = [\n" + ",\n".join(items_code_15) + "\n];"
pattern_15 = r'const CREATORS_CHURRASQUEIRA_BISCUITT_15\s*=\s*\[.*?\];'
js_updated_15 = re.sub(pattern_15, new_dataset_15, js_content, flags=re.DOTALL)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(js_updated_15)

print("Dataset CREATORS_CHURRASQUEIRA_BISCUITT_15 atualizado!")

# 2. ATUALIZAR pages/produto-15.html
with open('pages/produto-15.html', 'r', encoding='utf-8') as f:
    html_15 = f.read()

# Substituir Shopee URLs no slider
html_15 = re.sub(r'https://down-br\.img\.susercontent\.com/file/br-[^"]+', '../img/produto-15-1.jpg', html_15)
html_15 = re.sub(r'https://down-br\.img\.susercontent\.com/file/sg-[^"]+', '../img/produto-15-2.jpg', html_15)

# Substituir video e script
html_15 = re.sub(r"img:\s*'https://down-ws-br\.vod\.susercontent\.com/[^']*'", "img: '../img/produto-15-1.jpg'", html_15)
html_15 = re.sub(r'imagens:\s*\["https://down-ws-br\.vod\.susercontent\.com/[^"]*"\]', 'imagens: ["../videosprodutos/video-produto-15.mp4", "../img/produto-15-1.jpg", "../img/produto-15-2.jpg", "../img/produto-15-3.jpg", "../img/produto-15-4.jpg"]', html_15)

# Avaliações canônicas ouro 104
star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
stars_5 = star_svg * 5

new_reviews_15 = f'''      <!-- AVALIAÇÕES (Padrão Canônico Ouro 104) -->
      <div class="reviews-section" id="avaliacoes">
        <h3 class="reviews-header">Avaliações dos clientes (638)</h3>
        <div class="reviews-summary">
          <span class="review-avg">4.9</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          </div>
        </div>

        <!-- Avaliação 1: M**a S. -->
        <div class="review-card" data-author-name="M**a S." data-author-avatar="../img/reviews-avatars/review-user-1.jpg" data-author-stars="5" data-author-variation="Preto Fosco + Bag Térmica" data-author-date="14/10" data-author-comment="Incrível demais! Comprei meio receoso se realmente não fazia fumaça, e me surpreendi. Fiz picanha na varanda do meu apartamento e o cooler a pilha mantém a brasa viva sem jogar fumaça na cara. A Stone Shop enviou super rápido!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-1.jpg" alt="M**a S.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">M**a S.</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">14/10 · Preto Fosco + Bag Térmica</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Incrível demais! Comprei meio receoso se realmente não fazia fumaça, e me surpreendi. Fiz picanha na varanda do meu apartamento e o cooler a pilha mantém a brasa viva sem jogar fumaça na cara. A Stone Shop enviou super rápido!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-15-c1-1.jpg" alt="Unboxing Churrasqueira Biscuitt" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 2: F**o C**a -->
        <div class="review-card" data-author-name="F**o C**a" data-author-avatar="../img/reviews-avatars/review-user-2.jpg" data-author-stars="5" data-author-variation="Inox Premium + Bag Térmica" data-author-date="09/10" data-author-comment="A bag de transporte é sensacional, levei pra praia no feriado e fizemos churrasco na areia. Gasta um punhado minúsculo de carvão e a grelha antiaderente limpa na pia sem esforço. Produto nota 10!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-2.jpg" alt="F**o C**a">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">F**o C**a</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">09/10 · Inox Premium + Bag Térmica</div>
              </div>
            </div>
          </div>
          <p class="review-comment">A bag de transporte é sensacional, levei pra praia no feriado e fizemos churrasco na areia. Gasta um punhado minúsculo de carvão e a grelha antiaderente limpa na pia sem esforço. Produto nota 10!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-15-c2-1.jpg" alt="Churrasqueira Biscuitt na mesa" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 3: R**o G**s -->
        <div class="review-card" data-author-name="R**o G**s" data-author-avatar="../img/reviews-avatars/review-user-3.jpg" data-author-stars="5" data-author-variation="Preto Fosco + Bag Térmica" data-author-date="03/10" data-author-comment="Melhor churrasqueira portátil do mercado. A tecnologia alemã de ventilação fechada é impecável. Pode tocar na lateral de plástico que não queima a mão. Podem comprar sem medo!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-3.jpg" alt="R**o G**s">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">R**o G**s</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">03/10 · Preto Fosco + Bag Térmica</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Melhor churrasqueira portátil do mercado. A tecnologia alemã de ventilação fechada é impecável. Pode tocar na lateral de plástico que não queima a mão. Podem comprar sem medo!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-15-c3-1.jpg" alt="Churrasqueira Biscuitt com bag" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 4: K**s M**a -->
        <div class="review-card" data-author-name="K**s M**a" data-author-avatar="../img/reviews-avatars/review-user-4.jpg" data-author-stars="5" data-author-variation="Preto Fosco + Bag Térmica" data-author-date="27/09" data-author-comment="Chegou super rápido e muito bem embalada. Testamos com linguiça toscana e coraçãozinho, ficou igualzinho a churrascaria profissional. Muito prática!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-4.jpg" alt="K**s M**a">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">K**s M**a</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">27/09 · Preto Fosco + Bag Térmica</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou super rápido e muito bem embalada. Testamos com linguiça toscana e coraçãozinho, ficou igualzinho a churrascaria profissional. Muito prática!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-15-c4-1.jpg" alt="Churrasco pronto na Biscuitt" onclick="openPhotoModal(this.src)">
          </div>
        </div>
      </div>'''

start_idx = html_15.find('<section class="reviews-section"')
if start_idx == -1:
    start_idx = html_15.find('<div class="reviews-section"')
end_idx = html_15.find('</section>', start_idx)
if end_idx != -1:
    end_idx += len('</section>')
else:
    end_idx = html_15.find('</div>', html_15.find('class="review-card"', start_idx))

if start_idx != -1 and end_idx != -1:
    html_15 = html_15[:start_idx] + new_reviews_15 + html_15[end_idx:]
    print("Reviews do Produto 15 atualizados!")

# Purgar Shopee e Padrao
html_15 = html_15.replace('· Padrão', '· Preto Fosco + Bag Térmica')
html_15 = html_15.replace('>Padrão<', '>Preto Fosco + Bag Térmica<')
html_15 = re.sub(r'src="https://down-br\.img\.susercontent\.com/[^"]*"', 'src="../img/produto-15-1.jpg"', html_15)

with open('pages/produto-15.html', 'w', encoding='utf-8') as f:
    f.write(html_15)

print("pages/produto-15.html 100% blindado!")
