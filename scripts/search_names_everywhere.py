import os

for root, dirs, files in os.walk('.'):
    if 'node_modules' in dirs: dirs.remove('node_modules')
    if '.git' in dirs: dirs.remove('.git')
    for f in files:
        p = os.path.join(root, f)
        try:
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                t = fp.read()
            if 'Camila Souza' in t or 'Larissa Mello' in t:
                print(f"Found in: {p}")
        except:
            pass
print("Search complete.")
