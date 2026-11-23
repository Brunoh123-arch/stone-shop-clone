import re

print("Upgrade cirúrgico do Produto 21 (Bola Penalty Bravo XXV)...")

# 1. ATUALIZAR js/videos-criadores.js
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

creators_data_21 = [
    {"name": "Drible & Arte", "username": "dribleeartesp", "likes": 34500, "comments": 52, "shares": 610, "title": "Testando a Penalty Bravo XXV no gramado molhado: colou no pé! ⚽🔥"},
    {"name": "Futebol Raiz", "username": "futebolraiz.oficial", "likes": 48200, "comments": 91, "shares": 1120, "title": "A melhor bola custo-benefício do Brasil para o racha do fim de semana."},
    {"name": "Canal do Goleiro", "username": "canaldogoleiro_br", "likes": 26700, "comments": 39, "shares": 340, "title": "Visão do goleiro: quique macio e peso oficial FIFA. Muito confortável nas defesas."},
    {"name": "Falta Perfeita", "username": "faltaperfeitabr", "likes": 51200, "comments": 104, "shares": 1450, "title": "Cobrando falta no ângulo com a Penalty Bravo: curva limpa e sem oscilar no ar."},
    {"name": "Pelada de Quarta", "username": "peladadequarta.sp", "likes": 22100, "comments": 33, "shares": 280, "title": "Compramos 3 bolas pra nossa turma na promoção da Stone Shop e valeu demais!"},
    {"name": "Freestyle BR", "username": "freestyle.brasil", "likes": 39400, "comments": 68, "shares": 720, "title": "Controle de bola e embaixadinha: grip excelente da textura externa."},
    {"name": "Base Forte", "username": "baseforte.futebol", "likes": 18900, "comments": 27, "shares": 190, "title": "Treino de finalização com os garotos da escolinha. Costura termo-fusionada dura muito."},
    {"name": "Futebol no Quintal", "username": "futebolnoquintal", "likes": 29800, "comments": 45, "shares": 410, "title": "Unboxing da Penalty Bravo XXV original: acabamento impecável e bico lubrificado."},
    {"name": "Craques da Várzea", "username": "craquesdavarzea_oficial", "likes": 44100, "comments": 83, "shares": 930, "title": "Bola pesada e precisa. Não é daquelas bexigas leves que voam longe na batida forte."},
    {"name": "Camisa 10", "username": "camisa10.tips", "likes": 31500, "comments": 57, "shares": 540, "title": "Dica de calibração: 8 a 10 libras pra ficar perfeita no campo sintético e grama natural."},
    {"name": "Resenha F.C.", "username": "resenhafutebolclube", "likes": 37200, "comments": 71, "shares": 680, "title": "Domingo de churrasco e futebol com bola oficial. Todo mundo elogiou."},
    {"name": "Artilheiro Nato", "username": "artilheironato.br", "likes": 28400, "comments": 49, "shares": 390, "title": "Chute de fora da área sem desvio no vento. A trajetória é muito estável."},
    {"name": "Review Esportivo", "username": "reviewesportivobr", "likes": 20300, "comments": 34, "shares": 240, "title": "Comparativo Penalty Bravo XXV vs marcas importadas: ganha de lavada no preço!"},
    {"name": "Fut & Sol", "username": "futesol.litoral", "likes": 17600, "comments": 22, "shares": 180, "title": "Jogamos na praia e não absorveu água nenhuma graças à selagem Ultra Fusion."},
    {"name": "Papo de Boleiro", "username": "papodeboleiro_oficial", "likes": 42900, "comments": 79, "shares": 860, "title": "Penalty é patrimônio nacional do futebol. Essa nova geração Bravo XXV tá um espetáculo."},
    {"name": "Craque do Apê", "username": "craquedoape", "likes": 25100, "comments": 41, "shares": 320, "title": "Comprei pro meu filho treinar e agora até eu tô jogando todo dia na quadra."},
    {"name": "Treino de Pontaria", "username": "treinodepontaria", "likes": 33800, "comments": 61, "shares": 490, "title": "Acertando o travessão a 25 metros de distância. Precisão cirúrgica dessa bola."},
    {"name": "Várzea do Bom", "username": "varzeadobom.sp", "likes": 36100, "comments": 66, "shares": 590, "title": "Resistência bruta no terrão e no asfalto: aguentou o tranco sem descascar."},
    {"name": "Futebol Arte", "username": "futebolarte.br", "likes": 21800, "comments": 36, "shares": 270, "title": "Sensação de bater na bola de chapa: curva redondinha e som macio."},
    {"name": "Escolinha de Craques", "username": "escolinhadecraques_br", "likes": 19400, "comments": 29, "shares": 210, "title": "Recomendada para todas as idades: tamanho oficial número 5 profissional."},
    {"name": "Dicas do Capitão", "username": "dicasdocapitao", "likes": 30700, "comments": 54, "shares": 440, "title": "Como saber se a bola é original Penalty: detalhes da válvula e do logo Bravo XXV."},
    {"name": "Arena Sintética", "username": "arenasintetica.sp", "likes": 27500, "comments": 46, "shares": 370, "title": "A bola oficial dos nossos campeonatos de Fut7 aqui na arena. Aprovada!"},
    {"name": "Achados Esportivos", "username": "achadosesportivos.br", "likes": 46300, "comments": 95, "shares": 1050, "title": "Preço de Black Friday na Stone Shop: R$ 49,00 com frete grátis tá surreal!"},
    {"name": "Toque de Primeira", "username": "toquedeprimeira_oficial", "likes": 23400, "comments": 38, "shares": 310, "title": "Domínio orientado no peito: a bola amortiza muito macia sem espirrar longe."},
    {"name": "Golaço F.C.", "username": "golacofc.brasil", "likes": 38100, "comments": 74, "shares": 710, "title": "Chute no ângulo com efeito. Essa bola responde perfeitamente ao toque do jogador."},
    {"name": "Pé de Ouro", "username": "pedeouro_treinos", "likes": 18200, "comments": 26, "shares": 195, "title": "Treinamento diário de cobrança de pênalti: bola não perde a calibração fácil."},
    {"name": "Resenha & Gol", "username": "resenhaegol.br", "likes": 32900, "comments": 58, "shares": 480, "title": "Chegou lacrada com nota fiscal e já inauguramos com gol de bicicleta!"},
    {"name": "Fut dos Amigos", "username": "futdosamigos.oficial", "likes": 24200, "comments": 40, "shares": 330, "title": "Custo por jogo sai centavos porque a durabilidade da câmara interna é monstra."},
    {"name": "Mundo do Futebol", "username": "mundodofutebol_sp", "likes": 41800, "comments": 82, "shares": 890, "title": "Melhor compra esportiva do ano na Black Friday da Stone Shop. Entrega voando!"},
    {"name": "Top Ofertas BR", "username": "topofertas.brasil", "likes": 49700, "comments": 112, "shares": 1380, "title": "Bola Penalty original por esse preço no TikTok Ads esgota em poucas horas!"}
]

