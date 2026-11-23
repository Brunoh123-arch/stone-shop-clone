with open('pages/produto-13.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# We want to add photos to cards 6, 7, 8, 9, 10
# In card 6:
# <p class="review-comment">Melhor aquisição pro verão da criançada. Cabe duas crianças e dois adultos sentados tranquilamente curtindo uma água gelada.</p>
# In card 7, 8, 9, 10, each has <p class="review-comment">...</p></div>

comments_to_patch = [
    ("Melhor aquisição pro verão da criançada. Cabe duas crianças e dois adultos sentados tranquilamente curtindo uma água gelada.", "unboxing_1.jpg"),
    ("A lona é grossa e resistente. Coloquei uma lona embaixo no chão pra proteger e ficou perfeita. Diversão garantida pra família toda!", "unboxing_2.jpg"),
    ("Super recomendo a loja, envio no mesmo dia e produto 100% original com nota fiscal e garantia. Atendimento nota 10.", "unboxing_3.jpg"),
    ("Piscina maravilhosa! Cor azul brilhante muito bonita e tamanho ideal pra quem tem pouco espaço no quintal ou laje.", "unboxing_4.jpg"),
    ("Enche rápido e não gasta tanta água quanto as piscinas gigantes. Dá pra trocar e manter sempre limpinha gastando pouco.", "unboxing_5.jpg")
]

for comment, img in comments_to_patch:
    photo_div = f'<div class="review-photos" style="display: flex; gap: 8px; margin-top: 10px;">\n<img alt="Foto da avaliação" class="review-photo" onclick="window.abrirModalImagem &amp;&amp; window.abrirModalImagem(this.src)" src="../img/reviews-unboxing/piscina_13/{img}" style="width: 80px; height: 80px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 1px solid #eee;"/>\n</div>\n</div>'
    target = f'<p class="review-comment">{comment}</p>\n</div>'
    if target in c:
        c = c.replace(target, f'<p class="review-comment">{comment}</p>\n{photo_div}')
        print(f"[OK] Patched {img}")
    else:
        print(f"[MISS] Could not find: {comment[:30]}")

with open('pages/produto-13.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Done patching P13!")
