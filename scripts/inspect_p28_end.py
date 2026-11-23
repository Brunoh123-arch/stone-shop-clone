# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Ultimas 60 linhas de pages/produto-28.html:")
for l in lines[-60:]:
    print(l.rstrip())
