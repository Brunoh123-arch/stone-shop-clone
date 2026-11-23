with open('pages/produto-54.html', 'r', encoding='utf-8') as f:
    c54 = f.read()

c54_new = c54.replace('https://files.catbox.moe/3rtr42.mp4', 'https://files.catbox.moe/0qd90i.mp4')
with open('pages/produto-54.html', 'w', encoding='utf-8') as f:
    f.write(c54_new)
print('P54 atualizado para 0qd90i.mp4!')

with open('pages/produto-32.html', 'r', encoding='utf-8') as f:
    c32 = f.read()

c32_new = c32.replace('https://files.catbox.moe/3rtr42.mp4', 'https://files.catbox.moe/iopyod.mp4')
with open('pages/produto-32.html', 'w', encoding='utf-8') as f:
    f.write(c32_new)
print('P32 atualizado para iopyod.mp4!')

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    cjs = f.read()

cjs_new = cjs.replace('case 32:\n        activeDataset = CREATORS_FOGAO_117;', 'case 32:\n        activeDataset = CREATORS_LAVADORA_123;')
with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(cjs_new)
print('js/videos-criadores.js case 32 atualizado para CREATORS_LAVADORA_123!')
