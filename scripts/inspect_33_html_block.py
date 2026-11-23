with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(678, min(len(lines), 770)):
    print(f"{i+1}: {lines[i]}", end='')
