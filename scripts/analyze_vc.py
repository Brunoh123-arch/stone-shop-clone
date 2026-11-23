with open('js/videos-criadores.js', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i, l in enumerate(lines):
    if l.strip().startswith('const CREATORS_'):
        print(f"Line {i+1}: {l.strip()[:60]}")
    elif l.strip() == '})();':
        print(f"*** IIFE ENDS AT LINE {i+1} ***")
