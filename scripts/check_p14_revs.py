import re

txt = open('pages/produto-14.html', encoding='utf-8').read()
start = txt.find('review-card')
print(txt[start+1200:start+2000])
