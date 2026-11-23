with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('PRODUTO_ATUAL')
print(c[idx:idx+1000])
