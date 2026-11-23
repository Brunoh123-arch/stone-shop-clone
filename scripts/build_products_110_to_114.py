import os, sys
sys.stdout.reconfigure(encoding='utf-8')

# Definition of the 5 products
PRODUCTS = [
    {
        "id": 110,
        "title": "Tênis Kappa Pulse RX Masculino e Feminino Amortecimento Corrida e Caminhada",
        "short_title": "Tênis Kappa Pulse RX",
        "category": "Moda & Calçados",
        "price": 69.90,
        "price_str": "69,90",
        "price_cents": ",90",
        "price_int": "69",
        "price_orig": "259,90",
        "price_orig_float": 259.90,
        "discount": 73,
        "rating": "4.9",
        "reviews_count": "1.840",
        "sold_count": "6.520",
        "installment": "6x de R$ 11,65 sem juros",
        "slider_images": [
            "../img/produto-110-1.jpg",
            "../img/produto-110-2.jpg",
            "../img/produto-110-3.jpg",
            "../img/produto-110-4.jpg",
            "../img/produto-110-5.jpg"
        ],
        "variation_preview_text": "3 Cores, 6 Tamanhos (38 a 43)",
        "variacoes_js": {
            "cor": {
                "com_imagem": True,
                "label": "Cor",
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
        "creators": [
            {"name": "Lucas Corrida", "user": "lucascorridafit", "poster": "../videosprodutos/posters/poster-produto-110.jpg", "avatar": "../img/creators-auto/creator-1.jpg"},
            {"name": "Rodrigo Tênis", "user": "rodrigo.tenisreview", "poster": "../videosprodutos/posters/poster-produto-110-criadora2.jpg", "avatar": "../img/creators-auto/creator-2.jpg"},
            {"name": "Bruna Fit & Run", "user": "brunafit.corrida", "poster": "../videosprodutos/posters/poster-produto-110-criadora3.jpg", "avatar": "../img/creators-auto/creator-3.jpg"},
            {"name": "Marcos Runners", "user": "marcosrunner_sp", "poster": "../videosprodutos/posters/poster-produto-110-criadora4.jpg", "avatar": "../img/creators-auto/creator-4.jpg"},
            {"name": "Felipe Estilo", "user": "felipetenis_oficial", "poster": "../videosprodutos/posters/poster-produto-110-criadora5.jpg", "avatar": "../img/creators-auto/creator-5.jpg"}
        ],
        "reviews": [
            {
                "user": "Carlos Eduardo M.",
                "avatar": "../img/reviews-avatars/review-user-1.jpg",
                "date": "Ontem às 16:42",
                "comment": "Tênis sensacional! Peguei o tamanho 41 e calçou como uma luva. O amortecimento em EVA é muito macio na corrida na esteira e não machuca nada o calcanhar. Kappa original no precinho!",
                "photos": ["../img/review-110-1.jpg", "../img/review-110-2.jpg"]
            },
            {
                "user": "Mariana Silveira",
                "avatar": "../img/reviews-avatars/review-user-2.jpg",
                "date": "Há 2 dias",
                "comment": "Comprei pra caminhadas no parque e me surpreendeu demais. O tecido respira muito bem, o pé não transpira e ele é super leve. Chegou em 4 dias aqui em SP!",
                "photos": ["../img/review-110-3.jpg", "../img/review-110-4.jpg"]
            },
            {
                "user": "Rafael Gomes P.",
                "avatar": "../img/reviews-avatars/review-user-3.jpg",
                "date": "Há 3 dias",
                "comment": "Excelente acabamento. A costura é bem feita e a sola tem uma aderência top no piso molhado. Recomendo muito a loja pelo envio rápido.",
                "photos": ["../img/review-110-5.jpg", "../img/review-110-6.jpg"]
            }
        ],
        "description_html": """<div class="desc-content">
          <h4>Desempenho, Amortecimento e Conforto para o seu Dia a Dia</h4>
          <p>O <strong>Tênis Kappa Pulse RX</strong> é a escolha ideal para quem busca versatilidade, leveza e amortecimento de alto nível em treinos, corridas leves, caminhadas e na rotina do trabalho.</p>
          <ul class="desc-features" style="margin: 12px 0 16px 20px; line-height: 1.6; color: #444;">
            <li><strong>Cabedal Mesh Respirável:</strong> Malha tramada de alta densidade que proporciona ventilação térmica contínua, mantendo os pés secos.</li>
            <li><strong>Entressola em EVA Pulse Soft:</strong> Absorve os impactos e reduz a fadiga nas articulações a cada passada.</li>
            <li><strong>Solado Antiderrapante:</strong> Padrão de tração multidirecional que garante estabilidade em pisos secos e molhados.</li>
            <li><strong>Ajuste Anatômico:</strong> Colarinho acolchoado e palmilha conformada para calce macio sem atrito.</li>
          </ul>
          <p>Produto 100% original Kappa com nota fiscal e garantia de fábrica.</p>
        </div>"""
    },
    {
        "id": 111,
        "title": "Projetor de Árvore de Natal HD USB com 6 Cenas Festivas 3D Rotativo",
        "short_title": "Projetor Natalino 3D USB",
        "category": "Casa & Decoração",
        "price": 49.90,
        "price_str": "49,90",
        "price_cents": ",90",
        "price_int": "49",
        "price_orig": "199,90",
        "price_orig_float": 199.90,
        "discount": 75,
        "rating": "4.9",
        "reviews_count": "1.420",
        "sold_count": "5.180",
        "installment": "6x de R$ 8,32 sem juros",
        "slider_images": [
            "../img/produto-111-1.jpg",
            "../img/produto-111-2.jpg",
            "../img/produto-111-3.jpg",
            "../img/produto-111-4.jpg",
            "../img/produto-111-5.jpg"
        ],
        "variation_preview_text": "6 Cenas Natalinas 3D (Completo) · USB Bivolt",
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
        "creators": [
            {"name": "Decor & Magia", "user": "decormagianatal", "poster": "../videosprodutos/posters/poster-produto-111.jpg", "avatar": "../img/creators-aspirador/creator-1.jpg"},
            {"name": "Lar da Camila", "user": "lardacamila.home", "poster": "../videosprodutos/posters/poster-produto-111-criadora2.jpg", "avatar": "../img/creators-aspirador/creator-2.jpg"},
            {"name": "Achadinhos Natal", "user": "achadinhosdenatal", "poster": "../videosprodutos/posters/poster-produto-111-criadora3.jpg", "avatar": "../img/creators-aspirador/creator-3.jpg"},
            {"name": "Família & Casa", "user": "familiacasa_decor", "poster": "../videosprodutos/posters/poster-produto-111-criadora4.jpg", "avatar": "../img/creators-aspirador/creator-4.jpg"},
            {"name": "Cantinho Luz", "user": "cantinhoiluminado", "poster": "../videosprodutos/posters/poster-produto-111-criadora5.jpg", "avatar": "../img/creators-aspirador/creator-5.jpg"}
        ],
        "reviews": [
            {
                "user": "Luciana Ferraz",
                "avatar": "../img/reviews-avatars/review-user-4.jpg",
                "date": "Ontem às 19:15",
                "comment": "Gente, que coisa mais linda! As projeções no teto parecem filme de Natal! As crianças ficaram encantadas vendo o Papai Noel e os flocos girando. Super fácil de ligar no carregador do celular.",
                "photos": ["../img/review-111-1.jpg", "../img/review-111-2.jpg"]
            },
            {
                "user": "Patricia Albuquerque",
                "avatar": "../img/reviews-avatars/review-user-5.jpg",
                "date": "Há 1 dia",
                "comment": "Chegou muito rápido e muito bem embalado. A qualidade da lente é ótima, tem foco perfeito mesmo em ambientes maiores. Deu um toque mágico na sala!",
                "photos": ["../img/review-111-3.jpg", "../img/review-111-4.jpg"]
            }
        ],
        "description_html": """<div class="desc-content">
          <h4>A Magia Completa do Natal na Sua Casa</h4>
          <p>O <strong>Projetor Natalino 3D Rotativo</strong> transforma paredes e tetos em um espetáculo festivo iluminado com 6 cenas exclusivas de alta resolução.</p>
          <ul class="desc-features" style="margin: 12px 0 16px 20px; line-height: 1.6; color: #444;">
            <li><strong>6 Cenas Festivas 3D:</strong> Papai Noel com trenó, flocos de neve cadentes, árvore natalina, renas, sinos e presentes.</li>
            <li><strong>Rotação Suave 360°:</strong> Mecanismo silencioso com movimento dinâmico contínuo.</li>
            <li><strong>Alimentação USB Bivolt:</strong> Conecte em qualquer tomada, powerbank ou porta USB com baixo consumo LED.</li>
            <li><strong>Lente Óptica de Alta Nitidez:</strong> Projeta imagens vivas com alcance amplo e cores brilhantes.</li>
          </ul>
        </div>"""
    },
    {
        "id": 112,
        "title": "Caminhão de Bombeiros 2 em 1 Montanha-Russa de Patinhos Bate-Volta Led Musical",
        "short_title": "Caminhão Bombeiro Patinhos 2 em 1",
        "category": "Brinquedos & Kids",
        "price": 44.90,
        "price_str": "44,90",
        "price_cents": ",90",
        "price_int": "44",
        "price_orig": "169,90",
        "price_orig_float": 169.90,
        "discount": 73,
        "rating": "4.9",
        "reviews_count": "980",
        "sold_count": "3.890",
        "installment": "6x de R$ 7,48 sem juros",
        "slider_images": [
            "../img/produto-112-1.jpg",
            "../img/produto-112-2.jpg",
            "../img/produto-112-3.jpg",
            "../img/produto-112-4.jpg",
            "../img/produto-112-5.jpg"
        ],
        "variation_preview_text": "Caminhão Bombeiro + 3 Patinhos Amarelos",
        "variacoes_js": {
            "modelo": {
                "label": "Modelo",
                "opcoes": ["Caminhão Bombeiro + 3 Patinhos Amarelos"]
            }
        },
        "creators": [
            {"name": "Mamãe Brincalhona", "user": "mamae.brincalhona", "poster": "../videosprodutos/posters/poster-produto-112.jpg", "avatar": "../img/creators-avatars/creator-1.jpg"},
            {"name": "Dicas da Tia Ju", "user": "dicasdatiaju_kids", "poster": "../videosprodutos/posters/poster-produto-112-criadora2.jpg", "avatar": "../img/creators-avatars/creator-2.jpg"},
            {"name": "Mundo do Enzo", "user": "omundodoenzo", "poster": "../videosprodutos/posters/poster-produto-112-criadora3.jpg", "avatar": "../img/creators-avatars/creator-3.jpg"},
            {"name": "Brinquedos Incríveis", "user": "brinquedos_incriveis", "poster": "../videosprodutos/posters/poster-produto-112-criadora4.jpg", "avatar": "../img/creators-avatars/creator-4.jpg"},
            {"name": "Rotina de Mãe", "user": "rotinademae_oficial", "poster": "../videosprodutos/posters/poster-produto-112-criadora5.jpg", "avatar": "../img/creators-avatars/creator-5.jpg"}
        ],
        "reviews": [
            {
                "user": "Vanessa Martins",
                "avatar": "../img/reviews-avatars/review-user-6.jpg",
                "date": "Hoje às 11:30",
                "comment": "Meu filho não larga mais! Os patinhos sobem a escadinha e descem o escorregador enquanto o caminhão anda sozinho tocando música e com as luzes piscando. Material bem resistente!",
                "photos": ["../img/review-112-1.jpg", "../img/review-112-2.jpg"]
            },
            {
                "user": "Tiago Barbosa",
                "avatar": "../img/reviews-avatars/review-user-2.jpg",
                "date": "Há 2 dias",
                "comment": "Muito divertido! O sistema bate e volta desvia dos móveis sozinho. Comprei no preço de oferta e valeu cada centavo.",
                "photos": ["../img/review-112-3.jpg", "../img/review-112-4.jpg"]
            }
        ],
        "description_html": """<div class="desc-content">
          <h4>Diversão Sem Fim: Caminhão Bate-Volta + Escorregador de Patinhos</h4>
          <p>O <strong>Caminhão de Bombeiros 2 em 1</strong> combina a emoção do veículo de resgate com uma pista montanha-russa vertical onde patinhos sobem e descem em loop infinito.</p>
          <ul class="desc-features" style="margin: 12px 0 16px 20px; line-height: 1.6; color: #444;">
            <li><strong>Sensor Bate-Volta Inteligente:</strong> O caminhão anda pelo chão e muda de direção ao encontrar qualquer obstáculo.</li>
            <li><strong>Montanha-Russa de Patinhos:</strong> Pista com escada rolante sincronizada e 3 patinhos inclusos.</li>
            <li><strong>Luzes LED e Efeitos Sonoros:</strong> Luzes coloridas vibrantes e canções alegres que estimulam o desenvolvimento visual e motor.</li>
            <li><strong>Material Seguro e Atóxico:</strong> Plástico ABS resistente com bordas arredondadas e sem peças afiadas.</li>
          </ul>
        </div>"""
    },
    {
        "id": 113,
        "title": "Comedouro Cachorro e Gato Elevado Duplo em Acrílico Transparente Anti-Engasgo",
        "short_title": "Comedouro Pet Duplo Elevado",
        "category": "Pet Shop",
        "price": 39.90,
        "price_str": "39,90",
        "price_cents": ",90",
        "price_int": "39",
        "price_orig": "129,90",
        "price_orig_float": 129.90,
        "discount": 69,
        "rating": "4.9",
        "reviews_count": "1.650",
        "sold_count": "7.340",
        "installment": "6x de R$ 6,65 sem juros",
        "slider_images": [
            "../img/produto-113-1.jpg",
            "../img/produto-113-2.jpg",
            "../img/produto-113-3.jpg",
            "../img/produto-113-4.jpg",
            "../img/produto-113-5.jpg"
        ],
        "variation_preview_text": "Tigela Dupla Transparente (Água + Ração) · 15°",
        "variacoes_js": {
            "modelo": {
                "label": "Modelo",
                "opcoes": ["Tigela Dupla Transparente (Água + Ração)", "Tigela Individual Inclinada"]
            },
            "suporte": {
                "label": "Suporte",
                "opcoes": ["Acrílico Premium Ergonômico 15°"]
            }
        },
        "creators": [
            {"name": "Dra. Paula Vet", "user": "vetdicas_pet", "poster": "../videosprodutos/posters/poster-produto-113.jpg", "avatar": "../img/creators-avatars/creator-6.jpg"},
            {"name": "Gatinhos da Lu", "user": "gatinhosdalu", "poster": "../videosprodutos/posters/poster-produto-113-criadora2.jpg", "avatar": "../img/creators-avatars/creator-7.jpg"},
            {"name": "Cão Saudável", "user": "caofeliz_saudavel", "poster": "../videosprodutos/posters/poster-produto-113-criadora3.jpg", "avatar": "../img/creators-avatars/creator-8.jpg"},
            {"name": "Vida de Pet", "user": "vidadepet_oficial", "poster": "../videosprodutos/posters/poster-produto-113-criadora4.jpg", "avatar": "../img/creators-avatars/creator-9.jpg"},
            {"name": "Lar Bichinhos", "user": "larcombichinhos", "poster": "../videosprodutos/posters/poster-produto-113-criadora5.jpg", "avatar": "../img/creators-avatars/creator-10.jpg"}
        ],
        "reviews": [
            {
                "user": "Renata Vasconcelos",
                "avatar": "../img/reviews-avatars/review-user-1.jpg",
                "date": "Ontem às 20:10",
                "comment": "Meu gato vomitava direto depois de comer e desde que troquei pra esse comedouro inclinado acabou o problema! A postura dele fica perfeita. O acrílico é de muita qualidade e super higiênico.",
                "photos": ["../img/review-113-1.jpg", "../img/review-113-2.jpg"]
            },
            {
                "user": "Marcio Antunes",
                "avatar": "../img/reviews-avatars/review-user-3.jpg",
                "date": "Há 3 dias",
                "comment": "Produto impecável! A base tem borrachinhas antiderrapantes e as tigelas saem facilmente pra lavar. Minha cachorrinha adorou.",
                "photos": ["../img/review-113-3.jpg", "../img/review-113-4.jpg"]
            }
        ],
        "description_html": """<div class="desc-content">
          <h4>Saúde Postural e Conforto Digestivo para Cães e Gatos</h4>
          <p>O <strong>Comedouro Elevado Duplo</strong> foi desenhado ergonomicamente com ângulo de 15 graus recomendado por médicos veterinários para prevenir refluxos e engasgos.</p>
          <ul class="desc-features" style="margin: 12px 0 16px 20px; line-height: 1.6; color: #444;">
            <li><strong>Inclinação Científica de 15°:</strong> Reduz a pressão sobre a coluna cervical e estômago durante a alimentação.</li>
            <li><strong>Dupla Capacidade:</strong> Compartimentos separados para água fresca e ração no mesmo suporte.</li>
            <li><strong>Acrílico Cristal Premium Atóxico:</strong> Não acumula bactérias, livre de BPA e não solta resíduos.</li>
            <li><strong>Tigelas Removíveis:</strong> Fácil encaixe e desencaixe para higienização rápida em água corrente.</li>
          </ul>
        </div>"""
    },
    {
        "id": 114,
        "title": "Controle Arcade 7 em 1 Stick Retrô Multiplataforma PS4 PS3 Xbox PC Switch Celular",
        "short_title": "Controle Arcade 7 em 1 Stick Retrô",
        "category": "Eletrônicos & Games",
        "price": 89.90,
        "price_str": "89,90",
        "price_cents": ",90",
        "price_int": "89",
        "price_orig": "349,90",
        "price_orig_float": 349.90,
        "discount": 74,
        "rating": "4.9",
        "reviews_count": "870",
        "sold_count": "2.950",
        "installment": "6x de R$ 14,98 sem juros",
        "slider_images": [
            "../img/produto-114-1.jpg",
            "../img/produto-114-2.jpg",
            "../img/produto-114-3.jpg",
            "../img/produto-114-4.jpg",
            "../img/produto-114-5.jpg"
        ],
        "variation_preview_text": "Arcade Stick Retrô 7 em 1 · Cabo USB Blindado 2.5m",
        "variacoes_js": {
            "modelo": {
                "label": "Modelo",
                "opcoes": ["Arcade Stick Retrô 7 em 1 (Preto & Botões Color)"]
            },
            "conexao": {
                "label": "Conexão",
                "opcoes": ["Cabo USB Blindado 2.5m Plug & Play"]
            }
        },
        "creators": [
            {"name": "Nostalgia Gamer", "user": "nostalgiagamer_br", "poster": "../videosprodutos/posters/poster-produto-114.jpg", "avatar": "../img/creators-tech/creator-1.jpg"},
            {"name": "Fliperama em Casa", "user": "fliperamaemcasa", "poster": "../videosprodutos/posters/poster-produto-114-criadora2.jpg", "avatar": "../img/creators-tech/creator-2.jpg"},
            {"name": "Retro Station", "user": "retrostation_games", "poster": "../videosprodutos/posters/poster-produto-114-criadora3.jpg", "avatar": "../img/creators-tech/creator-3.jpg"},
            {"name": "Tech & Play", "user": "techandplay_review", "poster": "../videosprodutos/posters/poster-produto-114-criadora4.jpg", "avatar": "../img/creators-tech/creator-4.jpg"},
            {"name": "Mundo Arcade", "user": "mundoarcade_br", "poster": "../videosprodutos/posters/poster-produto-114-criadora5.jpg", "avatar": "../img/creators-tech/creator-5.jpg"}
        ],
        "reviews": [
            {
                "user": "Guilherme Sampaio",
                "avatar": "../img/reviews-avatars/review-user-2.jpg",
                "date": "Ontem às 22:40",
                "comment": "Sensacional! Testei no PS4 jogando Street Fighter e no PC com emulador MAME: resposta imediata dos botões sem nenhum lag! A alavanca é bem firme e precisa. Nostalgia total!",
                "photos": ["../img/review-114-1.jpg", "../img/review-114-2.jpg"]
            },
            {
                "user": "Felipe Nogueira",
                "avatar": "../img/reviews-avatars/review-user-3.jpg",
                "date": "Há 2 dias",
                "comment": "Qualidade absurda de construção. As ventosas embaixo seguram firme na mesa mesmo em lutas intensas. Valeu muito a compra!",
                "photos": ["../img/review-114-3.jpg", "../img/review-114-4.jpg"]
            }
        ],
        "description_html": """<div class="desc-content">
          <h4>A Autêntica Experiência dos Fliperamas Clássicos</h4>
          <p>O <strong>Controle Arcade Fightstick 7 em 1</strong> foi construído para gamers que exigem precisão cirúrgica, durabilidade extrema e compatibilidade universal.</p>
          <ul class="desc-features" style="margin: 12px 0 16px 20px; line-height: 1.6; color: #444;">
            <li><strong>Compatibilidade 7 em 1:</strong> Funciona nativamente em PS4, PS3, Xbox One, Nintendo Switch, PC (Windows), Android e TV Box.</li>
            <li><strong>Alavanca Direcional Microswitch 360°:</strong> Precisão arcade profissional com cliques táteis instantâneos para combos perfeitos.</li>
            <li><strong>8 Botões de Ação Mecânicos:</strong> Layout clássico japonês com resposta rápida e alta resistência.</li>
            <li><strong>Base com Ventosas Anti-Derrapantes:</strong> Fixação segura em qualquer superfície plana durante as partidas.</li>
          </ul>
        </div>"""
    }
]

# Read template structure from produto-109.html
with open('pages/produto-109.html', encoding='utf-8') as f:
    template_raw = f.read()

import json

for p in PRODUCTS:
    pid = p["id"]
    print(f"Building page for product {pid}...")

    # Build slider items
    slider_html = ""
    for idx, img_path in enumerate(p["slider_images"]):
        slider_html += f"""        <div class="slide">
          <img src="{img_path}" alt="{p['short_title']} - Foto {idx+1}" loading="{'eager' if idx == 0 else 'lazy'}" {'fetchpriority="high"' if idx == 0 else ''}>
        </div>\n"""

    # Build creators cards
    creators_html = ""
    for idx, c in enumerate(p["creators"]):
        creators_html += f"""        <div class="creator-card" data-video-id="{idx}">
          <img src="{c['poster']}" alt="" loading="eager" fetchpriority="high" decoding="async" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0;">
          <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, transparent 40%, rgba(0,0,0,0.75) 100%);"></div>
          <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2;">
            <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
          </div>
          <div style="position: absolute; bottom: 8px; left: 8px; right: 8px; display: flex; align-items: center; gap: 6px; z-index: 2;">
            <img src="{c['avatar']}" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
            <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">{c['name']}</span>
          </div>
        </div>\n"""

    # Build review cards
    reviews_html = ""
    prewarm_photos = []
    for r in p["reviews"]:
        photos_html = ""
        if r.get("photos"):
            for ph in r["photos"]:
                photos_html += f'<img loading="lazy" decoding="async" class="review-photo" src="{ph}" alt="Foto do comprador" onclick="openPhotoModal(this.src)">'
                prewarm_photos.append(ph)

        reviews_html += f"""        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <img loading="lazy" decoding="async" src="{r['avatar']}" alt="{r['user']}" onerror="this.src='../img/reviews-avatars/default-avatar.svg'">
              </div>
              <div class="review-user-info">
                <div class="review-user-name">{r['user']}</div>
                <div class="review-user-stars">
                  <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                </div>
              </div>
            </div>
            <div class="review-date">{r['date']}</div>
          </div>
          <p class="review-comment">{r['comment']}</p>
          {f'<div class="review-photos">{photos_html}</div>' if photos_html else ''}
        </div>\n"""

    # Build options preview thumbnails in product-info-rows
    opt_thumbs_html = ""
    for img_thumb in p["slider_images"][:3]:
        opt_thumbs_html += f'<img src="{img_thumb}" alt="Variação">'

    # Build PRODUTO_ATUAL object string
    prod_atual = {
        "id": p["id"],
        "nome": p["title"],
        "preco": p["price"],
        "preco_antigo": p["price_orig_float"],
        "img": p["slider_images"][0],
        "imagens": p["slider_images"],
        "variacoes": p["variacoes_js"]
    }
    prod_atual_json = json.dumps(prod_atual, ensure_ascii=False, indent=2)

    # Let's craft the complete HTML
    html_page = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<script src="/js/anti-clone-guard.js?v=20261020"></script>
<!-- TikTok Pixel Base Code -->
<script>
!function(w,d,t){{w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=['page','track','identify','instances','debug','on','off','once','ready','alias','group','enableCookie','disableCookie','holdConsent','revokeConsent','grantConsent'],ttq.setAndDefer=function(t,e){{t[e]=function(){{t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){{for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e}},ttq.load=function(e,n){{var r='https://analytics.tiktok.com/i18n/pixel/events.js',o=n&&n.partner;ttq._i=ttq._i||{{}},ttq._i[e]=[],ttq._i[e]._u=r,ttq._t=ttq._t||{{}},ttq._t[e]=+new Date,ttq._o=ttq._o||{{}},ttq._o[e]=n||{{}};var s=d.createElement('script');s.type='text/javascript',s.async=!0,s.src=r+'?sdkid='+e+'&lib='+t;var a=d.getElementsByTagName('script')[0];a.parentNode.insertBefore(s,a)}},ttq.load('DBD7ASBC77UF91061F1G'),ttq.page()}}(window,document,'ttq');
</script>
<script src="../js/tiktok-events.js"></script>
<!-- End TikTok Pixel Base Code -->
<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
  <title>{p['title']} - Stone Shop</title>
  <meta name="description" content="{p['title']} com {p['discount']}% OFF. Apenas R$ {p['price_str']}. Frete grátis.">
  <link rel="stylesheet" href="../css/style.css?v=1111_v22_grid4x">
  <link rel="icon" type="image/x-icon" href="../favicon.ico">
  <link rel="shortcut icon" type="image/x-icon" href="../favicon.ico">
  <link rel="preload" as="image" href="../decalque/decalque-oferta.jpg?v=1111" fetchpriority="high">
</head>
<body>
  <!-- CRITICAL TIKTOK SPINNER -->
  <div id="tt-instant-loader" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(255,255,255,0.42);backdrop-filter:blur(3.5px);-webkit-backdrop-filter:blur(3.5px);z-index:99999999;display:flex;align-items:center;justify-content:center;transition:opacity 0.12s ease,visibility 0.12s ease;pointer-events:none;">
    <div style="position:relative;width:44px;height:20px;">
      <div style="position:absolute;width:20px;height:20px;border-radius:50%;background:#25F4EE;left:0;animation:ttBallCyan 0.85s cubic-bezier(0.45,0.05,0.55,0.95) infinite;"></div>
      <div style="position:absolute;width:20px;height:20px;border-radius:50%;background:#FE2C55;right:0;animation:ttBallPink 0.85s cubic-bezier(0.45,0.05,0.55,0.95) infinite;"></div>
    </div>
  </div>
  <style>
    @keyframes ttBallCyan{{0%{{transform:translateX(0) scale(1);z-index:2}}50%{{transform:translateX(24px) scale(1.12);z-index:2}}50.01%{{z-index:1}}100%{{transform:translateX(0) scale(0.88);z-index:1}}}}
    @keyframes ttBallPink{{0%{{transform:translateX(0) scale(0.88);z-index:1}}50%{{transform:translateX(-24px) scale(0.88);z-index:1}}50.01%{{z-index:2}}100%{{transform:translateX(0) scale(1.12);z-index:2}}}}
  </style>
  <script>
    (function(){{
      var el = document.getElementById('tt-instant-loader');
      if(!el) return;
      var dismissed = false;
      function dismiss(){{
        if(dismissed) return;
        dismissed = true;
        el.style.opacity = '0';
        el.style.visibility = 'hidden';
        setTimeout(function(){{ if(el && el.parentNode) el.parentNode.removeChild(el); }}, 150);
      }}
      function checkAndDismiss(){{
        var imgs = Array.from(document.querySelectorAll('.info-row-opcoes img, .slider-track img:first-child'));
        if(!imgs.length){{ dismiss(); return; }}
        var p = imgs.map(function(img){{
          if(img.complete && img.naturalWidth > 0) return Promise.resolve();
          if(img.decode) return img.decode().catch(function(){{ return Promise.resolve(); }});
          return new Promise(function(res){{ img.onload = res; img.onerror = res; }});
        }});
        Promise.all(p).then(function(){{
          setTimeout(dismiss, 50);
        }});
      }}
      if(document.readyState === 'loading'){{
        document.addEventListener('DOMContentLoaded', checkAndDismiss);
      }} else {{
        checkAndDismiss();
      }}
      setTimeout(dismiss, 650);
    }})();
  </script>

  <div class="app-container">

  <!-- HEADER -->
  <header class="header">
    <a class="header-back-btn" href="../index.html" aria-label="Voltar">
      <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </a>
    <div class="header-search-wrapper">
      <button class="header-search-icon-btn">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
      </button>
      <input type="text" class="header-search" placeholder="Pesquisar" readonly onclick="window.location='../index.html'">
    </div>
    <div class="header-icons">
      <button class="header-share-btn" onclick="shareProduct()" aria-label="Compartilhar">
        <img src="../img/share-arrow.png" alt="Compartilhar" style="width: 22px; height: 22px; object-fit: contain;">
        <span class="share-dot"></span>
      </button>
      <a href="../pages/carrinho.html" class="header-icon-btn" aria-label="Carrinho">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="9" cy="21" r="1"></circle>
          <circle cx="20" cy="21" r="1"></circle>
          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
        </svg>
        <span class="cart-badge" style="display:none">0</span>
      </a>
      <button class="header-more-btn" onclick="showMoreOptions()" aria-label="Mais opcoes">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
          <circle cx="5" cy="12" r="2"></circle>
          <circle cx="12" cy="12" r="2"></circle>
          <circle cx="19" cy="12" r="2"></circle>
        </svg>
      </button>
    </div>
  </header>

  <!-- TOOLTIP CIANO OFICIAL TIKTOK SHOP -->
  <div id="share-tooltip-bubble" class="share-tooltip-bubble" onclick="closeShareTooltip()">
    <div class="share-tooltip-arrow"></div>
    Compartilhe isso com amigos para ganhar comissoes nas compras deles
  </div>

  <!-- CONTEUDO DA PAGINA -->
  <div class="page-content">

    <!-- SLIDER DE IMAGENS -->
    <div class="image-slider">
      <div class="slider-track">
{slider_html}      </div>
      <div class="slider-indicator">1/{len(p['slider_images'])}</div>
    </div>

    <!-- ABAS DE NAVEGAÇÃO -->
    <nav class="product-tabs">
      <button class="product-tab active" data-tab="visao-geral">Visão geral</button>
      <button class="product-tab" data-tab="avaliacoes">Avaliações</button>
      <button class="product-tab" data-tab="descricao">Descrição</button>
      <button class="product-tab" data-tab="recomendacoes">Recomendações</button>
    </nav>

    <!-- SEÇÃO DE PREÇO / OFERTA RELÂMPAGO -->
    <div class="price-section">
      <div class="discount-badge-white">-{p['discount']}%</div>
      <div class="price-row">
        <span class="price-currency-sign">R$</span>
        <div class="price-current">{p['price_int']}<span class="price-cents">{p['price_cents']}</span></div>
      </div>
      <div class="price-original">R$ {p['price_orig']}</div>
      <div class="price-right">
        <div class="timer-row">
          <span class="timer-label">Termina em</span>
          <span class="timer-value oferta-timer">02:58:44</span>
        </div>
      </div>
    </div>

    <!-- INFORMAÇÕES DO PRODUTO -->
    <div class="product-info">

      <!-- 1. Parcelamento oficial TikTok Shop -->
      <div class="installment-row" style="display: flex; align-items: center; justify-content: space-between; font-size: 13px; color: #161823; cursor: pointer;" onclick="handleAddToCart()">
        <div style="display: inline-flex; align-items: center; gap: 5px;">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fe2c55" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect>
            <line x1="1" y1="10" x2="23" y2="10"></line>
          </svg>
          <span style="font-weight: 500;">{p['installment']}</span>
        </div>
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#8a8b91" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </div>

      <!-- Título do Produto -->
      <div class="product-title-row">
        <h1 class="product-title">{p['title']}</h1>
        <button class="btn-bookmark" onclick="toggleBookmark(this)" aria-label="Salvar produto">
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      </div>

      <!-- Avaliações e Vendas -->
      <div class="ratings-row" style="display: flex; align-items: center; gap: 6px; margin-bottom: 12px;">
        <div class="star-row" style="display: flex; align-items: center; gap: 4px;">
          <svg class="star-icon" viewBox="0 0 24 24" width="13" height="13" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          <span style="font-size: 13px; font-weight: 700; color: #161823;">{p['rating']}</span>
          <span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector('.reviews-section')?.scrollIntoView({{behavior:'smooth'}});">({p['reviews_count']})</span>
        </div>
        <span style="color: #e5e5e5; font-size: 12px; margin: 0 1px;">|</span>
        <div class="sold-count" style="font-size: 13px; color: #757575; font-weight: 400;">{p['sold_count']} vendidos</div>
      </div>

      <!-- BLOCO PRÉ-DESCRIÇÃO OFICIAL TIKTOK SHOP -->
      <div class="product-info-rows">
        <!-- Linha 1: Frete Grátis -->
        <div class="info-row-item" onclick="window.openEnvioModal && window.openEnvioModal()" style="cursor: pointer;">
          <div class="info-row-left">
            <div class="info-row-icon">
              <svg width="20" height="20" viewBox="0 -2 20 20" xmlns="http://www.w3.org/2000/svg">
                <g transform="translate(-2 -4)">
                  <path d="M9.17,17H13V6a1,1,0,0,0-1-1H5" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2"/>
                  <line fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" x1="1" x2="3" y1="9" y2="9"/>
                  <line fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" x1="1" x2="2.5" y1="12" y2="12"/>
                  <line fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2" x1="1" x2="3.5" y1="15" y2="15"/>
                  <path d="M13,9h4.55a1,1,0,0,1,.8.4l1.37,1.83a1,1,0,0,1,.2.6V16a1,1,0,0,1-1,1H17.41" fill="none" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2"/>
                  <circle cx="6.5" cy="17.5" fill="none" r="2.5" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2"/>
                  <circle cx="15.5" cy="17.5" fill="none" r="2.5" stroke="#222" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.2"/>
                </g>
              </svg>
            </div>
            <div class="info-row-texts">
              <div class="info-row-main"><strong style="color: #00b67a; font-weight: 700;">Frete grátis</strong></div>
              <div class="info-row-sub dynamic-delivery-date" style="font-size: 12px; color: #757575;">Receba em até 4 a 7 dias úteis</div>
            </div>
          </div>
          <div class="info-row-arrow">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#8a8b91" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </div>
        </div>

        <!-- Linha 2: Seletor de Opções com Miniaturas -->
        <div class="info-row-item" onclick="handleAddToCart()" style="cursor: pointer;">
          <div class="info-row-left">
            <div class="info-row-icon">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="#222" stroke-width="1.5">
                <rect x="3" y="3" width="7" height="7"></rect>
                <rect x="14" y="3" width="7" height="7"></rect>
                <rect x="14" y="14" width="7" height="7"></rect>
                <rect x="3" y="14" width="7" height="7"></rect>
              </svg>
            </div>
            <div class="info-row-texts">
              <div class="info-row-main"><strong>Selecione as opções</strong></div>
              <div class="info-row-sub" style="font-size: 12px; color: #757575;">{p['variation_preview_text']}</div>
            </div>
          </div>
          <div class="info-row-right">
            <div class="info-row-opcoes">
              {opt_thumbs_html}
            </div>
            <div class="info-row-arrow">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#8a8b91" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </div>
          </div>
        </div>

        <!-- Linha 3: Proteção do Cliente Oficial TikTok Shop -->
        <div class="info-row-item">
          <div class="info-row-left" style="align-items: flex-start;">
            <div class="info-row-icon" style="margin-top: 1px;">
              <svg viewBox="0 0 24 24" width="20" height="20" fill="none">
                <path d="M12 2L3 6v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V6l-9-4z" fill="#00b67a" fill-opacity="0.12" stroke="#00b67a" stroke-width="1.6" stroke-linejoin="round"/>
                <path d="M9 12l2 2 4-4" stroke="#00b67a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <div class="info-row-texts">
              <div class="info-row-main" style="display: flex; align-items: center; gap: 6px;">
                <strong style="color: #161823; font-weight: 700;">Proteção do cliente</strong>
              </div>
              <div class="info-row-sub" style="font-size: 12px; color: #757575; line-height: 1.45; margin-top: 2px;">
                Pagamento seguro · Devolução grátis em 7 dias · Reembolso garantido
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP -->
      <div id="creators-section" class="creators-section">
        <h3 class="creators-title">Vídeos de criadores (30+)</h3>
        <div class="creators-carousel" id="creators-carousel-list">
{creators_html}        </div>
      </div>

      <!-- AVALIAÇÕES -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes ({p['reviews_count']})</h3>
        <div class="reviews-summary" style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
          <span class="review-avg">{p['rating']}</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
            <svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="14" height="14"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
          </div>
        </div>

{reviews_html}      </div>

      <!-- DESCRIÇÃO -->
      <div class="description-section">
        <h3 class="description-header">Descrição do Produto</h3>
        {p['description_html']}
      </div>

    </div><!-- fim product-info -->

  </div><!-- fim page-content -->

  <!-- BARRA DE COMPRA FIXA INFERIOR -->
  <div class="bottom-bar">
    <a href="../index.html" class="bottom-bar-btn" aria-label="Início">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
      <span>Início</span>
    </a>
    <button class="bottom-bar-btn" onclick="shareProduct()" aria-label="Compartilhar">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="18" cy="5" r="3"></circle>
        <circle cx="6" cy="12" r="3"></circle>
        <circle cx="18" cy="19" r="3"></circle>
        <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
        <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
      </svg>
      <span>Partilhar</span>
    </button>
    <button class="btn-cart" id="btn-add-cart" onclick="handleAddToCart()" aria-label="Adicionar ao carrinho">
      <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="9" cy="21" r="1"></circle>
        <circle cx="20" cy="21" r="1"></circle>
        <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
      </svg>
    </button>
    <button class="btn-buy" id="btn-buy" onclick="handleBuyNow()">
      <span class="btn-line1">Compre</span>
      <span class="btn-line2">R$ {p['price_str']} com cupom</span>
    </button>
  </div>

</div><!-- fim app-container -->

<script src="../js/catalogo.js?v=1794108813711"></script>
<script src="../js/app.js?v=1794108813711"></script>
<script>
const PRODUTO_ATUAL = {prod_atual_json};

function handleAddToCart() {{
  if (typeof handleAddToCartWithVariacoes === 'function') {{
    handleAddToCartWithVariacoes(PRODUTO_ATUAL, false);
  }} else {{
    if (typeof addToCart === 'function') addToCart(PRODUTO_ATUAL);
  }}
}}

function handleBuyNow() {{
  if (typeof handleAddToCartWithVariacoes === 'function') {{
    handleAddToCartWithVariacoes(PRODUTO_ATUAL, true);
  }} else if (typeof irDiretoAoCheckoutComProduto === 'function') {{
    irDiretoAoCheckoutComProduto(PRODUTO_ATUAL, '', 1);
  }} else {{
    if (typeof addToCart === 'function') addToCart(PRODUTO_ATUAL);
    window.location.href = 'resumo.html?produto=' + PRODUTO_ATUAL.id + '&preco=' + PRODUTO_ATUAL.preco + '&v=' + Date.now();
  }}
}}

// PRE-AQUECIMENTO ULTRA-RAPIDO NO CACHE DA GPU (AVALIACOES E AVATARES - 0MS LAG)
(function() {{
  function prewarmReviewsAndAvatars() {{
    const list = {json.dumps(prewarm_photos)};
    list.forEach(function(url) {{
      const img = new Image();
      img.src = url;
      if (img.decode) {{
        img.decode().catch(function() {{}});
      }}
    }});
  }}
  if (document.readyState === 'complete') {{
    prewarmReviewsAndAvatars();
  }} else {{
    window.addEventListener('load', function() {{
      setTimeout(prewarmReviewsAndAvatars, 200);
    }}, {{ once: true, passive: true }});
  }}
}})();
</script>
<script src="/tracker.js"></script>
<script>
  function initShareTooltip() {{
    const tooltip = document.getElementById('share-tooltip-bubble');
    if (!tooltip) return;
    setTimeout(() => {{ tooltip.classList.add('visible'); }}, 400);
    setTimeout(() => {{ closeShareTooltip(); }}, 4800);
  }}
  function closeShareTooltip() {{
    const tooltip = document.getElementById('share-tooltip-bubble');
    if (tooltip) {{
      tooltip.classList.remove('visible');
      setTimeout(() => {{ if (tooltip && tooltip.parentNode) tooltip.style.display = 'none'; }}, 400);
    }}
  }}
  document.addEventListener('DOMContentLoaded', () => {{ initShareTooltip(); }});
</script>
<script>
function toggleBookmark(btn) {{
  const svg = btn.querySelector('svg');
  if (svg.getAttribute('fill') === 'currentColor') {{
    svg.setAttribute('fill', 'none');
  }} else {{
    svg.setAttribute('fill', 'currentColor');
  }}
}}
</script>
<script defer src="../js/videos-criadores.js?v=1794108813711"></script>
<!-- TIKTOK MODAL PLAYER OFICIAL (PRÉ-RENDERIZADO INSTANTÂNEO) -->
  <div class="tt-modal" id="tiktok-modal">
    <div class="tt-container">
      <div class="tt-top-bar">
        <button class="tt-back-btn" id="tt-close-btn" aria-label="Voltar">
          <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
        </button>
        <div class="tt-search-container">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input class="tt-search-input" type="text" value="Encontrar conteúdo relacionado" readonly>
        </div>
      </div>

      <div class="tt-video-wrapper" id="tt-video-wrapper">
        <video class="tt-video" id="tt-modal-player" muted loop playsinline webkit-playsinline autoplay preload="auto" style="background:#000;"></video>

        <div class="tt-sound-badge" id="tt-sound-badge" style="position: absolute; top: 14px; right: 14px; background: rgba(0,0,0,0.65); backdrop-filter: blur(4px); color: #fff; padding: 6px 12px; border-radius: 16px; font-size: 12px; font-weight: 600; z-index: 16; display: none; align-items: center; gap: 6px; cursor: pointer; border: 1px solid rgba(255,255,255,0.2);">
          <svg viewBox="0 0 24 24" width="16" height="16" fill="#fff"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/></svg>
          <span>Ativar som</span>
        </div>
        <div class="tt-play-icon-overlay" id="tt-play-overlay">
          <svg viewBox="0 0 24 24" width="34" height="34" fill="#fff"><path d="M8 5v14l11-7z"/></svg>
        </div>

        <div class="tt-right-actions">
          <div class="tt-creator-wrapper">
            <img loading="lazy" decoding="async" class="tt-creator-avatar" id="tt-action-avatar" src="" alt="">
            <button class="tt-follow-btn" id="tt-action-follow">+</button>
          </div>
          <button class="tt-action-btn" id="tt-action-like">
            <svg viewBox="0 0 24 24" width="32" height="32" fill="#fff"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            <span class="tt-action-label" id="tt-like-count">14.2K</span>
          </button>
          <button class="tt-action-btn" id="tt-action-comment">
            <svg viewBox="0 0 24 24" width="30" height="30" fill="#fff"><path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18zM18 14H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/></svg>
            <span class="tt-action-label" id="tt-comment-count">128</span>
          </button>
          <button class="tt-action-btn" id="tt-action-save">
            <svg viewBox="0 0 24 24" width="30" height="30" fill="#fff"><path d="M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2z"/></svg>
            <span class="tt-action-label" id="tt-save-count">3.4K</span>
          </button>
          <button class="tt-action-btn" id="tt-action-share">
            <svg viewBox="0 0 24 24" width="28" height="28" fill="#fff"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92z"/></svg>
            <span class="tt-action-label">Compartilhar</span>
          </button>
        </div>

        <div class="tt-left-info">
          <div class="tt-username" id="tt-display-name">@tiktokshop</div>
          <div class="tt-desc" id="tt-display-desc">Review oficial do produto</div>
        </div>

        <div class="tt-comments-drawer" id="tt-comments-drawer">
          <div class="tt-drawer-header">
            <span class="tt-drawer-title" id="tt-drawer-title">128 comentários</span>
            <button class="tt-drawer-close" id="tt-drawer-close">✕</button>
          </div>
          <div class="tt-drawer-list" id="tt-drawer-comments-list"></div>
          <div class="tt-comment-input-bar">
            <input type="text" class="tt-comment-input" id="tt-comment-input-field" placeholder="Adicionar comentário...">
            <button class="tt-comment-submit-btn" id="tt-comment-send-btn" aria-label="Enviar comentário">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="22" y1="2" x2="11" y2="13"></line>
                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</body>
</html>
"""
    out_file = f"pages/produto-{pid}.html"
    with open(out_file, "w", encoding="utf-8") as out:
        out.write(html_page)
    print(f"Page {out_file} generated successfully! Size: {len(html_page)} chars.")

print("All 5 product pages generated successfully!")
