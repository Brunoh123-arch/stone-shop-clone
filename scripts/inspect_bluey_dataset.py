with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2116, 2178):
    print(f"{i+1}: {lines[i]}", end='')
