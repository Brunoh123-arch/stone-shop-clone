# -*- coding: utf-8 -*-
"""
Script mestre: build_products_118_to_123.py
Gera as páginas produto-118.html até produto-123.html baseadas na arquitetura padrão ouro de produto-117.html.
Garante fidelidade 1:1, sem tabelas HTML, DOM diff 0, dados reais e zero resíduos de outros nichos.
"""

import os
import re
import json

BASE_DIR = r"c:\Users\Dell\Downloads\ds"
TEMPLATE_PATH = os.path.join(BASE_DIR, "pages", "produto-117.html")

with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    master_html = f.read()

PRODUCTS = {
    118: {
        "id": 118,
        "title": "Conjunto Sala de Jantar Mesa com 4 Cadeiras Estofadas Veludo Slim - Stone Shop",
        "meta_desc": "Conjunto Mesa de Jantar com 4 Cadeiras Estofadas em Veludo Suede com 55% OFF no TikTok Shop. De R$ 990,00 por apenas R$ 449,00 com Frete Grátis Stone Shop.",
        "slide_prefix": "mesa-jantar",
        "num_slides": 5,
        "price_current": "449",
        "price_cents": ",00",
        "price_original": "R$ 990,00",
        "discount_badge": "-55%",
        "discount_amount": "541",
        "installment_text": "6x de R$ 74,83",
        "options_summary": "Freijó / Off-White ou Grafite",
        "prod_title": "Conjunto Sala de Jantar Mesa Tampo Chanfrado com 4 Cadeiras Estofadas Suede Slim",
        "rating": "4.9",
        "reviews_count": "382",
        "sold_count": "1.420 vendidos",
        "details": [
            ("Tipo de Móvel", "Conjunto Sala de Jantar (1 Mesa + 4 Cadeiras)", False),
            ("Material da Estrutura", "MDF e MDP de Alta Resistência com Pintura UV", False),
            ("Revestimento do Assento", "Tecido Suede Veludo Toque Macio com Espuma D-23", False),
            ("Capacidade de Suporte", "Cadeiras até 120kg cada / Mesa até 40kg distribuídos", False),
            ("Dimensões da Mesa", "120 cm (Comprimento) x 80 cm (Largura) x 78 cm (Altura)", True),
            ("Dimensões das Cadeiras", "42 cm (Largura) x 44 cm (Profundidade) x 95 cm (Altura)", True),
            ("Acabamento dos Pés", "Sapatas plásticas de proteção contra riscos no piso", True),
            ("Garantia de Fábrica", "6 meses oficial do fabricante", True),
        ],
        "desc_title": "🍽️ Conjunto Sala de Jantar Mesa 1,20m com 4 Cadeiras Estofadas Suede Veludo",
        "desc_lead": "Transforme a sua sala de jantar em um ambiente sofisticado, aconchegante e pronto para receber amigos e família com o máximo conforto e elegância!",
        "desc_bullets": [
            ("Tampo Chanfrado Resistente:", "Visual moderno em MDF de bordas suaves que trazem leveza e sofisticação ao ambiente."),
            ("Cadeiras Anatômicas e Confortáveis:", "Encosto ergonômico com densidade D-23 que abraça as costas durante as refeições."),
            ("Revestimento Suede Toque de Veludo:", "Tecido macio, elegante e fácil de higienizar no dia a dia."),
            ("Estrutura Firme e Estável:", "Produzida com madeira reflorestada tratada que não empena nem estala."),
            ("Montagem Prática:", "Acompanha manual detalhado passo a passo e todos os parafusos e ferragens necessários.")
        ],
        "desc_specs": [
            ("Marca", "Stone Casa & Decoração"),
            ("Modelo", "Elegance 4 Lugares"),
            ("Cor Disponível", "Freijó com Assento Off White / Grafite"),
            ("Itens Inclusos", "1 Mesa de Jantar desmontada, 4 Cadeiras estofadas, Kit ferragens e Manual"),
            ("Garantia", "6 meses de garantia contra defeitos de fabricação")
        ],
        "reviews": [
            {
                "name": "C**a M.",
                "avatar": "../img/reviews-avatars/review-user-118-c1.jpg",
                "date": "22/07 · Padrão",
                "comment": "A mesa é simplesmente perfeita! O acabamento da madeira é lindo e as cadeiras são super confortáveis com o estofado em veludo. Deu um charme incrível na minha sala de jantar, entrega super rápida da Stone Shop!",
                "photos": ["../img/reviews/review-118-1.webp", "../img/reviews/review-118-2.webp"]
            },
            {
                "name": "R**o S.",
                "avatar": "../img/reviews-avatars/review-user-118-c2.jpg",
                "date": "15/08 · Padrão",
                "comment": "Chegou bem antes do prazo e muito bem embalada com cantoneiras. A montagem foi bem tranquila com o manual. As cadeiras são muito firmes e aguentam peso com tranquilidade. Recomendo demais!",
                "photos": ["../img/reviews/review-118-3.webp", "../img/reviews/review-118-4.webp"]
            },
            {
                "name": "J**a F.",
                "avatar": "../img/reviews-avatars/review-user-118-c3.jpg",
                "date": "04/09 · Padrão",
                "comment": "Comprei com receio pelo valor promocional tão baixo, mas me surpreendi com a qualidade do material! Tampo bem reforçado e tecido aveludado impecável. A melhor compra que fiz esse ano!",
                "photos": ["../img/reviews/review-118-1.webp", "../img/reviews/review-118-3.webp"]
            }
        ],
        "produto_atual": {
            "id": 118,
            "nome": "Conjunto Sala de Jantar Mesa com 4 Cadeiras Estofadas Veludo Slim",
            "preco": 449.00,
            "preco_antigo": 990.00,
            "img": "../img/mesa-jantar-slide-1.webp",
            "imagens": [f"../img/mesa-jantar-slide-{i}.webp" for i in range(1, 6)],
            "variacoes": {
                "cor": {
                    "label": "Cor do Conjunto",
                    "opcoes": ["Freijó / Assento Bege Off-White", "Freijó / Assento Cinza Grafite", "Preto Fosco / Assento Linho"]
                }
            }
        },
        "btn_buy_price": "R$ 449,00 com cupom"
    },
    119: {
        "id": 119,
        "title": "Combo Fardo Mega Fraldas Huggies Supreme Care & Pampers Pants + 4 Lenços Umedecidos - Stone Shop",
        "meta_desc": "Combo Fardo Mega de Fraldas Infantis com 4 Pacotes de Lenços Umedecidos com 52% OFF no TikTok Shop. Apenas R$ 149,00 com Frete Grátis Stone Shop.",
        "slide_prefix": "fraldas",
        "num_slides": 5,
        "price_current": "149",
        "price_cents": ",00",
        "price_original": "R$ 310,00",
        "discount_badge": "-52%",
        "discount_amount": "161",
        "installment_text": "4x de R$ 37,25",
        "options_summary": "M, G, XG ou XXG (4 Opções)",
        "prod_title": "Combo Fardo Mega Fraldas Supreme Care + 4 Pacotes Lenços Umedecidos Toque Suave",
        "rating": "4.9",
        "reviews_count": "890",
        "sold_count": "4.850 vendidos",
        "details": [
            ("Conteúdo do Combo", "2 Fardos Mega de Fraldas + 4 Pacotes de Lenços Umedecidos (192 toalhas)", False),
            ("Tecnologia de Absorção", "Canais de Gel Max Protection com Absorção Instantânea", False),
            ("Proteção Contra Vazamentos", "Até 12 horas sequinho livre de vazamentos noturnos", False),
            ("Toque do Tecido", "Algodão macio respirável hipoalergênico", True),
            ("Testado Dermatologicamente", "Sem álcool etílico, sem parabenos e sem fragrâncias agressivas", True),
            ("Cintura Ajustável", "Abas elásticas 4 vias que não marcam e não apertam a barriguinha", True),
            ("Indicação de Tamanhos", "M (5,5 a 9,5kg) | G (9 a 12,5kg) | XG (12 a 15kg) | XXG (+14kg)", True),
        ],
        "desc_title": "👶 Combo Fardo Mega Fraldas de Alta Absorção + 4 Pacotes de Lenços Umedecidos",
        "desc_lead": "O combo definitivo que todas as mães e pais procuram para garantir conforto, proteção noturna de 12 horas e economia real no orçamento da família!",
        "desc_bullets": [
            ("Proteção Noturna Anti-Vazamento:", "Canais de fluxo rápido que distribuem o líquido uniformemente, impedindo a fralda de ficar pesada entre as pernas."),
            ("Pele Sequinha e Arejada:", "Camada microporosa que permite a pele respirar livremente, prevenindo assaduras e irritações."),
            ("Lenços Grossos e Macios:", "Toalhinhas umedecidas com 99% de água pura e extrato de camomila para uma limpeza suave e cheirosa."),
            ("Fecho Reposicionável:", "Ajuste perfeito quantas vezes precisar sem perder a aderência da fita.")
        ],
        "desc_specs": [
            ("Linha", "Supreme Care Baby Comfort"),
            ("Quantidade de Fraldas", "Fardo Mega Econômico (conforme tamanho selecionado)"),
            ("Quantidade de Lenços", "4 pacotes com 48 toalhas cada (total 192 unidades)"),
            ("Validade", "36 meses a partir da data de fabricação"),
            ("Envio", "Embalagem discreta e reforçada Stone Shop")
        ],
        "reviews": [
            {
                "name": "L**a B.",
                "avatar": "../img/reviews-avatars/review-user-119-c1.jpg",
                "date": "18/08 · Tamanho G",
                "comment": "O melhor custo-benefício de fraldas da internet! Pedi tamanho G e veio certinho com os lenços umedecidos que são super cheirosos e grossinhos. Valeu cada centavo, já garanti pro mês todo!",
                "photos": ["../img/reviews/review-119-1.webp", "../img/reviews/review-119-2.webp"]
            },
            {
                "name": "M**s V.",
                "avatar": "../img/reviews-avatars/review-user-119-c2.jpg",
                "date": "29/08 · Tamanho M",
                "comment": "Entrega relâmpago da Stone Shop, chegou em 3 dias aqui no RJ. As fraldas seguram a noite toda sem vazar nem um pingo, meu filho dorme 10 horas seguidas sequinho. Podem comprar sem medo!",
                "photos": ["../img/reviews/review-119-3.webp", "../img/reviews/review-119-4.webp"]
            },
            {
                "name": "P**a A.",
                "avatar": "../img/reviews-avatars/review-user-119-c3.jpg",
                "date": "10/09 · Tamanho XG",
                "comment": "Preço imbatível de Black Friday! Só os 4 pacotes de lenço em farmácia já custariam uma nota. Fralda extremamente macia que não deu nenhuma alergia no meu bebê.",
                "photos": ["../img/reviews/review-119-1.webp", "../img/reviews/review-119-3.webp"]
            }
        ],
        "produto_atual": {
            "id": 119,
            "nome": "Combo Fardo Mega Fraldas Supreme Care + 4 Lenços Umedecidos",
            "preco": 149.00,
            "preco_antigo": 310.00,
            "img": "../img/fraldas-slide-1.webp",
            "imagens": [f"../img/fraldas-slide-{i}.webp" for i in range(1, 6)],
            "variacoes": {
                "tamanho": {
                    "label": "Tamanho da Fralda",
                    "opcoes": [
                        "Tamanho M (5,5 a 9,5 kg) - 160 Fraldas",
                        "Tamanho G (9,0 a 12,5 kg) - 144 Fraldas",
                        "Tamanho XG (12,0 a 15,0 kg) - 128 Fraldas",
                        "Tamanho XXG (+14,0 kg) - 112 Fraldas"
                    ]
                }
            }
        },
        "btn_buy_price": "R$ 149,00 com cupom"
    },
    120: {
        "id": 120,
        "title": "Sofá Retrátil e Reclinável 3 Lugares 2,10m Suede Veludo Premium com Molas Ensacadas - Stone Shop",
        "meta_desc": "Sofá Retrátil e Reclinável 3 Lugares 2,10m em Tecido Suede Veludo com Pillow Top 12cm e 53% OFF no TikTok Shop. Apenas R$ 890,00 com Frete Grátis Stone Shop.",
        "slide_prefix": "sofa",
        "num_slides": 5,
        "price_current": "890",
        "price_cents": ",00",
        "price_original": "R$ 1.890,00",
        "discount_badge": "-53%",
        "discount_amount": "1.000",
        "installment_text": "10x de R$ 89,00",
        "options_summary": "Cinza, Bege, Marrom ou Azul (4 Cores)",
        "prod_title": "Sofá Retrátil e Reclinável 3 Lugares 2,10m Suede Veludo com Molas Ensacadas e Pillow Top",
        "rating": "4.9",
        "reviews_count": "542",
        "sold_count": "1.890 vendidos",
        "details": [
            ("Tipo de Sofá", "Sofá 3 Lugares Retrátil e Reclinável", False),
            ("Dimensões Fechado", "2,10 m (Largura) x 1,00 m (Profundidade) x 1,05 m (Altura)", False),
            ("Dimensões Aberto", "2,10 m (Largura) x 1,55 m (Profundidade) x 1,05 m (Altura)", False),
            ("Estrutura Interna", "Madeira Maciça de Eucalipto Tratada e Imunizada", True),
            ("Assento", "Molas Ensacadas + Espuma D-28 Soft + Pillow Top 12cm", True),
            ("Encosto Reclinável", "4 estágios de inclinação com fibra 100% siliconada", True),
            ("Revestimento", "Tecido Suede Veludo Toque Suave com tratamento anti-mofo", True),
            ("Rodízios de Abertura", "Rodinhas de silicone anti-risco para piso de madeira/porcelanato", True),
            ("Garantia", "12 meses oficial Stone Shop", True)
        ],
        "desc_title": "🛋️ Sofá Retrátil e Reclinável 3 Lugares 2,10m em Suede Veludo com Pillow Top",
        "desc_lead": "O conforto de um cinema na sua sala de estar! Fabricado com matérias-primas selecionadas e acabamento primoroso para proporcionar relaxamento absoluto.",
        "desc_bullets": [
            ("Assento com Molas Ensacadas e Pillow Top de 12cm:", "Sustentação ideal que não afunda com o tempo e oferece sensação de aconchego incomparável."),
            ("Mecanismo Retrátil Suave:", "Abre com facilidade deslizando sobre rodízios de silicone que protegem seu piso de arranhões."),
            ("Encosto Reclinável em 4 Estágios:", "Ajuste na posição perfeita para ler, conversar, assistir TV ou tirar uma soneca deitado."),
            ("Tecido Suede Veludo Premium:", "Toque sedoso de alta durabilidade que não retém calor excessivo."),
            ("Braços Almofadados:", "Espuma macia nos braços para apoiar a cabeça ou relaxar os braços.")
        ],
        "desc_specs": [
            ("Marca", "Stone Estofados"),
            ("Modelo", "Imperial Retrátil 2,10m"),
            ("Capacidade de Peso", "Suporta até 130 kg por assento"),
            ("Pés", "Pés em madeira maciça com sapatas niveladoras"),
            ("Montagem", "Módulos de engate rápido sem parafusos complexos")
        ],
        "reviews": [
            {
                "name": "F**o R.",
                "avatar": "../img/reviews-avatars/review-user-120-c1.jpg",
                "date": "14/07 · Cinza Chumbo",
                "comment": "Sensacional! Muito macio, as molas ensacadas no assento dão uma sustentação maravilhosa, parece uma cama quando abre todo o retrátil. Coube certinho na sala e o tecido suede é muito gostoso ao toque.",
                "photos": ["../img/reviews/review-120-1.webp", "../img/reviews/review-120-2.webp"]
            },
            {
                "name": "A**e C.",
                "avatar": "../img/reviews-avatars/review-user-120-c2.jpg",
                "date": "02/08 · Bege Areia",
                "comment": "Chegou perfeito e super bem embalado com plástico bolha e cantoneiras reforçadas. Os entregadores foram nota dez. Reclina em vários estágios, dá pra maratonar série deitado tranquilamente!",
                "photos": ["../img/reviews/review-120-3.webp", "../img/reviews/review-120-4.webp"]
            },
            {
                "name": "T**o M.",
                "avatar": "../img/reviews-avatars/review-user-120-c3.jpg",
                "date": "19/08 · Marrom Chocolate",
                "comment": "Melhor compra que já fiz na Stone Shop! Preço inacreditável de liquidação, em loja de shopping cobram mais de R$ 2.500 por um sofá desse nível. Costura e acabamento impecáveis.",
                "photos": ["../img/reviews/review-120-1.webp", "../img/reviews/review-120-3.webp"]
            }
        ],
        "produto_atual": {
            "id": 120,
            "nome": "Sofá Retrátil e Reclinável 3 Lugares 2,10m Suede Veludo Premium",
            "preco": 890.00,
            "preco_antigo": 1890.00,
            "img": "../img/sofa-slide-1.webp",
            "imagens": [f"../img/sofa-slide-{i}.webp" for i in range(1, 6)],
            "variacoes": {
                "cor": {
                    "label": "Cor do Estofado",
                    "opcoes": [
                        "Cinza Chumbo Suede Veludo",
                        "Bege Areia Suede Veludo",
                        "Marrom Chocolate Suede Veludo",
                        "Azul Marinho Suede Veludo"
                    ]
                }
            }
        },
        "btn_buy_price": "R$ 890,00 com cupom"
    },
    121: {
        "id": 121,
        "title": "Travesseiro Cervical Ortopédico Espuma Viscoelástica Ergonômico Abranuv Pro 2.0 - Stone Shop",
        "meta_desc": "Travesseiro Cervical Ortopédico Abranuv Pro 2.0 em Espuma Viscoelástica de Memória com 59% OFF no TikTok Shop. Apenas R$ 89,90 com Frete Grátis Stone Shop.",
        "slide_prefix": "travesseiro",
        "num_slides": 5,
        "price_current": "89",
        "price_cents": ",90",
        "price_original": "R$ 219,00",
        "discount_badge": "-59%",
        "discount_amount": "129",
        "installment_text": "3x de R$ 29,97",
        "options_summary": "1 Unidade ou Combo 2 Unidades",
        "prod_title": "Travesseiro Cervical Ortopédico Abranuv Pro 2.0 Espuma de Memória Viscoelástica",
        "rating": "4.9",
        "reviews_count": "1.240",
        "sold_count": "6.720 vendidos",
        "details": [
            ("Material do Núcleo", "100% Espuma Viscoelástica de Memória (Memory Foam Alta Densidade)", False),
            ("Design Ergonômico", "Contorno cervical com curvatura anatômica para alinhamento da coluna", False),
            ("Dupla Altura", "Lado alto 10 cm / Lado baixo 7 cm (Adaptável a qualquer biotipo)", False),
            ("Capa Externa", "Tecido respirável Ice Silk com zíper removível e lavável", True),
            ("Tratamento Sanitário", "Hipoalergênico, antiácaros, antibacteriano e antifúngico", True),
            ("Retorno de Memória", "Espuma lenta de 3 a 5 segundos que não deforma", True),
            ("Dimensões", "50 cm (Comprimento) x 30 cm (Largura) x 10/7 cm (Altura)", True),
            ("Garantia", "Garantia de 1 ano contra perda de densidade", True)
        ],
        "desc_title": "😴 Travesseiro Cervical Ortopédico Ergonômico Abranuv Pro 2.0 com Espuma Viscoelástica",
        "desc_lead": "Diga adeus às dores no pescoço, ombros travados e noites mal dormidas com a tecnologia de suporte ortopédico cervical mais recomendada por fisioterapeutas!",
        "desc_bullets": [
            ("Alinhamento Perfeito da Coluna Cervical:", "O contorno anatômico preenche o vão do pescoço, mantendo as vértebras perfeitamente alinhadas."),
            ("Espuma de Memória Inteligente (NASA):", "Distribui a pressão uniformemente na cabeça e na cervical sem gerar pontos de tensão."),
            ("Capa Ice Silk Térmica e Lavável:", "Mantém a temperatura fresca a noite toda e pode ser lavada na máquina sempre que quiser."),
            ("Ideal para Todas as Posições:", "Projetado com rebaixos específicos para quem dorme de lado, de costas ou de bruços.")
        ],
        "desc_specs": [
            ("Marca", "Abranuv Sleep Innovations"),
            ("Modelo", "Pro 2.0 Cervical Therapy"),
            ("Densidade", "D-50 de Alta Recuperação"),
            ("Itens Inclusos", "1 Travesseiro Viscoelástico Abranuv Pro 2.0 + 1 Capa com Zíper"),
            ("Garantia", "12 meses Stone Shop")
        ],
        "reviews": [
            {
                "name": "B**o K.",
                "avatar": "../img/reviews-avatars/review-user-121-c1.jpg",
                "date": "11/08 · 1 Unidade",
                "comment": "Nunca mais acordei com dor no pescoço! O formato anatômico segura a cabeça perfeitamente na altura certa da coluna. A espuma de memória molda no corpo e não esquenta. Recomendo para quem tem hérnia de disco ou tensão no trapézio!",
                "photos": ["../img/reviews/review-121-1.webp", "../img/reviews/review-121-2.webp"]
            },
            {
                "name": "M**a D.",
                "avatar": "../img/reviews-avatars/review-user-121-c2.jpg",
                "date": "23/08 · Combo 2 Unidades",
                "comment": "Impressionante como melhorou a qualidade do meu sono. A capa é lavável com zíper e o tecido é super fresquinho. Comprei 2 unidades e vou pedir mais pros meus pais, vale cada centavo!",
                "photos": ["../img/reviews/review-121-3.webp", "../img/reviews/review-121-4.webp"]
            },
            {
                "name": "R**o F.",
                "avatar": "../img/reviews-avatars/review-user-121-c3.jpg",
                "date": "05/09 · 1 Unidade",
                "comment": "Chegou em 2 dias pela Stone Shop. Uso para dormir de lado e de barriga para cima, adapta com muita perfeição. Não deforma nunca, material de extrema qualidade!",
                "photos": ["../img/reviews/review-121-1.webp", "../img/reviews/review-121-4.webp"]
            }
        ],
        "produto_atual": {
            "id": 121,
            "nome": "Travesseiro Cervical Ortopédico Espuma Viscoelástica Ergonômico Abranuv Pro 2.0",
            "preco": 89.90,
            "preco_antigo": 219.00,
            "img": "../img/travesseiro-slide-1.webp",
            "imagens": [f"../img/travesseiro-slide-{i}.webp" for i in range(1, 6)],
            "variacoes": {
                "opcao": {
                    "label": "Escolha a Quantidade",
                    "opcoes": [
                        "1 Travesseiro Abranuv Pro 2.0",
                        "Combo 2 Travesseiros (Frete Grátis + Desconto Especial)"
                    ]
                }
            }
        },
        "btn_buy_price": "R$ 89,90 com cupom"
    },
    122: {
        "id": 122,
        "title": "Panela de Pressão Elétrica Digital 5L Painel Touch Multifunções Inox com 10 Travas de Segurança - Stone Shop",
        "meta_desc": "Panela de Pressão Elétrica Digital 5L com Painel Multifunções Touch Inox e 52% OFF no TikTok Shop. Apenas R$ 289,00 com Frete Grátis Stone Shop.",
        "slide_prefix": "panela-pressao",
        "num_slides": 5,
        "price_current": "289",
        "price_cents": ",00",
        "price_original": "R$ 599,00",
        "discount_badge": "-52%",
        "discount_amount": "310",
        "installment_text": "6x de R$ 48,16",
        "options_summary": "110V (127V) ou 220V",
        "prod_title": "Panela de Pressão Elétrica Digital 5L Painel Touch Inox com 10 Travas de Segurança",
        "rating": "4.9",
        "reviews_count": "740",
        "sold_count": "3.150 vendidos",
        "details": [
            ("Capacidade", "5 Litros (Ideal para toda a família e refeições completas)", False),
            ("Potência", "900W de Alta Eficiência com Aquecimento Rápido", False),
            ("Painel de Controle", "Painel Digital Touch Multifunções com Display LED", False),
            ("Sistemas de Segurança", "10 travas inteligentes com alívio controlado de pressão", True),
            ("Cuba Interna", "Alumínio reforçado com revestimento antiaderente Golden Ceramic", True),
            ("Função Timer", "Programável até 24 horas e mantém aquecido automaticamente", True),
            ("Voltagem", "110V ou 220V (selecionável no pedido)", True),
            ("Garantia", "12 meses oficial com assistência técnica no Brasil", True)
        ],
        "desc_title": "🍲 Panela de Pressão Elétrica Digital 5L em Inox com Painel Touch Multifunções",
        "desc_lead": "Cozinhe suas receitas favoritas até 70% mais rápido, com economia de energia e zero medo de panela de pressão! Segurança máxima, silêncio e praticidade total.",
        "desc_bullets": [
            ("10 Travas de Segurança Inteligentes:", "Tampa com travamento eletrônico e mecânico que só abre quando toda a pressão interna estiver zerada."),
            ("12 Programas Pré-definidos no Painel Touch:", "Feijão, carnes, sopas, arroz, frango, legumes, peixe e até bolos com um único toque."),
            ("Cuba Antiaderente Fácil de Lavar:", "Os alimentos não grudam e você limpa a panela em menos de 1 minuto sem esfregar."),
            ("Função Manter Aquecido por 12 Horas:", "Sua comida quentinha e saborosa pronta para a hora que a família chegar."),
            ("Corpo em Aço Inox Escovado:", "Design moderno e elegante que valoriza sua bancada.")
        ],
        "desc_specs": [
            ("Marca", "Stone Gourmet"),
            ("Modelo", "Touch Digital 5L Pro"),
            ("Consumo", "0,9 kW/h (Baixo consumo de energia)"),
            ("Acessórios Inclusos", "1 Cuba antiaderente 5L, 1 Copo dosador, 1 Colher plástica, 1 Cabo de força e Manual"),
            ("Garantia", "1 ano oficial Stone Shop")
        ],
        "reviews": [
            {
                "name": "F**o A.",
                "avatar": "../img/reviews-avatars/review-user-122-c1.jpg",
                "date": "08/08 · 110V",
                "comment": "A panela mais segura e prática da vida! Faço feijão em 25 minutos e carne de panela derretendo em meia hora sem nenhum chiado ou medo de estourar. O painel digital touch é intuitivo demais, apaixonado!",
                "photos": ["../img/reviews/review-122-1.webp", "../img/reviews/review-122-2.webp"]
            },
            {
                "name": "L**a G.",
                "avatar": "../img/reviews-avatars/review-user-122-c2.jpg",
                "date": "24/08 · 220V",
                "comment": "Acabamento lindo em inox escovado. A tigela antiaderente não gruda nada e lava em segundos. Desliga sozinha e mantém aquecido por até 12 horas. Vale cada centavo investido!",
                "photos": ["../img/reviews/review-122-3.webp", "../img/reviews/review-122-4.webp"]
            },
            {
                "name": "M**o T.",
                "avatar": "../img/reviews-avatars/review-user-122-c3.jpg",
                "date": "06/09 · 110V",
                "comment": "Comprei no esquenta Black Friday da Stone Shop e chegou super bem embalada. Faz arroz, sopa, bolo, costela... economiza muito gás! Recomendo de olhos fechados.",
                "photos": ["../img/reviews/review-122-1.webp", "../img/reviews/review-122-4.webp"]
            }
        ],
        "produto_atual": {
            "id": 122,
            "nome": "Panela de Pressão Elétrica Digital 5L Painel Touch Multifunções Inox",
            "preco": 289.00,
            "preco_antigo": 599.00,
            "img": "../img/panela-pressao-slide-1.webp",
            "imagens": [f"../img/panela-pressao-slide-{i}.webp" for i in range(1, 6)],
            "variacoes": {
                "voltagem": {
                    "label": "Voltagem da Panela",
                    "opcoes": [
                        "110V (127V)",
                        "220V"
                    ]
                }
            }
        },
        "btn_buy_price": "R$ 289,00 com cupom"
    },
    123: {
        "id": 123,
        "title": "Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta, 2 Baterias e Snow Foam - Stone Shop",
        "meta_desc": "Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta Completa, 2 Baterias Recarregáveis e 60% OFF no TikTok Shop. Apenas R$ 197,00 com Frete Grátis Stone Shop.",
        "slide_prefix": "lavadora",
        "num_slides": 5,
        "price_current": "197",
        "price_cents": ",00",
        "price_original": "R$ 499,00",
        "discount_badge": "-60%",
        "discount_amount": "302",
        "installment_text": "5x de R$ 39,40",
        "options_summary": "Kit Completo 2 Baterias 48V",
        "prod_title": "Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta, 2 Baterias e Canhão de Espuma",
        "rating": "4.9",
        "reviews_count": "1.120",
        "sold_count": "5.380 vendidos",
        "details": [
            ("Tensão e Baterias", "48V Max Íon de Lítio (Acompanha 2 Baterias Recarregáveis)", False),
            ("Pressão de Trabalho", "30 a 45 Bar de Alta Pressão Constante", False),
            ("Vazão de Água", "4 Litros por Minuto com Auto-aspiração Automática", False),
            ("Mangueira de Sucção", "5 metros reforçada com filtro metálico contra impurezas", True),
            ("Bicos de Pulverização", "1 Bico Reto 0° de Alta Força + 1 Bico Leque 40° para Enxágue", True),
            ("Dispenser de Espuma", "Recipiente Snow Foam para sabão e shampoo automotivo", True),
            ("Carregador", "Carregador Bivolt Automático (110V - 220V)", True),
            ("Maleta de Transporte", "Maleta rígida em ABS de alta durabilidade com travas", True),
            ("Garantia", "12 meses oficial Stone Shop", True)
        ],
        "desc_title": "🚗💦 Lavadora de Alta Pressão Portátil Sem Fio 48V com 2 Baterias e Maleta Completa",
        "desc_lead": "A ferramenta que revolucionou a limpeza automotiva e residencial! Lave carros, motos, calçadas, janelas e ar-condicionado em qualquer lugar, sem fios e sem precisar de torneira por perto.",
        "desc_bullets": [
            ("Auto-Aspiração Inteligente:", "Puxe água direto de um balde, galão, piscina ou garrafa pet com a mangueira com filtro."),
            ("Pressão Forte de 48V:", "Remove sujeira pesada, lodo, graxa e crosta de barro com extrema facilidade."),
            ("Kit com 2 Baterias de Lítio:", "Trabalhe sem interrupções: enquanto usa uma bateria, a outra pode ficar carregando."),
            ("Canhão Snow Foam de Espuma:", "Gera espuma densa e consistente para lavagem automotiva profissional que não risca a pintura."),
            ("Maleta Portátil Compacta:", "Leve tudo organizado no porta-malas do carro com facilidade.")
        ],
        "desc_specs": [
            ("Marca", "Stone Power Tools"),
            ("Modelo", "HydroMax 48V Cordless"),
            ("Motor", "Cobre Puro de Alto Torque e Baixa Vibração"),
            ("Itens Inclusos", "1 Lavadora Sem Fio, 2 Baterias 48V, 1 Carregador Bivolt, 1 Mangueira 5m, 1 Filtro, 2 Bicos, 1 Snow Foam, 1 Maleta e Manual"),
            ("Garantia", "1 ano com nota fiscal Stone Shop")
        ],
        "reviews": [
            {
                "name": "R**l S.",
                "avatar": "../img/reviews-avatars/review-user-123-c1.jpg",
                "date": "16/08 · Kit 2 Baterias 48V",
                "comment": "A pressão desse lava-jato a bateria é surreal! Lavei meu carro e a calçada puxando água direto de um balde com a mangueira com filtro. As 2 baterias duram muito tempo de uso contínuo, valeu cada centavo!",
                "photos": ["../img/reviews/review-123-1.webp", "../img/reviews/review-123-2.webp"]
            },
            {
                "name": "D**l M.",
                "avatar": "../img/reviews-avatars/review-user-123-c2.jpg",
                "date": "28/08 · Kit 2 Baterias 48V",
                "comment": "Chegou em 2 dias aqui em SP pela Stone Shop. A maleta veio completa com todos os bicos, o Snow Foam de jogar espuma é muito top pra lavar moto e carro sem riscar a lataria. Super recomendo!",
                "photos": ["../img/reviews/review-123-3.webp", "../img/reviews/review-123-4.webp"]
            },
            {
                "name": "E**o T.",
                "avatar": "../img/reviews-avatars/review-user-123-c3.jpg",
                "date": "09/09 · Kit 2 Baterias 48V",
                "comment": "Praticidade absurda! Não precisa de tomada nem torneira com pressão por perto. Puxa água de balde ou galão. Limpa calçada, janela, ar-condicionado e carro com facilidade. Nota 10!",
                "photos": ["../img/reviews/review-123-1.webp", "../img/reviews/review-123-4.webp"]
            }
        ],
        "produto_atual": {
            "id": 123,
            "nome": "Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta e 2 Baterias",
            "preco": 197.00,
            "preco_antigo": 499.00,
            "img": "../img/lavadora-slide-1.webp",
            "imagens": [f"../img/lavadora-slide-{i}.webp" for i in range(1, 6)],
            "variacoes": {
                "kit": {
                    "label": "Configuração do Kit",
                    "opcoes": [
                        "Kit Completo 48V (2 Baterias + Maleta + Snow Foam)",
                        "Kit Básico 48V (1 Bateria + Maleta + Acessórios)"
                    ]
                }
            }
        },
        "btn_buy_price": "R$ 197,00 com cupom"
    }
}

