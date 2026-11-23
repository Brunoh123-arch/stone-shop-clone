# -*- coding: utf-8 -*-
import json

d = json.load(open('scripts/data/lote4_ready.json', 'r', encoding='utf-8'))

for pid in ['6', '12', '20', '21']:
    items = d.get(pid, [])
    seen = set()
    dedup = []
    for it in items:
        u = it['username'].lower()
        if u not in seen:
            seen.add(u)
            dedup.append(it)
    d[pid] = dedup[:3]

with open('scripts/data/lote4_ready.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

for k, v in d.items():
    print(k, len(v), [x['username'] for x in v])