items_code_21 = []
for i, c in enumerate(creators_data_21):
    catbox_url = "https://files.catbox.moe/p7r4vc.mp4" if (i % 2 == 0) else "https://files.catbox.moe/ac2l43.mp4"
    items_code_21.append(f"""  {{
    "name": "{c['name']}",
    "username": "{c['username']}",
    "avatar": "../img/reviews-avatars/review-user-{(i % 12) + 1}.jpg",
    "poster": "../img/review-21-c{(i % 4) + 1}-1.jpg",
    "video": "{catbox_url}",
    "localVideo": "../videosprodutos/video-produto-21.mp4",
    "startTime": 0.2,
    "likes": {c['likes']},
    "comments": {c['comments']},
    "shares": {c['shares']},
    "saves": {c['likes'] // 10},
    "title": "{c['title']}"
  }}""")

new_dataset_21 = "const CREATORS_BOLA_PENALTY_21 = [\n" + ",\n".join(items_code_21) + "\n];"
pattern_21 = r'const CREATORS_BOLA_PENALTY_21\s*=\s*\[.*?\];'
js_updated_21 = re.sub(pattern_21, new_dataset_21, js_content, flags=re.DOTALL)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(js_updated_21)

print("Dataset CREATORS_BOLA_PENALTY_21 atualizado com sucesso!")

# 2. ATUALIZAR pages/produto-21.html
with open('pages/produto-21.html', 'r', encoding='utf-8') as f:
    html_21 = f.read()

# Substituir Shopee URLs no slider
html_21 = re.sub(r'https://down-br\.img\.susercontent\.com/file/sg-[^"]+', '../img/produto-21-1.jpg', html_21)
html_21 = re.sub(r'https://down-br\.img\.susercontent\.com/file/br-[^"]+', '../img/produto-21-2.jpg', html_21)

