import glob
import re
import os
from bs4 import BeautifulSoup

TOTAL_AVATARS = len([f for f in os.listdir('img/reviews-avatars/tiktok_real') if f.endswith('.jpg')])
assert TOTAL_AVATARS == 220, f"Esperava 220 avatares, encontrou {TOTAL_AVATARS}"

# 60 Nomes mascarados brasileiros autênticos do TikTok Shop (sem números, sem caracteres estranhos)
MASKED_NAMES_POOL = [
    "D**o M**s", "M**a S**a", "R**o S**a", "V**a L**a", "C**a P**o",
    "J**e F**s", "A**a N**a", "T**o A**o", "L**a M**s", "G**a R**s",
    "F**a B**a", "P**a S**s", "B**z L**a", "E**a S**a", "N**y M**a",
    "H**o C**a", "I**a S**a", "K**s M**o", "W**r P**a", "Y**a C**o",
    "S**a M**s", "V**r H**o", "L**s F**a", "D**a G**s", "M**o B**o",
    "J**o P**o", "C**s E**o", "R**a G**s", "B**a N**s", "T**s A**s",
    "A**r C**s", "F**e M**a", "L**u D**e", "G**o B**o", "R**n O**a",
    "M**s P**a", "C**o L**a", "B**a C**o", "E**e S**s", "L**z V**a",
    "R**l M**t", "S**o F**o", "T**g R**s", "K**a L**a", "J**n S**a",
    "P**o H**e", "D**e A**s", "V**a F**a", "M**e T**o", "N**a R**o",
    "G**l S**a", "L**e C**o", "F**o P**a", "A**e M**s", "C**e B**a",
    "I**r D**s", "H**a N**o", "T**a L**s", "M**l G**o", "Y**r S**a"
]

# Datas recentes oficiais do TikTok Shop (DD/MM de 2026)
DATES_POOL = [
    "15/02", "14/02", "12/02", "11/02", "10/02", "08/02", "07/02", "05/02",
    "04/02", "02/02", "01/02", "29/01", "28/01", "26/01", "25/01", "23/01",
    "21/01", "20/01", "18/01", "17/01", "15/01", "13/01", "12/01", "10/01",
    "08/01", "06/01", "05/01", "03/01", "02/01"
]

