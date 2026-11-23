with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('about-product-section')
print("about-product-section in 33:", idx)

idx2 = html.find('product-video-block')
print("product-video-block in 33:", idx2)
if idx2 != -1:
    print(html[idx2-200:idx2+1000])
