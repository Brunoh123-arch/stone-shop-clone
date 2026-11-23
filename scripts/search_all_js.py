import os

js_dir = 'js'
for f in os.listdir(js_dir):
    p = os.path.join(js_dir, f)
    if os.path.isfile(p) and f.endswith('.js'):
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
        
        matches = []
        for w in ['camila souza', 'camila', 'fernanda lima', 'larissa mello', 'lrv49i', 'chinelo']:
            count = c.lower().count(w)
            if count > 0:
                matches.append(f"{w}: {count}")
        if matches:
            print(f"File {f}: {', '.join(matches)}")
