# -*- coding: utf-8 -*-
import re

targets = [
    'pages/produto-23.html',
    'pages/produto-53.html',
    'pages/produto-87.html',
    'pages/produto-88.html',
    'pages/produto-94.html'
]

for t in targets:
    content = open(t, 'r', encoding='utf-8').read()
    m = re.search(r'<div[^>]*class=["\'][^"\']*sold[^"\']*["\'][^>]*>[\s\S]*?</div>', content)
    if m:
        print(f"{t}: {m.group(0)}")
    else:
        m2 = re.search(r'0\s+vendidos?', content, re.IGNORECASE)
        if m2:
            start = max(0, m2.start() - 30)
            end = min(len(content), m2.end() + 30)
            print(f"{t} (raw): {content[start:end]}")
