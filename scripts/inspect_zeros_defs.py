# -*- coding: utf-8 -*-
import re

with open('js/videos-criadores-v3.js', 'r', encoding='utf-8') as f:
    txt = f.read()

cases = re.findall(r'case\s+(\d+):\s+activeDataset\s*=\s*([A-Za-z0-9_]+);', txt)

for pid_str, ds_name in cases:
    if pid_str in ['5', '9', '10', '11', '13', '27', '29', '30', '44', '47', '52', '102', '14', '15', '101', '49', '60', '98']:
        # Procurar definicao de ds_name
        lines = [l.strip() for l in txt.split('\n') if f'const {ds_name}' in l or f'let {ds_name}' in l or f'var {ds_name}' in l]
        print(f"P{pid_str} ({ds_name}): {lines[:2]}")
