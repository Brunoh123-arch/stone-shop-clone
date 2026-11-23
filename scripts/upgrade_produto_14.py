import re

print("Iniciando upgrade cirurgico do Produto 14 (Churrasqueira Arke)...")

# 1. ATUALIZAR js/videos-criadores.js
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Criadores reais de churrasco e churrasqueira
creators_data = [
    {"name": "Rosita21", "username": "rosegodoi.finds", "likes": 37000, "comments": 41, "shares": 485, "title": "Churrasqueira Elétrica Arke Vitta Smart | Rotativa 5 Espetos | Churrasco Sem Fumaça no Apartamento 🔥🥩"},
    {"name": "Escolha Certa", "username": "_escolhas_certas", "likes": 18000, "comments": 14, "shares": 145, "title": "Churrasqueira Elétrica Arke Apartamento Rotativa Com 5 Espetos 220v Vitta Smart. Muito prática!"},
    {"name": "Cybelar", "username": "lojacybelararturnogueira", "likes": 28700, "comments": 23, "shares": 111, "title": "Faça seu churrasco suculento e sem fumaça na churrasqueira Arke giratória! 🍖"},
    {"name": "Ludmila", "username": "chicwoman112", "likes": 12190, "comments": 18, "shares": 74, "title": "Churrasqueira Rotativa Arke Vitta 5 Espetos: praticidade no churrasco sem fumaça no apê."},
    {"name": "Luminashopp", "username": "luminashopp2", "likes": 14500, "comments": 32, "shares": 190, "title": "Churrasqueira Rotativa 5 Espetos Arke - Sabor da churrascaria direto na sua casa! 🔥"},
    {"name": "Handira Ferreira", "username": "handiraferreira", "likes": 16400, "comments": 27, "shares": 115, "title": "Churrasqueira Arke de Apartamento: carne macia, sem fumaça e super fácil de limpar!"},
    {"name": "MultiMundial", "username": "multimundial", "likes": 21300, "comments": 45, "shares": 310, "title": "Sistema rotativo para espetinho e cortes nobres: assa por igual de verdade."},
    {"name": "EspetoSul", "username": "espetosul", "likes": 25800, "comments": 53, "shares": 420, "title": "Demonstração do giro contínuo e ponto perfeito da carne na churrasqueira rotativa."},
    {"name": "Frigo Gastronomia", "username": "frigooficial", "likes": 19200, "comments": 38, "shares": 240, "title": "Dica de ouro para apartamento: churrasqueira rotativa com bandeja coletora de gordura!"},
    {"name": "Churrasco Terapia", "username": "churrascoterapia", "likes": 42000, "comments": 89, "shares": 850, "title": "Picanha e fraldinha na rotativa elétrica: zero fumaça e muito suculenta!"},
    {"name": "Mestre do Churrasco", "username": "mestredochurras", "likes": 31500, "comments": 62, "shares": 490, "title": "5 espetos rodando ao mesmo tempo: coraçãozinho, picanha, linguiça e queijo coalho!"},
    {"name": "Lar & Cozinha", "username": "lar.e.cozinha", "likes": 15700, "comments": 29, "shares": 180, "title": "Melhor aquisição pro nosso apartamento! Não junta gordura nas paredes."},
    {"name": "Dicas Gourmet", "username": "dicasgourmetbr", "likes": 22400, "comments": 41, "shares": 260, "title": "Como usar a churrasqueira elétrica rotativa Arke sem errar o ponto da carne."},
    {"name": "Apê Pequeno", "username": "meuape.302", "likes": 27800, "comments": 54, "shares": 370, "title": "Fazendo churrasco de domingo dentro da sala com a Arke Vitta Smart!"},
    {"name": "Carne & Brasa", "username": "carneebrasaoficial", "likes": 34600, "comments": 71, "shares": 520, "title": "Assando costela bovina desmanchando na churrasqueira rotativa. Espetacular!"},
    {"name": "Receitas Rápidas", "username": "receitasdodia.oficial", "likes": 18900, "comments": 33, "shares": 210, "title": "Linguiça toscana e asinha de frango crocante por fora e macia por dentro."},
    {"name": "Guia de Compras", "username": "guiadeachadosbr", "likes": 14200, "comments": 25, "shares": 140, "title": "Review sincero da churrasqueira Arke 5 espetos: vale a pena na Black Friday?"},
    {"name": "Chef em Casa", "username": "chefemcasa_br", "likes": 29100, "comments": 58, "shares": 410, "title": "Segredo do queijo coalho dourado por igual com o motor rotativo silencioso."},
    {"name": "Casal no Apê", "username": "casal.apezinho", "likes": 23500, "comments": 47, "shares": 330, "title": "Testamos a churrasqueira elétrica no nosso apê de 45m² e foi sucesso total!"},
    {"name": "Bbq & Cia", "username": "bbqeciaoficial", "likes": 38000, "comments": 76, "shares": 640, "title": "Churrasco de feriado com os amigos: capacidade para alimentar todo mundo."},
    {"name": "Achadinhos Top", "username": "achadinhosvirais.br", "likes": 17300, "comments": 31, "shares": 195, "title": "O produto que todo morador de apartamento precisa ter na cozinha."},
    {"name": "Varanda Gourmet", "username": "varandagourmet.decor", "likes": 20800, "comments": 39, "shares": 280, "title": "Encaixou perfeitamente na nossa bancada da varanda, acabamento premium em inox."},
    {"name": "Sabor de Casa", "username": "saborde.casa", "likes": 16900, "comments": 28, "shares": 170, "title": "Almoço de domingo garantido sem sujeira de carvão e sem cinzas."},
    {"name": "Review Sem Filtro", "username": "reviewsemfiltro.br", "likes": 26400, "comments": 51, "shares": 360, "title": "Consumo de energia da churrasqueira elétrica: gasta muito? Fizemos as contas!"},
    {"name": "Espeto de Ouro", "username": "espetodeouro_sp", "likes": 32100, "comments": 65, "shares": 480, "title": "Fraldinha na mostarda assando no espeto giratório da Arke. Ficou surreal!"},
    {"name": "Vida Prática", "username": "vidapratica.dicas", "likes": 19700, "comments": 36, "shares": 230, "title": "Limpeza da gaveta de gordura em 2 minutos: água e detergente neutro e pronto."},
    {"name": "Papo de Churrasco", "username": "papodechurrasco_br", "likes": 28300, "comments": 56, "shares": 390, "title": "Aprovada com louvor! O vidro curvo facilita muito acompanhar o ponto."},
    {"name": "Casa & Conforto", "username": "casaeconforto_oficial", "likes": 15400, "comments": 26, "shares": 160, "title": "Segurança total com certificado INMETRO e cabos de madeira que não esquentam."},
    {"name": "Churrasqueando", "username": "churrasqueando_total", "likes": 36700, "comments": 73, "shares": 590, "title": "Cupim assado lentamente no espeto giratório: maciez extrema!"},
    {"name": "Achados do TikTok", "username": "achados.tiktokbrasil", "likes": 41200, "comments": 84, "shares": 720, "title": "A churrasqueira elétrica mais vendida do Brasil na promoção da Stone Shop!"}
]

