import glob

for f in glob.glob('scripts/*.py') + glob.glob('*.json'):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            txt = fp.read()
        if 'video-produto-33' in txt:
            print(f"Found in: {f}")
    except:
        pass
