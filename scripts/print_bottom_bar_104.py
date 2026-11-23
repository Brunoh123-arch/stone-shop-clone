with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('class="bottom-bar"')
if idx != -1:
    print(c[idx-30:idx+2500])
