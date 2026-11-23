with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    h104 = f.read()

idx = h104.find('description-text')
if idx != -1:
    print(h104[idx:idx+1500])
