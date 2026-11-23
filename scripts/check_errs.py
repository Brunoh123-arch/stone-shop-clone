import json

with open('scripts/shard1_audit_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for x in data:
    if x.get('status') is None or 'error' in x:
        print(f"ID {x['id']}: error = {x.get('error')}, status = {x.get('status')}")
