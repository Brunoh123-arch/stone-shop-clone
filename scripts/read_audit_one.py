import json

with open("scripts/audit_one_by_one_results.json", "r", encoding="utf-8") as f:
    d = json.load(f)

if isinstance(d, list):
    print("List of len", len(d))
    print("Keys of item 0:", list(d[0].keys()) if d else "empty")
    for item in d[:5]:
        print(item.get("id"), item.get("title")[:30] if item.get("title") else "no title")
