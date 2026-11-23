with open('pages/produto-104.html', encoding='utf-8') as f:
    text = f.read()

idx = text.find('class="review-card"')
if idx != -1:
    print(text[idx:idx+2500])
