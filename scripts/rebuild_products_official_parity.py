import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')

# Load the exact template of produto-108.html
with open('pages/produto-108.html', 'r', encoding='utf-8') as f:
    template_108 = f.read()

# Product specifications with full parity (CLEAN REVIEWS WITH 600x600 PHOTOS - ZERO MEME LETTERING)
PRODUCTS_DATA = {
    110: {
        "title": "Tênis Kappa Pulse RX Masculino e Feminino Amortecimento Corrida e Caminhada",
        "short_title": "Tênis Kappa Pulse RX",
        "meta_desc": "Tênis Kappa Pulse RX com 73% OFF no 11.11. Apenas R$ 69,90. Frete grátis.",
        "discount_badge": "-73%",
        "price_int": "69",
        "price_cents": ",90",
        "price_str": "69,90",
        "price_float": 69.90,
        "price_orig": "259,90",
        "price_orig_float": 259.90,
        "discount_amount": "190",
        "installment_text": "6x de R$ 11,65",
        "rating": "4.9",
        "reviews_count": "1.840",
        "sold_count": "6.520",
        "images": [
            "../img/produto-110-1.jpg",
            "../img/produto-110-2.jpg",
            "../img/produto-110-3.jpg",
            "../img/produto-110-4.jpg",
            "../img/produto-110-5.jpg"
        ],
        "options_thumbs": [
            "../img/produto-110-1.jpg",
            "../img/produto-110-2.jpg",
            "../img/produto-110-3.jpg"
        ],
        "options_count_text": "3 cores, 6 tamanhos",
        "variacoes_js": {
            "cor": {
                "com_imagem": True,
                "label": "Cor / Modelo",
                "opcoes": [
                    {"nome": "Preto com Grafite", "preco": 69.90, "imagem": "../img/produto-110-1.jpg"},
                    {"nome": "Branco com Marinho", "preco": 69.90, "imagem": "../img/produto-110-2.jpg"},
                    {"nome": "All Black (Preto Total)", "preco": 69.90, "imagem": "../img/produto-110-3.jpg"}
                ]
            },
            "tamanho": {
                "label": "Tamanho",
                "opcoes": ["38", "39", "40", "41", "42", "43"]
            }
        },
        "reviews": [
            {
                "user": "Carlos Eduardo M.",
                "avatar": "../img/reviews-avatars/review-user-1.jpg",
                "date": "Ontem às 16:42 · Preto/Grafite 41",
                "comment": "Tênis sensacional! Peguei o tamanho 41 e calçou como uma luva. O amortecimento em EVA é muito macio na corrida na esteira e não machuca nada o calcanhar. Kappa original no precinho!",
                "photos": ["../img/review-110-real-1.jpg", "../img/review-110-real-2.jpg"]
            },
            {
                "user": "Mariana Silveira",
                "avatar": "../img/reviews-avatars/review-user-2.jpg",
                "date": "Há 2 dias · Branco/Marinho 38",
                "comment": "Comprei pra caminhadas no parque e me surpreendeu demais. O tecido respira muito bem, o pé não transpira e ele é super leve. Chegou em 4 dias aqui em SP!",
                "photos": ["../img/review-110-real-3.jpg", "../img/review-110-real-4.jpg"]
            },
            {
                "user": "Rafael Gomes P.",
                "avatar": "../img/reviews-avatars/review-user-3.jpg",
                "date": "Há 3 dias · All Black 42",
                "comment": "Excelente acabamento. A costura é bem feita e a sola tem uma aderência top no piso molhado. Recomendo muito a loja pelo envio rápido.",
                "photos": ["../img/review-110-real-1.jpg", "../img/review-110-real-2.jpg"]
            }
        ],
        "desc_html": """<strong>👟🔥 Tênis Kappa Pulse RX Masculino e Feminino Original</strong><br><br>
          Desenvolvido para entregar o máximo em amortecimento, leveza e durabilidade para treinos, caminhadas, corridas e uso no dia a dia!<br><br>
          <strong>Destaques do Modelo:</strong><br>
          • <strong>Cabedal em Mesh Respirável:</strong> Tramas abertas que garantem ventilação contínua e mantêm os pés sempre secos.<br>
          • <strong>Entressola Pulse Soft EVA:</strong> Absorção de impacto superior que protege os joelhos e articulações a cada passada.<br>
          • <strong>Solado de Borracha Antiderrapante:</strong> Ranhuras tratoradas de alta aderência para segurança em piso seco ou molhado.<br>
          • <strong>Calce Anatômico e Confortável:</strong> Forro interno acolchoado e palmilha conformada anti-odor.<br><br>
          <strong>Especificações Técnicas:</strong><br>
          • Indicado para: Corrida, Caminhada, Academia e Dia a Dia<br>
          • Fechamento: Cadarço ajustável<br>
          • Peso médio: 230g (super leve)<br>
          • Produto 100% original Kappa com nota fiscal e garantia oficial."""
    },
    111: {
        "title": "Projetor de Árvore de Natal HD USB com 6 Cenas Festivas 3D Rotativo",
        "short_title": "Projetor Natalino 3D USB",
        "meta_desc": "Projetor de Árvore de Natal HD USB com 75% OFF no 11.11. Apenas R$ 49,90. Frete grátis.",
        "discount_badge": "-75%",
        "price_int": "49",
        "price_cents": ",90",
        "price_str": "49,90",
        "price_float": 49.90,
        "price_orig": "199,90",
        "price_orig_float": 199.90,
        "discount_amount": "150",
        "installment_text": "6x de R$ 8,32",
        "rating": "4.9",
        "reviews_count": "1.420",
        "sold_count": "5.180",
        "images": [
            "../img/produto-111-1.jpg",
            "../img/produto-111-2.jpg",
            "../img/produto-111-3.jpg",
            "../img/produto-111-4.jpg",
            "../img/produto-111-5.jpg"
        ],
        "options_thumbs": [
            "../img/produto-111-1.jpg"
        ],
        "options_count_text": "6 Cenas 3D · USB Bivolt",
        "variacoes_js": {
            "modelo": {
                "label": "Modelo",
                "opcoes": ["6 Cenas Natalinas 3D (Completo)"]
            },
            "alimentacao": {
                "label": "Alimentação",
                "opcoes": ["USB Bivolt (Cabo Incluso)"]
            }
        },
        "reviews": [
            {
                "user": "Luciana Ferraz",
                "avatar": "../img/reviews-avatars/review-user-4.jpg",
                "date": "Ontem às 19:15 · 6 Cenas USB",
                "comment": "Gente, que coisa mais linda! As projeções no teto parecem filme de Natal! As crianças ficaram encantadas vendo o Papai Noel e os flocos girando. Super fácil de ligar no carregador do celular.",
                "photos": ["../img/review-111-real-1.jpg", "../img/review-111-real-2.jpg"]
            },
            {
                "user": "Patricia Albuquerque",
                "avatar": "../img/reviews-avatars/review-user-5.jpg",
                "date": "Há 1 dia · 6 Cenas USB",
                "comment": "Chegou muito rápido e muito bem embalado. A qualidade da lente é ótima, tem foco perfeito mesmo em ambientes maiores. Deu um toque mágico na sala!",
                "photos": ["../img/review-111-real-3.jpg", "../img/review-111-real-4.jpg"]
            },
            {
                "user": "Camila Ramos",
                "avatar": "../img/reviews-avatars/review-user-2.jpg",
                "date": "Há 3 dias · 6 Cenas USB",
                "comment": "Comprei para a noite de Natal e testei logo que chegou. A rotação é bem suave e silenciosa, as cores são super vivas. Valeu cada centavo!",
                "photos": []
            }
        ],
        "desc_html": """<strong>🎄✨ Projetor LED Natalino 3D Rotativo com 6 Cenas em Alta Resolução</strong><br><br>
          Transforme a sua casa na magia do Natal! O projetor festivo rotativo ilumina paredes e tetos com 6 estampas exclusivas de alta definição em movimento contínuo 360°.<br><br>
          <strong>Destaques do Projetor:</strong><br>
          • <strong>6 Cenas Natalinas 3D:</strong> Papai Noel com trenó, flocos de neve, árvore de Natal, renas, sinos e caixas de presente.<br>
          • <strong>Mecanismo Rotativo Silencioso:</strong> Movimento fluido e suave sem ruídos incômodos.<br>
          • <strong>Alimentação USB Bivolt:</strong> Conecte no carregador de celular, computador, powerbank ou TV.<br>
          • <strong>Luz LED Suave e Segura:</strong> Não esquenta, economiza 90% de energia e pode ficar ligada a noite toda.<br><br>
          <strong>Especificações Técnicas:</strong><br>
          • Alcance de projeção: Até 8 metros com nitidez cristalina<br>
          • Alimentação: USB 5V Bivolt<br>
          • Acompanha: 1 Projetor 3D + Cabo USB + Manual oficial."""
    },
    112: {
        "title": "Caminhão de Bombeiros 2 em 1 Montanha-Russa de Patinhos Bate-Volta Led Musical",
        "short_title": "Caminhão Bombeiro Patinhos 2 em 1",
        "meta_desc": "Caminhão de Bombeiros 2 em 1 com Patinhos com 73% OFF no 11.11. Apenas R$ 44,90. Frete grátis.",
        "discount_badge": "-73%",
        "price_int": "44",
        "price_cents": ",90",
        "price_str": "44,90",
        "price_float": 44.90,
        "price_orig": "169,90",
        "price_orig_float": 169.90,
        "discount_amount": "125",
        "installment_text": "6x de R$ 7,48",
        "rating": "4.9",
        "reviews_count": "980",
        "sold_count": "3.890",
        "images": [
            "../img/produto-112-1.jpg",
            "../img/produto-112-2.jpg",
            "../img/produto-112-3.jpg",
            "../img/produto-112-4.jpg",
            "../img/produto-112-5.jpg"
        ],
        "options_thumbs": [
            "../img/produto-112-1.jpg"
        ],
        "options_count_text": "Caminhão + 3 Patinhos",
        "variacoes_js": {
            "modelo": {
                "label": "Modelo",
                "opcoes": ["Caminhão Bombeiro + 3 Patinhos Amarelos"]
            }
        },
        "reviews": [
            {
                "user": "Vanessa Martins",
                "avatar": "../img/reviews-avatars/review-user-6.jpg",
                "date": "Hoje às 11:30 · Caminhão + Patinhos",
                "comment": "Meu filho não larga mais! Os patinhos sobem a escadinha e descem o escorregador enquanto o caminhão anda sozinho tocando música e com as luzes piscando. Material bem resistente!",
                "photos": ["../img/review-112-real-1.jpg", "../img/review-112-real-2.jpg"]
            },
            {
                "user": "Tiago Barbosa",
                "avatar": "../img/reviews-avatars/review-user-2.jpg",
                "date": "Há 2 dias · Caminhão + Patinhos",
                "comment": "Muito divertido! O sistema bate e volta desvia dos móveis sozinho. Comprei no preço de oferta e valeu cada centavo.",
                "photos": ["../img/review-112-real-3.jpg", "../img/review-112-real-4.jpg"]
            },
            {
                "user": "Fernanda Lima",
                "avatar": "../img/reviews-avatars/review-user-1.jpg",
                "date": "Há 3 dias · Caminhão + Patinhos",
                "comment": "Brinquedo sensacional! Meu afilhado de 3 anos ficou hipnotizado. Veio tudo funcionando perfeitamente e a entrega foi super rápida.",
                "photos": []
            }
        ],
        "desc_html": """<strong>🚒🦆 Caminhão de Bombeiros 2 em 1 com Pista Escorregadora de Patinhos</strong><br><br>
          Diversão garantida para os pequenos! Um brinquedo dinâmico que combina veículo de resgate com pista montanha-russa vertical com escada rolante automática.<br><br>
          <strong>Destaques do Brinquedo:</strong><br>
          • <strong>Loop Infinito de Patinhos:</strong> Os patinhos sobem a escada sincronizada e descem a rampa velozes.<br>
          • <strong>Sistema Bate-Volta Inteligente:</strong> O caminhão anda pelo chão e desvia automaticamente de paredes e móveis.<br>
          • <strong>Efeitos de Luzes LED & Som:</strong> Luzes vibrantes que piscam no ritmo da música e divertem as crianças.<br>
          • <strong>Material Seguro e Atóxico:</strong> Plástico ABS reforçado, sem cheiro e com bordas arredondadas sem risco de cortes.<br><br>
          <strong>Conteúdo da Embalagem:</strong><br>
          • 1 Caminhão de Bombeiros Musical Bate-Volta<br>
          • 3 Patinhos com rodízios de deslizamento rápido<br>
          • 1 Conjunto de pistas montáveis de fácil encaixe."""
    },
    113: {
        "title": "Comedouro Cachorro e Gato Elevado Duplo em Acrílico Transparente Anti-Engasgo",
        "short_title": "Comedouro Pet Duplo Elevado",
        "meta_desc": "Comedouro Pet Elevado Duplo Acrílico com 69% OFF no 11.11. Apenas R$ 39,90. Frete grátis.",
        "discount_badge": "-69%",
        "price_int": "39",
        "price_cents": ",90",
        "price_str": "39,90",
        "price_float": 39.90,
        "price_orig": "129,90",
        "price_orig_float": 129.90,
        "discount_amount": "90",
        "installment_text": "6x de R$ 6,65",
        "rating": "4.9",
        "reviews_count": "1.650",
        "sold_count": "7.340",
        "images": [
            "../img/produto-113-1.jpg",
            "../img/produto-113-2.jpg",
            "../img/produto-113-3.jpg",
            "../img/produto-113-4.jpg",
            "../img/produto-113-5.jpg"
        ],
        "options_thumbs": [
            "../img/produto-113-1.jpg"
        ],
        "options_count_text": "Tigela Dupla Transparente",
        "variacoes_js": {
            "modelo": {
                "label": "Modelo",
                "opcoes": ["Tigela Dupla Acrílico Transparente"]
            }
        },
        "reviews": [
            {
                "user": "Dra. Paula Medeiros",
                "avatar": "../img/reviews-avatars/review-user-1.jpg",
                "date": "Ontem às 14:20 · Tigela Dupla Transparente",
                "comment": "Sou tutora de 2 gatos e 1 spitz. A altura e a inclinação de 15 graus são perfeitas pra postura deles. O refluxo do meu gato mais velho melhorou muito depois que troquei!",
                "photos": ["../img/review-113-real-1.jpg", "../img/review-113-real-2.jpg"]
            },
            {
                "user": "Juliana Castro",
                "avatar": "../img/reviews-avatars/review-user-3.jpg",
                "date": "Há 2 dias · Tigela Dupla Transparente",
                "comment": "Lindo demais na cozinha, parece um objeto de decoração! As tigelas saem facinho da base pra lavar e a água não vaza. Nota dez!",
                "photos": ["../img/review-113-real-3.jpg", "../img/review-113-real-4.jpg"]
            },
            {
                "user": "Marcelo Vieira",
                "avatar": "../img/reviews-avatars/review-user-2.jpg",
                "date": "Há 4 dias · Tigela Dupla Transparente",
                "comment": "Material de acrílico bem espesso e resistente. Meus cachorros comeram com muito mais conforto sem forçar o pescoço.",
                "photos": []
            }
        ],
        "desc_html": """<strong>🐾🥣 Comedouro e Bebedouro Elevado Duplo Ergonômico em Acrílico</strong><br><br>
          Proteja a saúde e a coluna do seu pet! Especialmente recomendado por veterinários, o comedouro elevado com ângulo de 15° previne engasgos, refluxos e problemas articulares.<br><br>
          <strong>Vantagens para o seu Pet:</strong><br>
          • <strong>Design Ergonômico Inclinado a 15°:</strong> Facilita a digestão e reduz a pressão no esôfago e articulações cervicais.<br>
          • <strong>Tigelas Duplas Removíveis:</strong> Uma para ração seca ou úmida e outra para água fresca sempre à disposição.<br>
          • <strong>Acrílico Premium Atóxico:</strong> Material ultra transparente, higiênico, livre de BPA e fácil de lavar.<br>
          • <strong>Base com Travamento Antiderrapante:</strong> Não tomba, não desliza no chão e evita sujeira na casa.<br><br>
          <strong>Especificações:</strong><br>
          • Capacidade: 350ml por tigela<br>
          • Dimensões: 27,5cm de comprimento x 13,5cm de largura x 9cm de altura<br>
          • Indicado para: Gatos de todas as idades e Cães de pequeno e médio porte."""
    },
    114: {
        "title": "Controle Arcade 7 em 1 Stick Retrô Multiplataforma PS4 PS3 Xbox PC Switch Celular",
        "short_title": "Controle Arcade Stick 7 em 1",
        "meta_desc": "Controle Arcade Fightstick 7 em 1 com 74% OFF no 11.11. Apenas R$ 89,90. Frete grátis.",
        "discount_badge": "-74%",
        "price_int": "89",
        "price_cents": ",90",
        "price_str": "89,90",
        "price_float": 89.90,
        "price_orig": "349,90",
        "price_orig_float": 349.90,
        "discount_amount": "260",
        "installment_text": "6x de R$ 14,98",
        "rating": "4.9",
        "reviews_count": "750",
        "sold_count": "2.950",
        "images": [
            "../img/produto-114-1.jpg",
            "../img/produto-114-2.jpg",
            "../img/produto-114-3.jpg",
            "../img/produto-114-4.jpg",
            "../img/produto-114-5.jpg"
        ],
        "options_thumbs": [
            "../img/produto-114-1.jpg"
        ],
        "options_count_text": "Arcade Stick 7 em 1",
        "variacoes_js": {
            "modelo": {
                "label": "Modelo",
                "opcoes": ["Controle Arcade 7 em 1 Multiplataforma USB"]
            }
        },
        "reviews": [
            {
                "user": "Guilherme Sampaio",
                "avatar": "../img/reviews-avatars/review-user-2.jpg",
                "date": "Ontem às 22:40 · Arcade Stick 7 em 1",
                "comment": "Sensacional! Testei no PS4 jogando Street Fighter e no PC com emulador MAME: resposta imediata dos botões sem nenhum lag! A alavanca é bem firme e precisa. Nostalgia total!",
                "photos": ["../img/review-114-real-1.jpg", "../img/review-114-real-2.jpg"]
            },
            {
                "user": "Felipe Nogueira",
                "avatar": "../img/reviews-avatars/review-user-3.jpg",
                "date": "Há 2 dias · Arcade Stick 7 em 1",
                "comment": "Qualidade absurda de construção. As ventosas embaixo seguram firme na mesa mesmo em lutas intensas. Valeu muito a compra!",
                "photos": ["../img/review-114-real-3.jpg", "../img/review-114-real-4.jpg"]
            },
            {
                "user": "Rodrigo Santos",
                "avatar": "../img/reviews-avatars/review-user-1.jpg",
                "date": "Há 3 dias · Arcade Stick 7 em 1",
                "comment": "Conectou no meu Switch e no PC na hora sem precisar de driver. Botões macios e alavanca com clique tátil gostoso igual dos fliperamas antigos.",
                "photos": []
            }
        ],
        "desc_html": """<strong>🕹️🔥 Controle Arcade Fightstick 7 em 1 Multiplataforma Profissional</strong><br><br>
          Reviva a autêntica emoção dos fliperamas dos anos 90 na sua casa! Compatível com praticamente todas as plataformas de jogos com tecnologia de resposta ultra-rápida sem delay.<br><br>
          <strong>Destaques do Controle:</strong><br>
          • <strong>Compatibilidade 7 em 1:</strong> Plug and play instantâneo em PS4, PS3, Xbox One, Nintendo Switch, PC (Windows), Android e TV Box.<br>
          • <strong>Alavanca Direcional 360° com Microswitches:</strong> Precisão cirúrgica para executar combos e sequências especiais com cliques táteis perfeitos.<br>
          • <strong>8 Botões de Ação Mecânicos:</strong> Layout clássico de arcade com sensibilidade extrema e alta durabilidade.<br>
          • <strong>Fixação Segura com Ventosas:</strong> Base estável que adere firmemente à mesa ou escrivaninha.<br><br>
          <strong>Especificações:</strong><br>
          • Comprimento do cabo: 2,5 metros blindado<br>
          • Interface: Conexão USB Universal Plug & Play."""
    }
}

