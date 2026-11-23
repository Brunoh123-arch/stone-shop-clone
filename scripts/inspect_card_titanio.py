with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('256GB Titânio')
print(c[idx-200:idx+300])
