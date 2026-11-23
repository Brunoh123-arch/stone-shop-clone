import glob, re, os
from bs4 import BeautifulSoup

# Produtos estritamente femininos
FEMALE_PRODUCTS = [28, 38, 39, 45, 87, 88, 103, 104, 106, 108, 109]

# 110 Avatares Femininos Reais do TikTok (números pares)
FEMALE_AVATARS = [f"../img/reviews-avatars/tiktok_real/tt_avatar_{i}.jpg" for i in range(2, 221, 2)]

# Pool amplo de Nomes Femininos Brasileiros Mascarados Padrão TikTok Shop
FEMALE_NAMES = [
    "M**a S**a", "V**a L**a", "C**a P**o", "J**e F**s", "A**a N**a",
    "L**a M**s", "F**a B**a", "P**a S**s", "B**z L**a", "E**a S**a",
    "I**a S**a", "S**a M**s", "B**a N**s", "L**u D**e", "B**a C**o",
    "E**e S**s", "K**a L**a", "V**a F**a", "N**a R**o", "A**e M**s",
    "C**e B**a", "T**a L**s", "R**a G**s", "G**a M**t", "M**e C**o",
    "L**s P**a", "A**a C**s", "J**a M**a", "F**a C**o", "P**a R**s",
    "B**a M**a", "T**a N**s", "V**a R**o", "C**a M**s", "D**a F**s",
    "I**s B**a", "L**a R**s", "M**a F**a", "N**a P**o", "R**e S**s"
]

print(f"Iniciando expurgo absoluto de avatares/nomes masculinos em {len(FEMALE_PRODUCTS)} produtos femininos...")

for pid in FEMALE_PRODUCTS:
    fpath = f"pages/produto-{pid}.html"
    if not os.path.exists(fpath):
        continue

    with open(fpath, 'r', encoding='utf-8') as fp:
        content = fp.read()

    soup = BeautifulSoup(content, 'html.parser')
    reviews = soup.select('.review-card')
    if not reviews:
        print(f"P{pid}: Nenhuma review encontrada.")
        continue

    # Gerador único de avatares femininos para este produto
    offset = (pid * 7) % len(FEMALE_AVATARS)
    name_offset = (pid * 11) % len(FEMALE_NAMES)

    count_replaced = 0

    for idx, card in enumerate(reviews):
        # 100% dos cards recebem dados exclusivamente femininos
        avatar_url = FEMALE_AVATARS[(offset + idx) % len(FEMALE_AVATARS)]
        masked_name = FEMALE_NAMES[(name_offset + idx) % len(FEMALE_NAMES)]

        # Atualiza atributos do card
        card['data-author-name'] = masked_name
        card['data-author-avatar'] = avatar_url

        # Atualiza elementos visuais internos
        name_el = card.select_one('.review-user-name')
        if name_el:
            name_el.string = masked_name

        img_el = card.select_one('.review-avatar img')
        if img_el:
            img_el['src'] = avatar_url
            img_el['alt'] = masked_name

        count_replaced += 1

    with open(fpath, 'w', encoding='utf-8') as fp:
        fp.write(str(soup))

    print(f"P{pid} ({fpath}): {count_replaced} avaliações 100% convertidas para mulheres reais.")

# Agora garantir que no js/videos-criadores.js o produto 28 aponte para criadoras femininas
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    cjs = f.read()

# P28 usava CREATORS_LIVRO_124. Mudar para POOL_MODA_FEMININA ou CREATORS_BODY_106
cjs_new = cjs.replace('case 28:\n        activeDataset = CREATORS_LIVRO_124;', 'case 28:\n        activeDataset = buildNichePool(CREATORS_BODY_106, POOL_MODA_FEMININA);')
with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(cjs_new)

print("\njs/videos-criadores.js P28 atualizado para criadoras femininas!")
