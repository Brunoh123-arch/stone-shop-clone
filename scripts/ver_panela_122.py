with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

idx = text.find('PANELA_122_VIDEOS_MAP')
if idx != -1:
    print(text[idx:idx+1500])
