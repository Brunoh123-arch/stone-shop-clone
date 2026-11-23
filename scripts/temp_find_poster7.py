import glob, re

for f in glob.glob("**/*.js", recursive=True) + glob.glob("**/*.html", recursive=True):
    if '.git' in f or 'node_modules' in f: continue
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    if 'poster-criador-7' in c:
        print(f"Found in {f}:")
        for line in c.split('\n'):
            if 'poster-criador-7' in line:
                print("  ", line[:120])