# Substituir video e script
html_21 = re.sub(r"img:\s*'https://down-[^']*'", "img: '../img/produto-21-1.jpg'", html_21)
html_21 = re.sub(r'imagens:\s*\["https://down-[^"]*"\]', 'imagens: ["../videosprodutos/video-produto-21.mp4", "../img/produto-21-1.jpg", "../img/produto-21-2.jpg"]', html_21)

# Avaliações canônicas ouro 104
star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
stars_5 = star_svg * 5

new_reviews_21 = f'''      <!-- AVALIAÇÕES (Padrão Canônico Ouro 104) -->
      <div class="reviews-section" id="avaliacoes">
        <h3 class="reviews-header">Avaliações dos clientes (1.120)</h3>
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

        <!-- Avaliação 1: L**s F. -->
        <div class="review-card" data-author-name="L**s F." data-author-avatar="../img/reviews-avatars/review-user-1.jpg" data-author-stars="5" data-author-variation="Branco e Preto - Campo Oficial" data-author-date="11/10" data-author-comment="Bola 100% original Penalty! O peso e a maciez são espetaculares. Já estreamos no racha de ontem à noite e todo mundo elogiou a precisão nos passes. Stone Shop entregou muito rápido!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-1.jpg" alt="L**s F.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">L**s F.</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">11/10 · Branco e Preto - Campo Oficial</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Bola 100% original Penalty! O peso e a maciez são espetaculares. Já estreamos no racha de ontem à noite e todo mundo elogiou a precisão nos passes. Stone Shop entregou muito rápido!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-21-c1-1.jpg" alt="Bola Penalty Bravo XXV" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 2: G**e S. -->
        <div class="review-card" data-author-name="G**e S." data-author-avatar="../img/reviews-avatars/review-user-2.jpg" data-author-stars="5" data-author-variation="Amarelo e Preto - Campo Oficial" data-author-date="06/10" data-author-comment="A tecnologia Ultra Fusion sem costura aparente é maravilhosa. Choveu durante a pelada e a bola não encharcou nada, continuou leve e rápida. Recomendo muito!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-2.jpg" alt="G**e S.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">G**e S.</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">06/10 · Amarelo e Preto - Campo Oficial</div>
              </div>
            </div>
          </div>
          <p class="review-comment">A tecnologia Ultra Fusion sem costura aparente é maravilhosa. Choveu durante a pelada e a bola não encharcou nada, continuou leve e rápida. Recomendo muito!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-21-c2-1.jpg" alt="Bola Penalty no campo" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 3: T**o A. -->
        <div class="review-card" data-author-name="T**o A." data-author-avatar="../img/reviews-avatars/review-user-3.jpg" data-author-stars="5" data-author-variation="Branco e Preto - Campo Oficial" data-author-date="29/09" data-author-comment="Preço imbatível de Black Friday. Vem com bico lubrificado e câmara que segura a pressão perfeitamente. Nota 10!">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="../img/reviews-avatars/review-user-3.jpg" alt="T**o A.">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">T**o A.</div>
                <div class="review-user-stars">{stars_5}</div>
                <div class="review-date">29/09 · Branco e Preto - Campo Oficial</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Preço imbatível de Black Friday. Vem com bico lubrificado e câmara que segura a pressão perfeitamente. Nota 10!</p>
          <div class="review-photos">
            <img loading="lazy" decoding="async" class="review-photo" src="../img/review-21-c3-1.jpg" alt="Bola Penalty cheia" onclick="openPhotoModal(this.src)">
          </div>
        </div>
      </div>'''

start_idx = html_21.find('<section class="reviews-section"')
if start_idx == -1:
    start_idx = html_21.find('<div class="reviews-section"')
end_idx = html_21.find('</section>', start_idx)
if end_idx != -1:
    end_idx += len('</section>')

if start_idx != -1 and end_idx != -1:
    html_21 = html_21[:start_idx] + new_reviews_21 + html_21[end_idx:]
    print("Reviews do Produto 21 atualizados!")

# Purgar Shopee e Padrao
html_21 = html_21.replace('· Padrão', '· Branco e Preto - Campo Oficial')
html_21 = html_21.replace('>Padrão<', '>Branco e Preto - Campo Oficial<')
html_21 = re.sub(r'src="https://down-br\.img\.susercontent\.com/[^"]*"', 'src="../img/produto-21-1.jpg"', html_21)

with open('pages/produto-21.html', 'w', encoding='utf-8') as f:
    f.write(html_21)

print("pages/produto-21.html 100% blindado!")
