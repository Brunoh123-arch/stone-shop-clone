with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx1 = c.find('class="reviews-list"')
print('idx1:', idx1)
if idx1 != -1:
    print("--- INICIO REVIEWS LIST ---")
    print(c[idx1:idx1+200])

idx_end = c.find('</section>', idx1)
print('idx_end:', idx_end)
if idx_end != -1:
    print("--- FIM REVIEWS LIST ---")
    print(c[idx_end-300:idx_end+50])
