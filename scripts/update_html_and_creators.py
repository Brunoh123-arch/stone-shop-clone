import re

# 1. ATUALIZAR js/videos-criadores.js
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    vjs = f.read()

# Definir novos blocos para Sabala 31 e POCO X7 Pro 36
new_sabala_block = """const SABALA_31_VIDEOS_MAP = [
  {
    name: "Elvyn | Canal do Pincei",
    username: "issopresta",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_14.jpg",
    poster: "../img/posters-sabala/poster_1.jpg",
    video: "https://files.catbox.moe/1ig8lo.mp4",
    desc: "Na minha humilde opinião, a Sabala DR-909 é o melhor custo benefício hoje! 39.000mAh de bateria, 200W RMS e graves que batem pesado! 🔊🔥 #sabala #dr909 #caixadesom #sompesado"
  },
  {
    name: "Mundo Tec Smartphones",
    username: "mundotec.smartphone",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_22.jpg",
    poster: "../img/posters-sabala/poster_3.jpg",
    video: "https://files.catbox.moe/v36v5l.mp4",
    desc: "A Caixa Sabala DR-909 enterra qualquer concorrente por metade do preço! Acabamento impecável e conexão TWS estéreo! ⚡🎶 #sabaladr909 #techaudio #somdequalidade"
  },
  {
    name: "Sabala Oficial Brasil",
    username: "sabala.brazil",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_35.jpg",
    poster: "../img/posters-sabala/poster_2.jpg",
    video: "https://files.catbox.moe/t42yc4.mp4",
    desc: "Sabala DR-909 lançada! Bateria ultralonga de até 36h, certificação IPX6 e 200W reais com radiadores passivos! 🚀🔊 #sabala #dr909 #unboxing #lancamento"
  },
  {
    name: "Gaspar Recomenda",
    username: "gaspar_recomenda",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_44.jpg",
    poster: "../img/posters-sabala/poster_4.jpg",
    video: "https://files.catbox.moe/47sfa7.mp4",
    desc: "Caixa de Som Bluetooth SABALA DR-909 é um monstro! Coloquei no volume máximo no churrasco e não distorceu nada! 🥩🎉 #sabala #somdechurrasco #audiophile"
  },
  {
    name: "Rosleon Reviews",
    username: "rosleonoficial",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_58.jpg",
    poster: "../img/posters-sabala/poster_5.jpg",
    video: "https://files.catbox.moe/9nh7z7.mp4",
    desc: "Testando a Sabala DR-909 de 200W no limite! Som limpo, graves potentes e o dobro de potência no modo TWS! 💥🎵 #sabaladr909 #reviewcompleto #testedeaudio"
  }
];
const CREATORS_SABALA_31 = SABALA_31_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25400 + i * 2900, commentsCount: 310 + i * 45, sharesCount: 110 + i * 22, savesCount: 2150 + i * 240, description: b.desc }));"""

new_poco_block = """const POCO_X7_PRO_36_VIDEOS_MAP = [
  {
    name: "Bloom Unboxings",
    username: "bloomfofa",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_82.jpg",
    poster: "../img/posters-poco/poster_4.jpg",
    video: "https://files.catbox.moe/vyssbh.mp4",
    desc: "Unboxing completo do meu POCO X7 Pro Amarelo! A traseira em couro vegano é perfeita e muito macia! Apaixonada! 💛📱 #pocox7pro #unboxing #xiaomi #celularnovo"
  },
  {
    name: "Cell Ofertas Brasil",
    username: "cellofertas.brasi",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_91.jpg",
    poster: "../img/posters-poco/poster_3.jpg",
    video: "https://files.catbox.moe/s313zy.mp4",
    desc: "Poco X7 Pro 512GB 12GB RAM: O monstro da Xiaomi com Dimensity 8400 Ultra! Roda tudo no ultra a 120fps liso! 🚀🎮 #pocox7pro #xiaomibrasil #gamer #techtok"
  },
  {
    name: "DBA Tech Reviews",
    username: "dba_iphone",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_77.jpg",
    poster: "../img/posters-poco/poster_2.jpg",
    video: "https://files.catbox.moe/6isg2y.mp4",
    desc: "Olha tudo o que vem na caixa do POCO X7 Pro! Carregador turbo de 90W original, capinha fosca e tela CrystalRes 1.5K! 📦✨ #pocox7pro #unboxingbrasil #tecnologia"
  },
  {
    name: "Tuk Imperial",
    username: "tukemperial",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_65.jpg",
    poster: "../img/posters-poco/poster_5.jpg",
    video: "https://files.catbox.moe/2txroy.mp4",
    desc: "POCO X7 PRO é o verdadeiro REI do custo-benefício em 2026! Câmera Sony de 50MP com OIS e bateria gigante de 6000mAh! 🔥📱 #pocox7pro #xiaomi #review"
  },
  {
    name: "Kevin Tech & Mobile",
    username: "kevinbreezetv",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_104.jpg",
    poster: "../img/posters-poco/poster_1.jpg",
    video: "https://files.catbox.moe/1ig8lo.mp4",
    desc: "Poco X7 Pro Unboxing & Hands-on! Design premium, bordas ultrafinas e resposta tátil sensacional! ⚡🙌 #pocox7pro #unboxing #techtokbrasil"
  }
];
const CREATORS_POCO_X7_PRO_36 = POCO_X7_PRO_36_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 29800 + i * 3200, commentsCount: 380 + i * 52, sharesCount: 140 + i * 28, savesCount: 2600 + i * 290, description: b.desc }));"""

