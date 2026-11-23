with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
idx = c.find('tt-product-video')
if idx != -1:
    print("Found tt-product-video at:", idx)
    print(c[max(0, idx-200):min(len(c), idx+600)])
else:
    print("tt-product-video NOT found")
