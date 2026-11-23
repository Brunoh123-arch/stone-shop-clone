import re

file_path = 'pages/produto-104.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r'<div class="size-guide-card-tt">.*?</div>\s*</div>'
new_block = '''<div class="size-guide-img-wrapper" style="width: 100%; border-radius: 8px; overflow: hidden; background: #f8f8fa; display: flex; justify-content: center; border: 1px solid #edf0f2;">
            <img src="../img/guia-tamanhos-104.png" alt="Tabela de Medidas – Calçados" style="width: 100%; max-width: 420px; height: auto; display: block; object-fit: contain;">
          </div>'''

c, count = re.subn(pattern, new_block, c, flags=re.DOTALL)
print(f"Replaced {count} instances.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated produto-104.html with official size guide image!")