# Substituir blocos antigos em js/videos-criadores.js
vjs = re.sub(r'const\s+SABALA_31_VIDEOS_MAP\s*=\s*\[.*?\];\s*const\s+CREATORS_SABALA_31\s*=\s*[^;]+;', new_sabala_block, vjs, flags=re.DOTALL)
vjs = re.sub(r'const\s+POCO_X7_PRO_36_VIDEOS_MAP\s*=\s*\[.*?\];\s*const\s+CREATORS_POCO_X7_PRO_36\s*=\s*[^;]+;', new_poco_block, vjs, flags=re.DOTALL)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(vjs)

print("js/videos-criadores.js atualizado com criadores e posters oficiais!")

# 2. ATUALIZAR pages/produto-31.html (Sabala DR-909)
with open('pages/produto-31.html', 'r', encoding='utf-8') as f:
    p31 = f.read()

# Substituir miniaturas da variação para usar slide_1.jpg em vez de thumbnail fake
p31 = re.sub(r'<div class="sku-thumb"[^>]*>.*?</div>', '<div class="sku-thumb"><img src="../img/produtos/p31/slide_1.jpg" alt="Sabala DR-909 Preto"></div>', p31)
p31 = re.sub(r'src="[^"]*thumb_p31[^"]*"', 'src="../img/produtos/p31/slide_1.jpg"', p31)
p31 = re.sub(r'src="[^"]*decalque[^"]*"', 'src="../img/produtos/p31/slide_1.jpg"', p31)

# Atualizar as fotos de unboxing nas primeiras avaliações
unboxing_sabala_html = """<div class="review-photos"><img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/sabala_31/unboxing_1.jpg"/> <img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/sabala_31/unboxing_2.jpg"/></div>"""
unboxing_sabala_html_2 = """<div class="review-photos"><img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/sabala_31/unboxing_3.jpg"/> <img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/sabala_31/unboxing_4.jpg"/></div>"""
unboxing_sabala_html_3 = """<div class="review-photos"><img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/sabala_31/unboxing_5.jpg"/></div>"""

# Substituir blocos de review-photos
photos_matches = list(re.finditer(r'<div class="review-photos">.*?</div>', p31, re.DOTALL))
if len(photos_matches) >= 3:
    p31 = p31[:photos_matches[0].start()] + unboxing_sabala_html + p31[photos_matches[0].end():]
    # recalcular matches
    photos_matches = list(re.finditer(r'<div class="review-photos">.*?</div>', p31, re.DOTALL))
    p31 = p31[:photos_matches[1].start()] + unboxing_sabala_html_2 + p31[photos_matches[1].end():]
    photos_matches = list(re.finditer(r'<div class="review-photos">.*?</div>', p31, re.DOTALL))
    p31 = p31[:photos_matches[2].start()] + unboxing_sabala_html_3 + p31[photos_matches[2].end():]

# Trocar avatares para o pool tiktok_real verificado
avatars_sabala = [
    ("../img/reviews-avatars/tiktok_real/tt_avatar_41.jpg", "M**a S**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_42.jpg", "C**a P**o"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_43.jpg", "R**o S**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_44.jpg", "F**e L**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_45.jpg", "J**o B**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_46.jpg", "L**a M**s"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_47.jpg", "G**l S**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_48.jpg", "A**a R**s"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_49.jpg", "D**o C**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_50.jpg", "P**o N**o"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg", "V**r M**o"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_52.jpg", "T**o S**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_53.jpg", "B**a F**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_54.jpg", "E**n P**o"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_55.jpg", "K**n S**a"),
]

