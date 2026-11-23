with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('class="review-card"')
print(c[idx:idx+2000])
