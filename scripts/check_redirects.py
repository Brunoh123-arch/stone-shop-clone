import os

SHARD_IDS = [80, 82, 85, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]

for pid in SHARD_IDS:
    path = f"pages/produto-{pid}.html"
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    if "noredirect=1" in c or "location.replace" in c:
        for line in c.splitlines():
            if "location.replace" in line or "http-equiv=\"refresh\"" in line:
                print(f"P{pid} redirect: {line.strip()}")
