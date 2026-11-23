import json

with open("scripts/catbox_audit_results.json", "r", encoding="utf-8") as f:
    d = json.load(f)["details"]

print("Length of details:", len(d))
print("Item 0:", d[0])
print("Item 1:", d[1])
