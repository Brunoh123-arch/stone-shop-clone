txt = open('pages/produto-118.html', encoding='utf-8').read()
import re
start = txt.find('class="review-card"')
print(txt[start+1000:start+2500])
