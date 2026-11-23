with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('reviews-summary')
print(c[idx:idx+4000])
