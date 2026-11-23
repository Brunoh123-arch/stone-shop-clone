# -*- coding: utf-8 -*-
with open('js/app.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function openSizeGuideModal')
if idx != -1:
    print(text[idx:idx+1500])
