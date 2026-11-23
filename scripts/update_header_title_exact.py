import re

# Update js/app.js
with open('js/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace any (${total}) in reviews-header-title-text with (...
c = re.sub(
    r'Avalia[çc][ãa]o?e?s? dos clientes\s*\(\$\{total\}\)',
    'Avaliações dos clientes (...',
    c
)
c = re.sub(
    r'`Avalia[çc][ãa]o?e?s? dos clientes\s*\(\$\{total\}\)`',
    '`Avaliações dos clientes (...`',
    c
)
c = re.sub(
    r'AvaliaÃ§Ãµes dos clientes\s*\(\$\{total\}\)',
    'Avaliações dos clientes (...',
    c
)

with open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated js/app.js to use: Avaliações dos clientes (...")

# Update pages/produto-104.html
with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    c104 = f.read()

c104 = re.sub(
    r'Avaliações dos clientes\s*\(\d+\)',
    'Avaliações dos clientes (...',
    c104
)
c104 = re.sub(
    r'AvaliaÃ§Ãµes dos clientes\s*\(\d+\)',
    'Avaliações dos clientes (...',
    c104
)

with open('pages/produto-104.html', 'w', encoding='utf-8') as f:
    f.write(c104)

print("Updated pages/produto-104.html to use: Avaliações dos clientes (...")
