# -*- coding: utf-8 -*-
import re

cat = open('js/catalogo.js', 'r', encoding='utf-8').read()
m = re.search(r'id:\s*["\']?49["\']?[\s\S]*?\n\s*\},?', cat)
if m:
    print(m.group(0))
else:
    print("Not found")
