with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('reviews-section')
if idx == -1:
    idx = c.find('Avaliações dos clientes')
print(c[idx:idx+2500])
