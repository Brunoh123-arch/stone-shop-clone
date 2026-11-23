with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('class="review-item"')
if idx == -1:
    idx = c.find('class="review"')
if idx == -1:
    idx = c.find('review-list')
if idx == -1:
    idx = c.find('reviews-list')

print("Idx:", idx)
print(c[idx:idx+2500])
