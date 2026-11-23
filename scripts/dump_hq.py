import urllib.request
import re

url = 'https://www.hqeletro.com.br/forno-eletrico-hq-48-litros-hq48d-1600w-preto-hq48d-/p'
headers = {'User-Agent': 'Mozilla/5.0'}
html = urllib.request.urlopen(urllib.request.Request(url, headers=headers)).read().decode('utf-8', errors='ignore')

with open('hq_page_dump.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Dump salvo!')
imgs = re.findall(r'https://[^\s"\']+\.(?:jpg|png|webp)', html)
print('Total imgs:', len(imgs))
for i in list(dict.fromkeys(imgs))[:20]:
    print('IMG:', i)
