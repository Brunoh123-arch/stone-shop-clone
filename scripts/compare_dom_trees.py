with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    h104 = f.read()

with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    h33 = f.read()

import re

def extract_dom_tree(html):
    # Extract tags in order
    matches = re.findall(r'<(div|section|nav|header|button|h1|h2|h3)[^>]*?(?:class=["\']([^"\']+)["\'])?[^>]*?(?:id=["\']([^"\']+)["\'])?[^>]*?>', html)
    tree = []
    for tag, cls, id_attr in matches:
        cls_main = cls.split()[0] if cls else ''
        tree.append((tag, cls_main, id_attr or ''))
    return tree

t104 = extract_dom_tree(h104)
t33 = extract_dom_tree(h33)

print("Total elements in 104:", len(t104))
print("Total elements in 33:", len(t33))

# Print main blocks of 104
print("\n--- PRINCIPAIS BLOCOS EM 104 ---")
for tag, cls, id_attr in t104:
    if any(k in cls for k in ['section', 'block', 'bar', 'header', 'slider', 'tabs', 'summary', 'details']):
        print(f"<{tag} class='{cls}' id='{id_attr}'>")

print("\n--- PRINCIPAIS BLOCOS EM 33 ---")
for tag, cls, id_attr in t33:
    if any(k in cls for k in ['section', 'block', 'bar', 'header', 'slider', 'tabs', 'summary', 'details']):
        print(f"<{tag} class='{cls}' id='{id_attr}'>")
