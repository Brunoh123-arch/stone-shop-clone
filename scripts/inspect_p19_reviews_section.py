with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('Avaliações dos clientes')
print("Index de Avaliações dos clientes:", idx)
if idx != -1:
    print(c[idx:idx+3000])
