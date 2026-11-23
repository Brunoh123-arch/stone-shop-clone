import os
import re

css_path = 'css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

import_font_rule = "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');"

# Remover o import de onde ele estiver atualmente
css_clean = css.replace(import_font_rule, '').strip()

# Colocar o @import na PRIMEIRA LINHA ABSOLUTA
css_final = import_font_rule + '\n\n' + css_clean + '\n'

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css_final)

print("✅ css/style.css: @import de fontes movido para a LINHA 1 ABSOLUTA!")

# 2. Injetar preconnect e link de fontes no <head> de todos os HTMLs para performance bruta
font_head_tags = """  <!-- Google Fonts: Plus Jakarta Sans & Inter (Oficial TikTok Parity) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap">"""

html_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.vercel', 'scripts_archive', 'scratch']):
        continue
    for file in files:
        if file.endswith('.html'):
            html_files.append(os.path.join(root, file))

updated_htmls = 0
for hpath in html_files:
    try:
        with open(hpath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        with open(hpath, 'r', encoding='latin-1') as f:
            content = f.read()

    if 'fonts.googleapis.com' not in content:
        # Inserir logo antes de </head> ou antes de <link rel="stylesheet" href="...style.css
        if '</head>' in content:
            new_content = content.replace('</head>', f"{font_head_tags}\n</head>", 1)
            with open(hpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_htmls += 1

print(f"✅ Preload de fontes injetado no <head> de {updated_htmls} arquivos HTML!")
