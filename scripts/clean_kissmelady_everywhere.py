import os
import re

old_full = "KISSMELADY 015 010 8110 com cinto preto calça mom jeans feminina moda novo  lisa sem rascada"
old_single_space = "KISSMELADY 015 010 8110 com cinto preto calça mom jeans feminina moda novo lisa sem rascada"
new_title = "Calça Mom Jeans Feminina com Cinto Preto KISSMELADY Cintura Alta Modeladora"

old_alt_prefix = "KISSMELADY 015 010 8110 com cinto preto"
new_alt_prefix = "Calça Mom Jeans Feminina com Cinto Preto KISSMELADY"

targets = [
    "index.html",
    "real.html",
    "stone.html",
    "api/stone_content.js",
    "api/_lib/stone_content.js",
    "api/_lib/versions_content.js",
    "js/catalogo.js",
    "pages/produto-104.html",
    "pages/produto-17.html",
    "pages/produto-63.html",
    "pages/produto-87.html",
    "versions/v1.html",
    "versions/v2.html",
    "versions/v3.html",
    "versions/v4.html",
    "versions/v5.html"
]

for t in targets:
    if not os.path.exists(t):
        continue
    with open(t, 'r', encoding='utf-8') as f:
        content = f.read()

    changed = False
    if old_full in content:
        content = content.replace(old_full, new_title)
        changed = True
    if old_single_space in content:
        content = content.replace(old_single_space, new_title)
        changed = True
    if old_alt_prefix in content:
        content = content.replace(old_alt_prefix, new_alt_prefix)
        changed = True

    if changed:
        with open(t, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {t}")

print("Cleaned KISSMELADY everywhere!")