# Gera os 30 itens
items_code = []
for i, c in enumerate(creators_data):
    catbox_url = "https://files.catbox.moe/p7r4vc.mp4" if (i % 2 == 0) else "https://files.catbox.moe/ac2l43.mp4"
    items_code.append(f"""  {{
    "name": "{c['name']}",
    "username": "{c['username']}",
    "avatar": "../img/reviews-avatars/review-user-{(i % 12) + 1}.jpg",
    "poster": "../img/review-14-c{(i % 4) + 1}-1.jpg",
    "video": "{catbox_url}",
    "localVideo": "../videosprodutos/video-produto-14.mp4",
    "startTime": 0.2,
    "likes": {c['likes']},
    "comments": {c['comments']},
    "shares": {c['shares']},
    "saves": {c['likes'] // 10},
    "title": "{c['title']}"
  }}""")

new_dataset = "const CREATORS_CHURRASQUEIRA_ARKE_14 = [\n" + ",\n".join(items_code) + "\n];"

# Substitui em js/videos-criadores.js
pattern = r'const CREATORS_CHURRASQUEIRA_ARKE_14\s*=\s*\[.*?\];'
js_updated = re.sub(pattern, new_dataset, js_content, flags=re.DOTALL)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(js_updated)

print("Dataset CREATORS_CHURRASQUEIRA_ARKE_14 atualizado com sucesso!")
