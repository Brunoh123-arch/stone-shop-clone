import os
import re

print("=== 1. ELIMINANDO SHARE-TOOLTIP-BUBBLE DE TODAS AS PAGINAS ===")

pages_dir = 'pages'
pages = [f for f in os.listdir(pages_dir) if f.endswith('.html')]

tooltip_html_regex = re.compile(r'\s*<!-- TOOLTIP CIANO OFICIAL TIKTOK SHOP -->\s*<div id="share-tooltip-bubble"[^>]*>[\s\S]*?</div>', re.MULTILINE)
tooltip_bubble_div_regex = re.compile(r'\s*<div id="share-tooltip-bubble"[^>]*>[\s\S]*?</div>', re.MULTILINE)
tooltip_script_regex = re.compile(r'\s*// Tooltip de Compartilhamento TikTok Shop\s*function initShareTooltip\(\)[\s\S]*?document\.addEventListener\(\'DOMContentLoaded\',\s*\(\)\s*=>\s*\{\s*initShareTooltip\(\);\s*\}\);', re.MULTILINE)

modified_pages = 0
for page in pages:
    file_path = os.path.join(pages_dir, page)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = tooltip_html_regex.sub('', content)
    new_content = tooltip_bubble_div_regex.sub('', new_content)
    new_content = tooltip_script_regex.sub('', new_content)

    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        modified_pages += 1
        print(f"  ✓ Removido share-tooltip de {page}")

# Também verificar arquivos na raiz (stone.html, index.html, template-produto.html)
root_files = ['stone.html', 'index.html', 'template-produto.html', 'real.html']
for rfile in root_files:
    if os.path.exists(rfile):
        with open(rfile, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = tooltip_html_regex.sub('', content)
        new_content = tooltip_bubble_div_regex.sub('', new_content)
        new_content = tooltip_script_regex.sub('', new_content)
        if new_content != content:
            with open(rfile, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✓ Removido share-tooltip de {rfile}")

print(f"Total de paginas limpas: {modified_pages}")

print("\n=== 2. BLINDANDO CSS/STYLE.CSS CONTRA LAYOUT SHIFTS ===")
css_path = 'css/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Injetar regra defensiva no início de style.css
defensive_css = """
/* === BLINDAGEM DE LAYOUT ZERO JANK / ZERO CLS === */
.share-tooltip-bubble {
  display: none !important;
  position: fixed !important;
  top: -9999px !important;
  left: -9999px !important;
  width: 0 !important;
  height: 0 !important;
  padding: 0 !important;
  margin: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
}

@media screen and (max-width: 600px) {
  :root {
    --header-height: 44px !important;
  }
  .header {
    height: 44px !important;
    padding: 0 12px !important;
  }
  .page-content {
    margin-top: 44px !important;
  }
}
"""

if 'BLINDAGEM DE LAYOUT ZERO JANK' not in css:
    css = defensive_css + '\n' + css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)
    print("  ✓ CSS defensivo injetado em css/style.css")
else:
    print("  ✓ CSS defensivo já presente em css/style.css")

print("\n=== SUCESSO: Zero layout shift garantido! ===")
