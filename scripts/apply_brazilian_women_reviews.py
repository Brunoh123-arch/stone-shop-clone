import glob, re, os
from bs4 import BeautifulSoup

FEMALE_PRODUCTS = [28, 38, 39, 45, 87, 88, 103, 104, 106, 108, 109]

# 80 Avatares de Brasileiras Reais do TikTok
BRAZILIAN_WOMEN_AVATARS = [f"../img/reviews-avatars/mulheres_brasil/mulher_{i}.jpg" for i in range(1, 81)]

# Pool de Nomes Femininos Brasileiros Autênticos Mascarados Padrão TikTok Shop
BRAZILIAN_FEMALE_NAMES = [
    "J**a S**a", "C**a M**o", "L**a R**s", "M**a F**a", "B**a N**s",
    "G**a P**o", "F**a C**o", "P**a S**s", "V**a L**a", "R**a G**s",
    "A**a N**a", "I**a S**a", "B**z L**a", "N**a R**o", "T**a L**s",
    "D**a F**s", "E**a S**a", "S**a M**s", "K**a L**a", "L**u D**e",
    "M**e C**o", "A**e M**s", "J**e F**s", "C**e B**a", "V**a F**a",
    "I**s B**a", "P**a R**s", "B**a M**a", "T**a N**s", "R**e S**s"
]

print(f"Aplicando 80 avatares de brasileiras reais do TikTok em {len(FEMALE_PRODUCTS)} produtos femininos...")

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

    # Offset para variação entre produtos
    offset = (pid * 5) % len(BRAZILIAN_WOMEN_AVATARS)
    name_offset = (pid * 3) % len(BRAZILIAN_FEMALE_NAMES)

    for idx, card in enumerate(reviews):
        avatar_url = BRAZILIAN_WOMEN_AVATARS[(offset + idx) % len(BRAZILIAN_WOMEN_AVATARS)]
        masked_name = BRAZILIAN_FEMALE_NAMES[(name_offset + idx) % len(BRAZILIAN_FEMALE_NAMES)]

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

    with open(fpath, 'w', encoding='utf-8') as fp:
        fp.write(str(soup))

    print(f"P{pid} ({fpath}): {len(reviews)} avaliações atualizadas com brasileiras reais do TikTok!")
