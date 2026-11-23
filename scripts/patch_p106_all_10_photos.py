with open('pages/produto-106.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Split by <div class="review-card"
parts = html.split('<div class="review-card"')
print("Total card segments:", len(parts))

extra_cards = [
    {
        "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_102.jpg",
        "name": "a**e l**a",
        "date": "10/11",
        "variation": "Lilás · M",
        "stars": "5",
        "comment": "O body é lindíssimo e chegou super rápido pela Stone Shop, amei minha compra! Vou comprar outras cores.",
        "photo": "../img/review-106-real-5.jpg"
    },
    {
        "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_104.jpg",
        "name": "M**a S.**",
        "date": "08/11",
        "variation": "Bege · G",
        "stars": "5",
        "comment": "Gostei muito, o material é uma malha fria de altíssima qualidade! Modela sem machucar e não enrola nada.",
        "photo": "../img/review-106-real-6.jpg"
    },
    {
        "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_106.jpg",
        "name": "L**a C**a",
        "date": "06/11",
        "variation": "Bege · P",
        "stars": "5",
        "comment": "Está de parabéns a loja... amei demais, super confortável pra ser tamanho P. Veste com perfeição!",
        "photo": "../img/review-106-real-7.jpg"
    },
    {
        "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_108.jpg",
        "name": "G**e M**a",
        "date": "04/11",
        "variation": "Bege · G",
        "stars": "5",
        "comment": "Gente eu tô apaixonada! Modela perfeitamente o corpo, costura reforçada e entrega relâmpago. Recomendo de olhos fechados!",
        "photo": "../img/review-106-real-8.jpg"
    },
    {
        "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_110.jpg",
        "name": "P**a F**a",
        "date": "02/11",
        "variation": "Preto · P",
        "stars": "5",
        "comment": "Gostei muito do body. O tecido é confortável, tem ótima compressão e o fecho embaixo é super prático no dia a dia.",
        "photo": "../img/review-106-real-9.jpg"
    },
    {
        "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_112.jpg",
        "name": "L**a G**s",
        "date": "31/10",
        "variation": "Bege · P",
        "stars": "5",
        "comment": "Ela é perfeita, superou todas as minhas expectativas. Modela perfeitamente a cintura e o tecido é super respirável!",
        "photo": "../img/review-106-real-10.jpg"
    }
]

formatted_cards = []
for c in extra_cards:
    stars_html = "".join([
        '<svg class="star-icon" fill="#ffb800" height="11" viewbox="0 0 24 24" width="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
        for _ in range(5)
    ])
    card_html = f''' data-author-avatar="{c['avatar']}" data-author-comment="{c['comment']}" data-author-date="{c['date']}" data-author-name="{c['name']}" data-author-stars="{c['stars']}" data-author-variation="{c['variation']}">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img alt="{c['name']}" decoding="async" loading="lazy" src="{c['avatar']}"/>
</div>
<div class="review-user-info">
<div class="review-user-name">{c['name']}</div>
<div class="review-user-stars">{stars_html}</div>
<div class="review-date">{c['date']} · {c['variation']}</div>
</div>
</div>
</div>
<p class="review-comment">{c['comment']}</p>
<div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px;">
<img alt="Foto de unboxing real da compradora" class="review-photo" decoding="async" loading="lazy" onclick="openPhotoModal(this.src)" src="{c['photo']}" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 1px solid #f0f0f0;"/>
</div>
</div>
'''
    formatted_cards.append(card_html)

# Replace parts[5] to parts[10]
new_parts = parts[:5] + formatted_cards + parts[11:]
rebuilt = '<div class="review-card"'.join(new_parts)

with open('pages/produto-106.html', 'w', encoding='utf-8') as f:
    f.write(rebuilt)

print("[OK] P106 now has 10 unboxing review cards!")
