import os

for f in os.listdir('scripts'):
    if 'bluey' in f.lower() or 'p33' in f.lower():
        print(f)