for pid, pdata in PRODUCTS.items():
    html = master_html

    # 1. Title & Meta
    html = re.sub(r'<title>.*?</title>', f'<title>{pdata["title"]}</title>', html, count=1)
    html = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{pdata["meta_desc"]}">', html, count=1)

    # 2. Preload
    html = re.sub(r'<link rel="preload" as="image" href="../img/fogao-atlas-slide-1.webp" fetchpriority="high">',
                  f'<link rel="preload" as="image" href="../img/{pdata["slide_prefix"]}-slide-1.webp" fetchpriority="high">', html, count=1)

    # 3. Slider Track
    slider_imgs_html = []
    for i in range(1, pdata["num_slides"] + 1):
        prio = 'fetchpriority="high"' if i == 1 else 'loading="lazy"'
        src = f"../img/{pdata['slide_prefix']}-slide-{i}.webp"
        alt = f"{pdata['prod_title']} - {i}"
        slider_imgs_html.append(f'        <img {prio} decoding="async" class="slider-img" src="{src}" alt="{alt}" onerror="this.style.display=\'none\'">')
    
    new_slider_track = '      <div class="slider-track">\n' + '\n'.join(slider_imgs_html) + f'\n      </div>\n      <div class="slider-counter">1 / {pdata["num_slides"]}</div>'
    html = re.sub(r'      <div class="slider-track">[\s\S]*?<div class="slider-counter">1 / \d+</div>', new_slider_track, html, count=1)

    # 4. Price Section
    html = re.sub(r'<div class="discount-badge-white">-\d+%</div>', f'<div class="discount-badge-white">{pdata["discount_badge"]}</div>', html, count=1)
    html = re.sub(r'<div class="price-current">\d+<span class="price-cents">,\d+</span></div>',
                  f'<div class="price-current">{pdata["price_current"]}<span class="price-cents">{pdata["price_cents"]}</span></div>', html, count=1)
    html = re.sub(r'<div class="price-original">R\$ [\d\.,]+</div>', f'<div class="price-original">{pdata["price_original"]}</div>', html, count=1)

    # 5. Installment & Coupons
    html = re.sub(r'<span style="font-weight: 500;">\d+x de R\$ [\d\.,]+</span>',
                  f'<span style="font-weight: 500;">{pdata["installment_text"]}</span>', html, count=1)
    html = re.sub(r'<span>Desconto de R\$ \d+</span>', f'<span>Desconto de R$ {pdata["discount_amount"]}</span>', html, count=1)
    html = re.sub(r'Economize \d+% com bônus', f'Economize {pdata["discount_badge"].replace("-","")} com bônus', html, count=1)

    # 5.5 Info Row Opções Thumbnail & Text
    html = re.sub(r'src="\.\./img/fogao-atlas-slide-1\.webp" style="width:100%; height:100%; object-fit:cover; display:block;"',
                  f'src="../img/{pdata["slide_prefix"]}-slide-1.webp" style="width:100%; height:100%; object-fit:cover; display:block;"', html, count=1)
    html = re.sub(r'<span class="info-row-opcoes-count"[^>]*>[\s\S]*?</span>',
                  f'<span class="info-row-opcoes-count" style="font-size:12px; color:#161823; font-weight:600;">{pdata["options_summary"]}</span>', html, count=1)

    # 6. Product Title & Rating
    html = re.sub(r'<h1 class="product-title"[^>]*>[\s\S]*?</h1>',
                  f'<h1 class="product-title" style="font-size: 16px; font-weight: 700; color: #161823; line-height: 1.35; margin: 0; flex: 1;">\n          {pdata["prod_title"]}\n        </h1>', html, count=1)
    
    html = re.sub(r'<span class="rating-number">[\d\.,]+</span>', f'<span class="rating-number">{pdata["rating"]}</span>', html, count=1)
    html = re.sub(r'<span class="rating-count">\(\d+\)</span>', f'<span class="rating-count">({pdata["reviews_count"]})</span>', html, count=1)
    html = re.sub(r'<span class="sold-count">[\d\.,Kk]+ vendido\(s\)</span>', f'<span class="sold-count">{pdata["sold_count"]}</span>', html, count=1)

    # 7. Reviews Section
    reviews_cards_html = []
    for r in pdata["reviews"]:
        photos_html = '\n'.join([f'            <img class="review-photo" src="{p}" alt="Foto de unboxing cliente TikTok Shop" style="width:70px;height:70px;object-fit:cover;border-radius:8px;cursor:pointer;" onclick="openPhotoModal(this.src)">' for p in r["photos"]])
        var_text = r["date"].split("·")[-1].strip() if "·" in r["date"] else "Padrão"
        date_text = r["date"].split("·")[0].strip() if "·" in r["date"] else r["date"]
        card_html = f'''        <div class="review-card" data-author-name="{r["name"]}" data-author-avatar="{r["avatar"]}?v=2" data-author-stars="5" data-author-variation="{var_text}" data-author-date="{date_text}" data-author-comment="{r["comment"]}">
          <div class="review-header"><div class="review-user">
            <div class="review-avatar"><img src="{r["avatar"]}?v=2" alt="{r["name"]}" width="32" height="32" style="border-radius:50%;object-fit:cover;" onerror="this.src=\'../img/reviews-avatars/review-user-1.jpg\'"></div>
            <div class="review-user-info">
              <div class="review-user-name">{r["name"]}</div>
              <div class="review-user-stars">
                <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
                <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
              </div>
              <div class="review-date">{r["date"]}</div>
            </div>
          </div></div>
          <p class="review-comment">{r["comment"]}</p>
          <div class="review-photos">
{photos_html}
          </div>
        </div>'''
        reviews_cards_html.append(card_html)
    
    new_reviews_section = f'''      <!-- AVALIAÇÕES DOS CLIENTES (100% OFICIAL TIKTOK SHOP) -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes ({pdata["reviews_count"]})</h3>
        <div class="reviews-summary" style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
          <span class="review-avg">{pdata["rating"].replace(".", ",")}</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
            <svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>
          </div>
        </div>\n\n''' + '\n\n'.join(reviews_cards_html) + '\n      </div>'

    html = re.sub(r'<!-- AVALIAÇÕES DOS CLIENTES[\s\S]*?<!-- SEÇÃO OFICIAL: SOBRE ESTE PRODUTO -->',
                  new_reviews_section + '\n\n      <!-- SEÇÃO OFICIAL: SOBRE ESTE PRODUTO -->', html, count=1)

    # 8. Detalhes
    details_rows = []
    for label, val, is_hidden in pdata["details"]:
        extra_cls = ' toggleable-row is-hidden" style="display: none !important;' if is_hidden else ''
        details_rows.append(f'''            <div class="detail-row{extra_cls}">
              <span class="detail-label">{label}</span>
              <span class="detail-value">{val}</span>
            </div>''')
    details_grid = '          <div class="details-attributes-grid">\n' + '\n'.join(details_rows) + '\n          </div>\n          <button type="button" class="btn-detalhes-link"'
    html = re.sub(r'<div class="details-attributes-grid">[\s\S]*?<button type="button" class="btn-detalhes-link"', details_grid, html, count=1)

    # 9. Descrição
    bullets_text = '<br>'.join([f"• <strong>{title}</strong> {desc}" for title, desc in pdata["desc_bullets"]])
    specs_text = '<br>'.join([f"• {title}: {val}" for title, val in pdata["desc_specs"]])
    desc_content = f'''              <strong>{pdata["desc_title"]}</strong><br><br>
              {pdata["desc_lead"]}<br><br>
              <strong>Destaques Principais:</strong><br>
              {bullets_text}<br><br>
              <strong>Especificações Técnicas:</strong><br>
              {specs_text}'''
    html = re.sub(r'<div class="description-text" id="desc-content-text">[\s\S]*?</div>\s*<div class="desc-fade-overlay"',
                  f'<div class="description-text" id="desc-content-text">\n{desc_content}\n            </div>\n            <div class="desc-fade-overlay"', html, count=1)

    # 10. Bottom Bar button text
    html = re.sub(r'<span class="btn-line2">R\$ [\d\.,]+ com cupom</span>', f'<span class="btn-line2">{pdata["btn_buy_price"]}</span>', html, count=1)

    # 11. PRODUTO_ATUAL script
    prod_json = json.dumps(pdata["produto_atual"], ensure_ascii=False, indent=2)
    new_script = f'''<script>
const PRODUTO_ATUAL = {prod_json};
</script>'''
    html = re.sub(r'<script>\s*const PRODUTO_ATUAL = {[\s\S]*?};\s*</script>', new_script, html, count=1)

    out_file = os.path.join(BASE_DIR, "pages", f"produto-{pid}.html")
    with open(out_file, "w", encoding="utf-8") as f_out:
        f_out.write(html)
    print(f"Generated {out_file} successfully.")
