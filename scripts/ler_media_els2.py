with open('js/app.js', encoding='utf-8') as f:
    text = f.read()

idx = text.find('const mediaEls =')
if idx != -1:
    print(text[idx+1800:idx+3500])
