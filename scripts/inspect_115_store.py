with open('pages/produto-115.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(635, 715):
    print(f"{i+1}: {lines[i]}", end='')
