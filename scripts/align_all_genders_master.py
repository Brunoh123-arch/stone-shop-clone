import glob
import re
import os
from bs4 import BeautifulSoup

TOTAL_AVATARS = len([f for f in os.listdir('img/reviews-avatars/tiktok_real') if f.endswith('.jpg')])
assert TOTAL_AVATARS == 220, f"Esperava 220 avatares, encontrou {TOTAL_AVATARS}"

# Classificação determinística e balanceada dos 220 avatares
# Pares = Feminino (110 avatares), Ímpares = Masculino (110 avatares)
FEMALE_AVATARS = [f"../img/reviews-avatars/tiktok_real/tt_avatar_{i}.jpg" for i in range(2, 221, 2)]
MALE_AVATARS = [f"../img/reviews-avatars/tiktok_real/tt_avatar_{i}.jpg" for i in range(1, 221, 2)]

# Pool de Nomes Claramente Femininos
FEMALE_NAMES = [
    "M**a S**a", "V**a L**a", "C**a P**o", "J**e F**s", "A**a N**a",
    "L**a M**s", "F**a B**a", "P**a S**s", "B**z L**a", "E**a S**a",
    "I**a S**a", "S**a M**s", "B**a N**s", "L**u D**e", "B**a C**o",
    "E**e S**s", "K**a L**a", "V**a F**a", "N**a R**o", "A**e M**s",
    "C**e B**a", "T**a L**s"
]

# Pool de Nomes Claramente Masculinos
MALE_NAMES = [
    "D**o M**s", "R**o S**a", "T**o A**o", "G**a R**s", "H**o C**a",
    "K**s M**o", "W**r P**a", "Y**a C**o", "V**r H**o", "L**s F**a",
    "D**a G**s", "M**o B**o", "J**o P**o", "C**s E**o", "R**a G**s",
    "T**s A**s", "A**r C**s", "F**e M**a", "G**o B**o", "R**n O**a",
    "M**s P**a", "C**o L**a", "L**z V**a", "R**l M**t", "S**o F**o",
    "T**g R**s", "J**n S**a", "P**o H**e", "D**e A**s", "M**e T**o",
    "G**l S**a", "L**e C**o", "F**o P**a", "I**r D**s", "H**a N**o",
    "M**l G**o", "Y**r S**a"
]

DATES_POOL = [
    "15/02", "14/02", "12/02", "11/02", "10/02", "08/02", "07/02", "05/02",
    "04/02", "02/02", "01/02", "29/01", "28/01", "26/01", "25/01", "23/01",
    "21/01", "20/01", "18/01", "17/01", "15/01", "13/01", "12/01", "10/01",
    "08/01", "06/01", "05/01", "03/01", "02/01"
]

files = sorted(glob.glob('pages/produto-*.html'))
print(f"Alinhando gênero em todas as reviews de {len(files)} páginas HTML...")

total_updated = 0

for file_path in files:
    m = re.search(r'produto-(\d+)\.html', file_path)
    if not m:
        continue
    pid = int(m.group(1))

    with open(file_path, 'r', encoding='utf-8') as fp:
        content = fp.read()

    soup = BeautifulSoup(content, 'html.parser')
    reviews = soup.select('.review-card')
    if not reviews:
        continue

    f_offset = (pid * 13) % len(FEMALE_AVATARS)
    m_offset = (pid * 17) % len(MALE_AVATARS)

    f_idx = 0
    m_idx = 0

    for idx, card in enumerate(reviews):
        is_female = (idx % 2 == 0)

        if is_female:
            masked_name = FEMALE_NAMES[(f_offset + f_idx) % len(FEMALE_NAMES)]
            avatar_url = FEMALE_AVATARS[(f_offset + f_idx) % len(FEMALE_AVATARS)]
            f_idx += 1
        else:
            masked_name = MALE_NAMES[(m_offset + m_idx) % len(MALE_NAMES)]
            avatar_url = MALE_AVATARS[(m_offset + m_idx) % len(MALE_AVATARS)]
            m_idx += 1

        date_str = DATES_POOL[idx % len(DATES_POOL)]

        # Atualiza atributos do card
        card['data-author-name'] = masked_name
        card['data-author-avatar'] = avatar_url
        card['data-author-date'] = date_str

        # Atualiza elementos visuais internos
        name_el = card.select_one('.review-user-name')
        if name_el:
            name_el.string = masked_name

        img_el = card.select_one('.review-avatar img')
        if img_el:
            img_el['src'] = avatar_url
            img_el['alt'] = masked_name

        date_el = card.select_one('.review-date')
        if date_el and date_el.string:
            parts = date_el.string.split('·')
            var_part = parts[1].strip() if len(parts) > 1 else ''
            date_el.string = f"{date_str} · {var_part}" if var_part else date_str

        total_updated += 1

    with open(file_path, 'w', encoding='utf-8') as fp:
        fp.write(str(soup))

print(f"Sucesso Total: {total_updated} avaliações atualizadas em {len(files)} páginas!")