# Comentários ricos, autênticos e contextuais por nicho
NICHE_COMMENTS = {
    'audio': [
        "Som absurdo de forte e cristalino! Os graves batem no peito sem chiar mesmo no volume máximo. A entrega da Stone Shop foi surreal de rápida, chegou em 2 dias bem embalado com plástico bolha reforçado!",
        "Qualidade impecável, conectou no Bluetooth instantaneamente no celular. Acabamento emborrachado super premium e a bateria durou o fim de semana todo tocando direto. Valeu cada centavo!",
        "Excelente custo-benefício! Muito superior às caixas comuns, o peso dos graves e o equilíbrio das vozes surpreendeu todo mundo no churrasco. Recomendo de olhos fechados!",
        "Caixa muito robusta e linda, as luzes de LED são um espetáculo à parte. Entrega super pontual e produto 100% original lacrado. Stone Shop está de parabéns!",
        "Simplesmente perfeita! O alcance do Bluetooth é ótimo, não corta o som mesmo indo pra longe. Graves profundos e potência que preenche o ambiente inteiro.",
        "Comprei para usar no sítio e tocou o dia todo sem descarregar! Som limpo e encorpado, muito fácil de parear. Recomendo demais!",
        "Acabamento de primeira linha, pesada e estável. Os botões são emborrachados e tem ótima vedação. Entrega rápida e produto impecável.",
        "Impressionado com a potência desse som! Não distorce nada nos médios e agudos. Vale muito mais do que o valor pago, excelente compra."
    ],
    'cozinha': [
        "Produto espetacular! Superou todas as minhas expectativas, material muito resistente e acabamento de primeira linha. Chegou antes do prazo e muito bem protegido!",
        "Amei demais a praticidade no dia a dia. Facílimo de limpar e usar, economiza um tempo danado na cozinha. Veio tudo certinho com manual e nota fiscal, nota 10!",
        "Comprem sem medo! A qualidade do acabamento é impressionante, esquenta rápido e de forma super uniforme. Minha melhor compra desse ano na Stone Shop!",
        "Entrega relâmpago e muito bem embalada! O design é lindo e moderno, combinou perfeitamente com a minha bancada. Já testei várias vezes e funciona perfeitamente.",
        "Maravilhoso! Material de altíssima durabilidade, cumpre exatamente o que promete no anúncio. Podem comprar com certeza de que é um produto premium.",
        "Fácil de manusear e muito eficiente. O antiaderente é de altíssima qualidade, não gruda absolutamente nada. Super aprovado pela família toda!",
        "Chegou super rápido, postagem no mesmo dia da compra! Muito bem embalado na caixa original lacrada. Qualidade nota mil da Stone Shop.",
        "Economiza muito tempo no preparo das refeições. Design moderno e acabamento fosco lindo. Recomendo de olhos fechados!"
    ],
    'fitness': [
        "Equipamento muito firme e resistente! Suporta o peso perfeitamente sem balançar e é super silencioso durante o exercício. A montagem foi bem intuitiva e rápida.",
        "Excelente para manter os treinos em casa. Estrutura de aço muito robusta, display com todas as funções necessárias e design compacto que cabe fácil no quarto.",
        "Chegou super rápido aqui em casa, tudo bem embalado sem nenhum arranhão. Já estou usando diariamente e a evolução nos treinos é nítida. Super recomendo!",
        "Melhor investimento pra minha saúde! Robusto, confortável e muito prático para guardar depois do uso. Atendimento da loja nota 10!",
        "Produto de altíssima qualidade, soldas perfeitas e acabamento impecável. Silencioso demais, dá pra treinar à noite sem incomodar ninguém.",
        "Conforto impressionante no assento e pedais firmes. O ajuste de carga é preciso e o display marca certinho tempo e calorias. Vale cada real!",
        "Estrutura tubular reforçada de verdade. Veio com todas as ferramentas necessárias para montagem. Stone Shop entregou muito rápido!",
        "Perfeita para treinar todo dia! Super estável, não faz nenhum barulho e o acabamento é de academia profissional. Recomendo muito."
    ],
    'casa_eletro': [
        "Simplesmente perfeito! Transformou o ambiente da casa, material de primeira e acabamento refinadíssimo. Entrega super rápida e muito cuidadosa.",
        "Superou minhas expectativas! Muito prático, atendeu 100% as necessidades da minha família. A loja postou no mesmo dia da compra, parabéns pelo serviço!",
        "Produto robusto e de altíssima durabilidade. Instalação super simples e resultado espetacular logo no primeiro uso. Comprarei novamente na Stone Shop!",
        "Adorei a qualidade! Tudo muito bem acabado, sem rebarbas ou defeitos. Veio super bem protegido na caixa. Recomendo com certeza a todos!",
        "Sensacional! Funciona perfeitamente e o acabamento é lindo demais. Excelente custo-benefício e suporte nota mil da equipe.",
        "Potência excelente e baixo ruído. Limpeza fácil e rápida. Stone Shop cumpriu o prazo com entrega impecável!",
        "Produto muito eficiente, nota-se de cara a robustez dos componentes e materiais. Chegou lacrado com plástico bolha e manual.",
        "Praticidade total no dia a dia, economiza tempo e esforço. Já indiquei para parentes e amigos, produto sensacional!"
    ],
    'tech_celular': [
        "Aparelho sensacional! Câmeras com resolução espetacular e a tela é super fluida. A bateria dura o dia todo com folga mesmo usando bastante.",
        "Chegou lacrado de fábrica com nota fiscal e garantia. Desempenho rápido demais, não trava nada em jogos e apps pesados. Stone Shop nota 10!",
        "Melhor custo-benefício que já vi! Construção premium em alumínio e vidro, design fininho e leve. Carregamento super veloz!",
        "Muito satisfeito com a compra! O som estéreo é ótimo e a tela tem cores vivas e vibrantes. Postaram super rápido, chegou antes do previsto.",
        "Produto 100% original, tudo perfeito do carregador aos manuais. Recomendo demais a loja pela agilidade e segurança na entrega."
    ],
    'beleza_saude': [
        "Amei demais esse produto! Deixa o cabelo super macio, alinhado e brilhoso sem danificar os fios. Esquenta rápido e é muito levinho de segurar.",
        "Chegou super rápido e muito bem embalado! Acabamento lindo na cor, as cerdas são firmes e o cabo giratório ajuda demais no manuseio.",
        "Melhor modelador que já tive na vida! Meus cachos duram o dia inteiro sem precisar de laquê. Podem comprar sem medo nenhum!",
        "Praticidade incrível, seca e modela ao mesmo tempo economizando horas de salão. Produto premium com qualidade de salão profissional.",
        "Maravilhosa! Muito potente, vento quente no ponto certo e não queima o couro cabeludo. Minha mãe e irmã já querem uma igual!"
    ],
    'moda_calcados': [
        "Conforto surreal! Parece que está pisando em nuvens, super macio e anatômico. O tamanho deu certinho seguindo a tabela da loja.",
        "Material de alta qualidade, acabamento impecável sem cheiro forte de borracha. Perfeito para usar o dia todo sem cansar os pés.",
        "Muito lindo e estiloso! A cor é exatamente como na foto do anúncio. Entrega rápida e atendimento nota 10 da Stone Shop.",
        "Comprei para presentear e a pessoa amou! Super resistente, sola antiderrapante e acabamento de primeira linha. Recomendo demais!",
        "Valeu cada centavo! Já peguei chuva com ele e não escorrega nada. Extremamente confortável para caminhada e dia a dia."
    ],
    'ferramentas_auto': [
        "Ferramenta brutal de forte! Torque impressionante, aguenta o tranco de serviço pesado sem esquentar. Maleta muito bem organizada.",
        "Qualidade profissional de verdade. Bateria de longa duração e recarga rápida. Stone Shop despachou no mesmo dia, entrega relâmpago!",
        "Excelente acabamento e empunhadura ergonômica muito confortável. Já usei em vários trabalhos aqui em casa e cumpriu com louvor.",
        "Produto robusto, material resistente a impactos e componentes de precisão. Veio tudo lacrado com todos os acessórios descritos.",
        "Custo-benefício imbatível! Dá de dez a zero em marcas que cobram o dobro. Podem comprar de olhos fechados!"
    ],
    'infantil_brinquedos': [
        "Meu filho amou demais! Material super seguro, bordas arredondadas e rodas reforçadas. Montagem bem rápida e fácil.",
        "Estrutura muito firme e estável, não tomba e dá total segurança pra criança brincar. Entrega super pontual e caixa lacrada.",
        "Brinquedo de excelente qualidade, cores vivas e material atóxico resistente. Valeu demais a compra, recomendo a todas as mães!",
        "Superou as expectativas! Robusto, bonito e muito divertido. Chegou em 3 dias aqui em casa super bem protegido. Nota 10!"
    ],
    'geral': [
        "Chegou super rápido e muito bem embalado! O produto é exatamente como no anúncio, qualidade absurda e acabamento impecável. Super recomendo a Stone Shop!",
        "Melhor compra que fiz ultimamente! Funciona perfeitamente, materiais de extrema qualidade e entrega relâmpago. Nota 10 em tudo!",
        "Superou todas as minhas expectativas! Muito resistente, prático e bonito. Podem comprar sem medo, loja 100% confiável e atendimento excelente.",
        "Excelente produto! Veio tudo lacrado de fábrica, completo com todos os acessórios. Já estou usando todos os dias e recomendo demais!",
        "Qualidade surpreendente pelo preço! Entrega pontual, produto original e muito bem embalado. Com certeza comprarei mais vezes nessa loja."
    ]
}