# Atualizar cada review-card em p31
cards = list(re.finditer(r'<div class="review-card"([^>]*)>', p31))
for idx, m in enumerate(cards):
    if idx < len(avatars_sabala):
        av_path, av_name = avatars_sabala[idx]
        old_tag = m.group(0)
        new_tag = re.sub(r'data-author-avatar="[^"]*"', f'data-author-avatar="{av_path}"', old_tag)
        new_tag = re.sub(r'data-author-name="[^"]*"', f'data-author-name="{av_name}"', new_tag)
        p31 = p31.replace(old_tag, new_tag, 1)

# Atualizar também as tags <img> de review-avatar internas
p31 = re.sub(r'<div class="review-avatar">\s*<img [^>]*src="[^"]*"', lambda m: f'<div class="review-avatar"><img src="{avatars_sabala[0][0]}"', p31, count=1)

with open('pages/produto-31.html', 'w', encoding='utf-8') as f:
    f.write(p31)

print("pages/produto-31.html atualizado com unboxing real e avatares limpos!")

# 3. ATUALIZAR pages/produto-36.html (POCO X7 Pro)
with open('pages/produto-36.html', 'r', encoding='utf-8') as f:
    p36 = f.read()

# Substituir miniaturas da variação para usar thumb_amarelo.jpg
p36 = re.sub(r'<div class="sku-thumb"[^>]*>.*?</div>', '<div class="sku-thumb"><img src="../img/produtos/p36/thumb_amarelo.jpg" alt="POCO X7 Pro Amarelo"></div>', p36)
p36 = re.sub(r'src="[^"]*thumb_p36[^"]*"', 'src="../img/produtos/p36/thumb_amarelo.jpg"', p36)
p36 = re.sub(r'src="[^"]*decalque[^"]*"', 'src="../img/produtos/p36/thumb_amarelo.jpg"', p36)

# Atualizar as fotos de unboxing nas primeiras avaliações
unboxing_poco_html = """<div class="review-photos"><img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/poco_36/unboxing_1.jpg"/> <img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/poco_36/unboxing_2.jpg"/></div>"""
unboxing_poco_html_2 = """<div class="review-photos"><img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/poco_36/unboxing_3.jpg"/> <img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/poco_36/unboxing_4.jpg"/></div>"""
unboxing_poco_html_3 = """<div class="review-photos"><img alt="Foto real da avaliação unboxing" class="review-photo" decoding="async" loading="lazy" src="../img/reviews-unboxing/poco_36/unboxing_5.jpg"/></div>"""

photos_matches = list(re.finditer(r'<div class="review-photos">.*?</div>', p36, re.DOTALL))
if len(photos_matches) >= 3:
    p36 = p36[:photos_matches[0].start()] + unboxing_poco_html + p36[photos_matches[0].end():]
    photos_matches = list(re.finditer(r'<div class="review-photos">.*?</div>', p36, re.DOTALL))
    p36 = p36[:photos_matches[1].start()] + unboxing_poco_html_2 + p36[photos_matches[1].end():]
    photos_matches = list(re.finditer(r'<div class="review-photos">.*?</div>', p36, re.DOTALL))
    p36 = p36[:photos_matches[2].start()] + unboxing_poco_html_3 + p36[photos_matches[2].end():]

# Trocar avatares para o pool tiktok_real verificado (sem nenhum logo como "Mimo...")
avatars_poco = [
    ("../img/reviews-avatars/tiktok_real/tt_avatar_71.jpg", "M**a S**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_72.jpg", "C**a P**o"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_73.jpg", "R**o S**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_74.jpg", "F**e L**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_75.jpg", "J**o B**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_76.jpg", "L**a M**s"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_77.jpg", "G**l S**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_78.jpg", "A**a R**s"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_79.jpg", "D**o C**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_80.jpg", "P**o N**o"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_81.jpg", "V**r M**o"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_82.jpg", "T**o S**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_83.jpg", "B**a F**a"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_84.jpg", "E**n P**o"),
    ("../img/reviews-avatars/tiktok_real/tt_avatar_85.jpg", "K**n S**a"),
]

cards = list(re.finditer(r'<div class="review-card"([^>]*)>', p36))
for idx, m in enumerate(cards):
    if idx < len(avatars_poco):
        av_path, av_name = avatars_poco[idx]
        old_tag = m.group(0)
        new_tag = re.sub(r'data-author-avatar="[^"]*"', f'data-author-avatar="{av_path}"', old_tag)
        new_tag = re.sub(r'data-author-name="[^"]*"', f'data-author-name="{av_name}"', new_tag)
        p36 = p36.replace(old_tag, new_tag, 1)

with open('pages/produto-36.html', 'w', encoding='utf-8') as f:
    f.write(p36)

print("pages/produto-36.html atualizado com unboxing real e avatares limpos!")
