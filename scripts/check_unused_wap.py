# -*- coding: utf-8 -*-
import json

existing_text = open('js/videos-criadores-v3.js', 'r', encoding='utf-8').read()
p78_raw = json.load(open('scripts/data/extracted_lote3/p78_wap_spotcleaner_78.json', 'r', encoding='utf-8'))

unused = []
for it in p78_raw:
    u = it['username'].lower()
    if u not in existing_text.lower():
        unused.append(it)

print(f"Total unused in p78: {len(unused)}")
for i, x in enumerate(unused[:6]):
    print(f"  {i}: @{x['username']} | {x['nickname']} | desc={x['desc'][:40]}")