def detect_niche(text):
    t = text.lower()
    if any(k in t for k in ['som', 'boombox', 'caixa', 'bluetooth', 'fone', 'audio', 'waaw', 'sabala', 'joog', 'jbl', 'party', 'subwoofer']):
        return 'audio'
    if any(k in t for k in ['air fryer', 'fritadeira', 'panela', 'micro-ondas', 'forno', 'pote', 'prato', 'jantar', 'copo', 'cozinha', 'panificadora', 'churrasqueira', 'sanduicheira', 'grill']):
        return 'cozinha'
    if any(k in t for k in ['bicicleta', 'esteira', 'bike', 'ergométrica', 'cardio', 'treino', 'spinning', 'fitness', 'dry fit', 'halter', 'musculação']):
        return 'fitness'
    if any(k in t for k in ['celular', 'smartphone', 'galaxy', 'iphone', 'xiaomi', 'tablet', 'notebook', 'smart tv', 'tv', 'smartwatch']):
        return 'tech_celular'
    if any(k in t for k in ['cacho', 'modelador', 'escova secadora', 'secador', 'chapinha', 'alisadora', 'perfume', 'cabelo', 'barbeador', 'depilador']):
        return 'beleza_saude'
    if any(k in t for k in ['chinelo', 'sandália', 'sandalia', 'tênis', 'tenis', 'calçado', 'sapato', 'bermuda', 'camisa', 'camiseta', 'vestido', 'calça']):
        return 'moda_calcados'
    if any(k in t for k in ['furadeira', 'parafusadeira', 'ferramenta', 'pneu', 'bateria automotiva', 'moura', 'pirelli', 'macaco hidraulico', 'jogo de chaves', 'solda']):
        return 'ferramentas_auto'
    if any(k in t for k in ['triciclo', 'carrinho de bebê', 'carrinho de bebe', 'brinquedo', 'patinete', 'boneca', 'piscina infantil']):
        return 'infantil_brinquedos'
    if any(k in t for k in ['sofa', 'sofá', 'mesa', 'chuveiro', 'lavadora', 'extratora', 'aspirador', 'purificador', 'ar condicionado', 'climatizador', 'ventilador', 'guarda-roupa', 'colchão', 'colchao']):
        return 'casa_eletro'
    return 'geral'

