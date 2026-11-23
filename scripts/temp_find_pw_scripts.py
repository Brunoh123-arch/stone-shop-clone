import glob, os, re

scripts = glob.glob("scripts/**/*.py", recursive=True)
for s in scripts:
    with open(s, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()
    if 'profile 42' in c.lower() or 'playwright' in c.lower() or 'catbox' in c.lower() or 'chrome' in c.lower():
        print(f"Script: {s}")
        for line in c.split('\n')[:20]:
            if any(k in line.lower() for k in ['profile', 'chrome', 'connect', 'user_data', 'launch', 'catbox']):
                print("  ", line.strip())
