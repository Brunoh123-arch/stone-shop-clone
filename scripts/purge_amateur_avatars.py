import shutil
import os
from PIL import Image

# 1. Replace creator avatars with real people
avatars_map = {
    'img/avatar-creator-14-1.jpg': 'img/reviews-avatars/review-user-104-c12.jpg', # real blonde girl
    'img/avatar-creator-14-2.jpg': 'img/reviews-avatars/review-user-104-c7.jpg',  # real brunette girl
    'img/avatar-creator-14-3.jpg': 'img/reviews-avatars/review-user-104-c11.jpg', # real couple/man
    'img/avatar-creator-14-4.jpg': 'img/reviews-avatars/review-user-104-c10.jpg', # real lady
    'img/avatar-creator-14-5.jpg': 'img/reviews-avatars/review-user-6.jpg',       # real girl
}

for dest, src in avatars_map.items():
    if os.path.exists(src):
        im = Image.open(src)
        im.resize((100, 100), Image.Resampling.LANCZOS).save(dest, quality=90)
        print(f"Replaced {dest} with human avatar from {src}")

# 2. Update reviews in pages/produto-14.html to use 100% human avatars
with open('pages/produto-14.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace review avatars in produto-14.html
html = html.replace('review-user-104-vanessa.jpg', 'review-user-104-c7.jpg')
html = html.replace('review-user-105-c1.jpg', 'review-user-104-c10.jpg')
html = html.replace('review-user-105-c3.jpg', 'review-user-104-c11.jpg')
html = html.replace('review-user-104-renata.jpg', 'review-user-104-c12.jpg')

with open('pages/produto-14.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated pages/produto-14.html reviews with human avatars")

# 3. Update js/videos-criadores.js to replace corporate/cartoon names with real creators
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Replace "Rosita21" with "Camila Rocha"
js_code = js_code.replace('"name": "Rosita21"', '"name": "Camila Rocha"')
js_code = js_code.replace('"username": "rosegodoi.finds"', '"username": "camilaoch.ape"')

# Replace "Escolha Certa" with "Marcos Silva"
js_code = js_code.replace('"name": "Escolha Certa"', '"name": "Marcos Churras"')
js_code = js_code.replace('"username": "_escolhas_certas"', '"username": "marcoschurras_ape"')

# Replace "Cybelar" with "Larissa & Rodrigo"
js_code = js_code.replace('"name": "Cybelar"', '"name": "Larissa & Rodrigo"')
js_code = js_code.replace('"username": "lojacybelararturnogueira"', '"username": "larissarodrigo_home"')

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
print("Updated js/videos-criadores.js with human creator names")
