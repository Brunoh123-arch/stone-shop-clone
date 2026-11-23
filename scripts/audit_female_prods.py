import os
import re

female_prods = [104, 103, 106, 87, 88, 38, 39, 45, 108, 109, 28]

report = {}
for pid in female_prods:
    filepath = f'pages/produto-{pid}.html'
    if not os.path.exists(filepath):
        report[pid] = 'File not found'
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Find all avatar images
    avatars = re.findall(r'src=["\']([^"\']*avatar[^"\']*)["\']', html)
    validadas = [a for a in avatars if 'mulheres_validadas' in a]
    outras = [a for a in avatars if 'mulheres_validadas' not in a]
    
    report[pid] = {
        'total_avatars': len(avatars),
        'validadas': len(validadas),
        'outras': outras
    }

for pid, data in report.items():
    print(f'P{pid}: {data}')
