with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(678, 755):
    print(f"{i+1}: {lines[i]}", end='')
