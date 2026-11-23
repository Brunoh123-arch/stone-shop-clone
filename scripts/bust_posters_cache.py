import os
import shutil
import re

print("[*] Renomeando posters para quebrar 100% de cache do CDN e mobile...")

posters = [
    ('videosprodutos/posters/poster-produto-111.jpg', 'videosprodutos/posters/poster-produto-111-real1.jpg'),
    ('videosprodutos/posters/poster-produto-111-criadora2.jpg', 'videosprodutos/posters/poster-produto-111-real2.jpg'),
    ('videosprodutos/posters/poster-produto-111-criadora3.jpg', 'videosprodutos/posters/poster-produto-111-real3.jpg'),
    ('videosprodutos/posters/poster-produto-111-criadora4.jpg', 'videosprodutos/posters/poster-produto-111-real4.jpg')
]

for src, dst in posters:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copiado {src} -> {dst}")

# Atualizar js/videos-criadores.js
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace('../videosprodutos/posters/poster-produto-111.jpg', '../videosprodutos/posters/poster-produto-111-real1.jpg')
js = js.replace('../videosprodutos/posters/poster-produto-111-criadora2.jpg', '../videosprodutos/posters/poster-produto-111-real2.jpg')
js = js.replace('../videosprodutos/posters/poster-produto-111-criadora3.jpg', '../videosprodutos/posters/poster-produto-111-real3.jpg')
js = js.replace('../videosprodutos/posters/poster-produto-111-criadora4.jpg', '../videosprodutos/posters/poster-produto-111-real4.jpg')

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("[OK] js/videos-criadores.js atualizado com novos posters!")

# Atualizar pages/produto-111.html
with open('pages/produto-111.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('../videosprodutos/posters/poster-produto-111.jpg', '../videosprodutos/posters/poster-produto-111-real1.jpg')
html = html.replace('../videosprodutos/posters/poster-produto-111-criadora2.jpg', '../videosprodutos/posters/poster-produto-111-real2.jpg')
html = html.replace('../videosprodutos/posters/poster-produto-111-criadora3.jpg', '../videosprodutos/posters/poster-produto-111-real3.jpg')
html = html.replace('../videosprodutos/posters/poster-produto-111-criadora4.jpg', '../videosprodutos/posters/poster-produto-111-real4.jpg')

with open('pages/produto-111.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("[OK] pages/produto-111.html atualizado!")
