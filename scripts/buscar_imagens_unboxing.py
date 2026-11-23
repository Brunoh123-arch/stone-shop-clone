import os

for term in ['elgin', 'fritadeira', 'cadeira', 'praia', 'joog', 'brasil', 'portugal', 'p5', 'p17', 'p18', 'p61', 'p74', 'p99']:
    matches = []
    for f in os.listdir('img'):
        if term in f.lower():
            matches.append(f)
    if matches:
        print(f"=== Match '{term}' ({len(matches)} files) ===")
        print(" ", matches[:8])
