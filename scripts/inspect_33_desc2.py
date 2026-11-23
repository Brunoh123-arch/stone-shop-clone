with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('product-video-block')
if idx != -1:
    print(html[idx:idx+2000])
