import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

with open('real.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('stone.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('api/stone_content.js', 'w', encoding='utf-8') as f:
    f.write('module.exports = ' + json.dumps(html) + ';\n')

with open('api/_lib/stone_content.js', 'w', encoding='utf-8') as f:
    f.write('module.exports = ' + json.dumps(html) + ';\n')

print('Sincronizados com sucesso: real.html, stone.html, api/stone_content.js, api/_lib/stone_content.js')
