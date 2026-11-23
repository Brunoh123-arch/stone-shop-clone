with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "targetContainer.style.display = 'none'" in line:
        print(f'=== Line {i+1} ===')
        for j in range(max(0, i-10), min(len(lines), i+10)):
            print(f'{j+1}: {lines[j]}', end='')
