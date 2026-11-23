with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(170, 215):
    print(f"{j+1}: {lines[j]}", end='')
