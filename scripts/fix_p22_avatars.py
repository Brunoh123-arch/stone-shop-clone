import re

with open('pages/produto-22.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace any missing avatar paths
c = c.replace('../img/reviews-avatars/review-user-22-c1.jpg', '../img/reviews-avatars/review-user-1.jpg')
c = c.replace('../img/reviews-avatars/review-user-22-c2.jpg', '../img/reviews-avatars/review-user-2.jpg')
c = c.replace('../img/reviews-avatars/review-user-22-c3.jpg', '../img/reviews-avatars/review-user-3.jpg')

with open('pages/produto-22.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Avatares ajustados com sucesso em produto-22.html!")
