with open('pages/produto-115.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(630, 660):
    print(f"{j+1}: {lines[j]}", end='')