# Function to build an exact clone of 108 with new product data
def generate_product_page(pid):
    p = PRODUCTS_DATA[pid]
    html = template_108

    # 1. Replace Title & Meta
    html = re.sub(r'<title>.*?</title>', f'<title>{p["title"]} - Stone Shop</title>', html)
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{p["meta_desc"]}">', html)

    # 2. Replace Slider Images (keeping the exact slider-track and class="slider-img")
    slider_imgs_html = ""
    for idx, img_src in enumerate(p["images"]):
        load_attr = 'fetchpriority="high"' if idx == 0 else 'loading="lazy"'
        slider_imgs_html += f'        <img {load_attr} decoding="async" class="slider-img" src="{img_src}" alt="{p["short_title"]} - {idx+1}" onerror="this.style.display=\'none\'">\n'
    
    html = re.sub(
        r'<div class="slider-track">.*?</div>',
        f'<div class="slider-track">\n{slider_imgs_html}      </div>',
        html,
        flags=re.DOTALL
    )

    # 3. Replace Price Section
    html = re.sub(r'<div class="discount-badge-white">.*?</div>', f'<div class="discount-badge-white">{p["discount_badge"]}</div>', html)
    html = re.sub(r'<div class="price-current">.*?</div>', f'<div class="price-current">{p["price_int"]}<span class="price-cents">{p["price_cents"]}</span></div>', html)
    html = re.sub(r'<div class="price-original">.*?</div>', f'<div class="price-original">R$ {p["price_orig"]}</div>', html)

    # 4. Replace Installment Row
    html = re.sub(
        r'(<div class="installment-row".*?<span style="font-weight: 500;">).*?(</span>\s*<span style="color: #df3564; font-weight: 400; margin-left: 2px;">sem juros</span>)',
        rf'\g<1>{p["installment_text"]}\g<2>',
        html,
        flags=re.DOTALL
    )

    # 5. Replace Discount Ticket
    html = re.sub(
        r'<span>Desconto de R\$\s*\d+</span>',
        f'<span>Desconto de R$ {p["discount_amount"]}</span>',
        html
    )

    # 6. Replace Product Title
    html = re.sub(
        r'<h1 class="product-title">.*?</h1>',
        f'<h1 class="product-title">{p["title"]}</h1>',
        html
    )

    # 7. Replace Ratings & Sold Count
    html = re.sub(
        r'<span style="font-size: 13px; font-weight: 700; color: #161823;">.*?</span>',
        f'<span style="font-size: 13px; font-weight: 700; color: #161823;">{p["rating"]}</span>',
        html,
        count=1
    )
    html = re.sub(
        r'<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;".*?>\(.*?\)</span>',
        f'<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector(\'.reviews-section\')?.scrollIntoView({{behavior:\'smooth\'}});">({p["reviews_count"]})</span>',
        html
    )
    html = re.sub(
        r'<div class="sold-count".*?>.*?</div>',
        f'<div class="sold-count" style="font-size: 13px; color: #757575; font-weight: 400;">{p["sold_count"]} vendidos</div>',
        html
    )

    # 8. Replace Linha 2: Opções Disponíveis (exact 34x34 box structure from 108)
    thumbs_html = ""
    for t_src in p["options_thumbs"]:
        thumbs_html += f"""                <div style="width:34px; height:34px; border-radius:4px; border:1px solid #e8e8e8; background:#f0f0f0; overflow:hidden; flex-shrink:0;">
                  <img loading="lazy" decoding="async" src="{t_src}" style="width:100%; height:100%; object-fit:cover; display:block;">
                </div>\n"""

    linha2_replacement = f"""<!-- Linha 2: Opções Disponíveis -->
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
        </div>"""

    html = re.sub(
        r'<!-- Linha 2: Opções Disponíveis -->.*?<!-- Linha 3: Proteção do Cliente -->',
        linha2_replacement + '\n\n        <!-- Linha 3: Proteção do Cliente -->',
        html,
        flags=re.DOTALL
    )

    # 9. Ocultar Carrossel de Criadores para evitar fatiamento fake de 1 único vídeo repetido
    creators_replacement = """<!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP -->
      <div id="creators-section" class="creators-section" style="display: none;"></div>"""

    html = re.sub(
        r'<!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP.*?-->\s*<div id="creators-section".*?</div>\s*</div>\s*<!-- AVALIAÇÕES -->',
        creators_replacement + '\n\n      <!-- AVALIAÇÕES -->',
        html,
        flags=re.DOTALL
    )

    # 10. Replace Reviews Section com FOTOS 600x600 LIMPAS DAS COMPRADORAS
    reviews_block_html = f"""      <!-- AVALIAÇÕES -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes ({len(p['reviews'])})</h3>
        <div class="reviews-summary">
          <span class="review-avg">{p['rating']}</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          </div>
        </div>\n"""

    prewarm_photos = []
    for r_idx, r in enumerate(p['reviews']):
        photos_tag = ""
        if r.get('photos') and len(r['photos']) > 0:
            for ph in r['photos']:
                photos_tag += f'\n            <img loading="lazy" decoding="async" class="review-photo" src="{ph}" alt="Foto da cliente" onclick="openPhotoModal(this.src)">'
                prewarm_photos.append(ph)

        photos_wrapper = f"""          <div class="review-photos">{photos_tag}
          </div>""" if photos_tag else ""

        reviews_block_html += f"""        <!-- Avaliação {r_idx+1} -->
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
{photos_wrapper}
        </div>\n"""

    reviews_block_html += "      </div>\n"

    html = re.sub(
        r'<!-- AVALIAÇÕES -->.*?<!-- DESCRIÇÃO DO PRODUTO -->',
        reviews_block_html + '\n      <!-- DESCRIÇÃO DO PRODUTO -->',
        html,
        flags=re.DOTALL
    )

    # 11. Replace Description
    html = re.sub(
        r'<div class="description-text">.*?</div>',
        f'<div class="description-text">\n          {p["desc_html"]}\n        </div>',
        html,
        flags=re.DOTALL
    )

    # 12. Replace Bottom Bar Price
    html = re.sub(
        r'<span class="btn-line2">.*? com cupom</span>',
        f'<span class="btn-line2">R$ {p["price_str"]} com cupom</span>',
        html
    )

    # 13. Replace PRODUTO_ATUAL object in script
    prod_atual = {
        "id": pid,
        "nome": p["title"],
        "preco": p["price_float"],
        "preco_antigo": p["price_orig_float"],
        "img": p["images"][0],
        "imagens": p["images"],
        "variacoes": p["variacoes_js"]
    }
    prod_atual_str = json.dumps(prod_atual, ensure_ascii=False, indent=2)

    html = re.sub(
        r'const PRODUTO_ATUAL = \{.*?\};\n',
        f'const PRODUTO_ATUAL = {prod_atual_str};\n',
        html,
        flags=re.DOTALL
    )

    # 14. Replace Prewarm list
    prewarm_str = json.dumps(prewarm_photos, ensure_ascii=False, indent=6)
    html = re.sub(
        r'const list = \[.*?\];',
        f'const list = {prewarm_str};',
        html,
        flags=re.DOTALL
    )

    out_path = f"pages/produto-{pid}.html"
    with open(out_path, 'w', encoding='utf-8') as out_f:
        out_f.write(html)
    print(f"Product page {out_path} created with clean 600x600 review photos! Length: {len(html)}")

# Generate all 5 products
for pid in [110, 111, 112, 113, 114]:
    generate_product_page(pid)

print("All 5 products cleanly rebuilt with clean customer review photos!")
