# -*- coding: utf-8 -*-
html = open('pages/produto-87.html', 'r', encoding='utf-8').read()

idx1 = html.find('class="product-desc"')
if idx1 == -1:
    idx1 = html.find('class="description-text"')
if idx1 == -1:
    idx1 = html.find('class="about-product-section"')

print(html[idx1:idx1+1500])
