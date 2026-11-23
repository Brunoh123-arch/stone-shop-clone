with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

count = 0
for i in range(365, 800):
    if i < len(lines):
        if 'name:' in lines[i]:
            count += 1
        if '];' in lines[i] and count > 0:
            print(f"Total de criadoras em ESCOVA_108: {count} na linha {i+1}")
            break