# Mapear avatares de criadores usados por produto em js/videos-criadores.js para evitar colisão
creators_avatars_used = {}
if os.path.exists('js/videos-criadores.js'):
    vc_content = open('js/videos-criadores.js', encoding='utf-8').read()
    # Pega qualquer tt_avatar_X.jpg usado
    all_tt_in_creators = re.findall(r'tt_avatar_(\d+)\.jpg', vc_content)
    print(f"Total de tt_avatars citados em videos-criadores.js: {len(all_tt_in_creators)}")

files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))
print(f"Iniciando população e higienização em {len(files)} páginas...")

total_cards_populated = 0
total_shopee_purged = 0

for file_path in files:
    pid = int(re.search(r'produto-(\d+)', file_path).group(1))
    with open(file_path, 'r', encoding='utf-8') as fp:
        html = fp.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Nicho do produto
    title_el = soup.find('h1') or soup.find('title')
    title_text = title_el.text.strip() if title_el else ''
    niche = detect_niche(title_text)
    comments_pool = NICHE_COMMENTS[niche]

    # Variações reais do produto
    variacoes = []
    for pill in soup.select('.var-item-pill, .var-size-btn, .option-card, .cor-btn, .tamanho-btn'):
        val = pill.get('data-val') or pill.text.strip()
        if val and val not in variacoes:
            variacoes.append(val)
    if not variacoes:
        if niche == 'audio':
            variacoes = ["Preto Bivolt", "Camuflado", "Azul Bivolt"]
        elif niche == 'cozinha':
            variacoes = ["110V Preto", "220V Preto", "Inox 110V", "Inox 220V"]
        elif niche == 'fitness':
            variacoes = ["Preto com Vermelho", "Preto Fosco"]
        elif niche == 'tech_celular':
            variacoes = ["128GB Preto", "256GB Azul", "256GB Titânio"]
        elif niche == 'moda_calcados':
            variacoes = ["38/39 Preto", "40/41 Preto", "42/43 Grafite", "36/37 Bege"]
        else:
            variacoes = ["Preto Bivolt", "Padrão Oficial", "Original Stone Shop"]

    reviews = soup.select('.review-card')
    if not reviews:
        continue

    # Passo primo 17 com offset exclusivo para cada produto
    # Garante que dentro do mesmo produto CADA REVIEW TENHA UM AVATAR DIFERENTE
    product_offset = (pid * 17) % TOTAL_AVATARS
    used_avatars_in_page = set()

    for idx, card in enumerate(reviews):
        # Seleciona avatar único do pool de 220
        av_idx = (product_offset + idx) % TOTAL_AVATARS
        # Se por acaso colidir (se a página tiver mais de 220 reviews, o que não ocorre), pula para o próximo livre
        while av_idx in used_avatars_in_page and len(used_avatars_in_page) < TOTAL_AVATARS:
            av_idx = (av_idx + 1) % TOTAL_AVATARS
        used_avatars_in_page.add(av_idx)
        
        av_num = av_idx + 1
        avatar_url = f"../img/reviews-avatars/tiktok_real/tt_avatar_{av_num}.jpg"

        # Nome mascarado brasileiro
        masked_name = MASKED_NAMES_POOL[(product_offset + idx) % len(MASKED_NAMES_POOL)]

        # Data recente TikTok
        date_str = DATES_POOL[idx % len(DATES_POOL)]

        # Variação real do produto
        var_str = variacoes[idx % len(variacoes)]

        # Estrelas (90% 5 estrelas, 10% 4 estrelas)
        is_5_stars = (idx % 7 != 0)
        stars_count = 5 if is_5_stars else 4
        stars_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>' * stars_count
        if not is_5_stars:
            stars_svg += '<svg viewBox="0 0 24 24" class="star-icon" fill="#e5e5e5" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'

        # Comentário contextual
        comm_el = card.select_one('.review-comment')
        existing_comment = comm_el.text.strip() if comm_el else ''
        
        # Filtra se é comentário com lixo de shopee, parâmetros técnicos de shopee, ou muito curto
        is_shopee_garbage = (
            any(k in existing_comment.lower() for k in ['shopee', 'vendedor', 'moedas', 'pontos', 'desempenho:', 'qualidade do produto:'])
            or len(existing_comment) < 35
            or '_' in existing_comment
        )
        if is_shopee_garbage:
            final_comment = comments_pool[idx % len(comments_pool)]
            total_shopee_purged += 1
        else:
            final_comment = existing_comment

        # Fotos de unboxing: preserva se NÃO for da shopee, NÃO for avatar, NÃO for thumbnail
        photos_div = card.select_one('.review-photos')
        valid_photos = []
        if photos_div:
            for m in photos_div.find_all(['img', 'video']):
                src = m.get('src') or ''
                if src and not any(k in src.lower() for k in ['susercontent', 'avatar', 'default-avatar', '_tn', 'review-user-']):
                    valid_photos.append(str(m))

        photos_html = ''
        if valid_photos:
            photos_html = f'\n          <div class="review-photos">\n            {" ".join(valid_photos)}\n          </div>'

        # Atualiza atributos do card
        card['data-author-name'] = masked_name
        card['data-author-avatar'] = avatar_url
        card['data-author-stars'] = str(stars_count)
        card['data-author-variation'] = var_str
        card['data-author-date'] = date_str
        card['data-author-comment'] = final_comment

        # Reconstroi o conteúdo interno do card
        inner_html = f'''
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="{avatar_url}" alt="{masked_name}">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">{masked_name}</div>
                <div class="review-user-stars">{stars_svg}</div>
                <div class="review-date">{date_str} · {var_str}</div>
              </div>
            </div>
          </div>
          <p class="review-comment">{final_comment}</p>{photos_html}
        '''
        card.clear()
        card.append(BeautifulSoup(inner_html, 'html.parser'))
        total_cards_populated += 1

    # Salva o arquivo HTML higienizado
    with open(file_path, 'w', encoding='utf-8') as fp:
        fp.write(str(soup))

print("\n=======================================================")
print(f"HIGIENIZAÇÃO E POPULAÇÃO CONCLUÍDAS COM SUCESSO!")
print(f"Total de avaliações processadas: {total_cards_populated} em {len(files)} páginas!")
print(f"Total de comentários da Shopee/lixo purgados: {total_shopee_purged}")
print("=======================================================")
