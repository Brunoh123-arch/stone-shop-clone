import os
import json
import re

with open('scripts/catbox_videos_map.json', 'r', encoding='utf-8') as f:
    vmap = json.load(f)

pages_dir = 'pages'
updated_pages = []

for f in os.listdir(pages_dir):
    if f.endswith('.html'):
        p = os.path.join(pages_dir, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
            content = fl.read()

        orig = content
        for base, cat_url in vmap.items():
            if cat_url.startswith('https://files.catbox.moe/'):
                # Replace variations in html
                patterns = [
                    f'../videosprodutos/{base}',
                    f'videosprodutos/{base}',
                    f'../img/{base}',
                    f'img/{base}'
                ]
                for pat in patterns:
                    if pat in content:
                        content = content.replace(pat, cat_url)

        if content != orig:
            with open(p, 'w', encoding='utf-8') as fl:
                fl.write(content)
            updated_pages.append(f)

print(f"Total de paginas HTML atualizadas com links Catbox: {len(updated_pages)}")
for pg in updated_pages:
    print(f"  Atualizada: {pg}")
