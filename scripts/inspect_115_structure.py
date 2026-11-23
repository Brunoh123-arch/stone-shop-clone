import re

with open('pages/produto-115.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('about-product-section')
if idx != -1:
    print("Found about-product-section in produto-115.html at index", idx)
    print(html[idx-50:idx+2500])
else:
    print("about-product-section NOT found in produto-115.html")
