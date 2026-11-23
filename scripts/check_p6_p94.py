# -*- coding: utf-8 -*-
import json

p6 = json.load(open('scripts/data/extracted_lote4/p6_bike_spinning_6.json', 'r', encoding='utf-8'))
p94 = json.load(open('scripts/data/extracted_lote4/p94_bike_spinning_94.json', 'r', encoding='utf-8'))

print("=== P06 Candidates ===")
for i, x in enumerate(p6[:8]):
    print(f"  {i}: @{x['username']} | {x['nickname']}")

print("\n=== P94 Candidates ===")
for i, x in enumerate(p94[:8]):
    print(f"  {i}: @{x['username']} | {x['nickname']}")
