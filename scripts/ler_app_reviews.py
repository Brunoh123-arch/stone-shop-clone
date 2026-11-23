with open('js/app.js', encoding='utf-8') as f:
    text = f.read()

idx = text.find('review-card-formatted')
if idx != -1:
    print(text[idx-200:idx+2500])
