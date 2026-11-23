# -*- coding: utf-8 -*-
import json

for fname in ['p12_piscina_mor_12.json', 'p20_bike_gt_20.json', 'p21_bola_penalty_21.json', 'p87_mom_jeans_87.json']:
    data = json.load(open('scripts/data/extracted_lote4/' + fname, 'r', encoding='utf-8'))
    print(f"=== {fname} ===")
    for i, x in enumerate(data[:6]):
        print(f"  {i}: @{x['username']} | {x['nickname']}")
