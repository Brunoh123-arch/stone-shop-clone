# -*- coding: utf-8 -*-
import json

items = json.load(open('scripts/data/extracted_lote4/p21_bola_penalty_21.json', 'r', encoding='utf-8'))
for i, x in enumerate(items[:10]):
    print(f"[{i}] @{x['username']} | {x['nickname']} | desc={x['desc'][:40]}")
