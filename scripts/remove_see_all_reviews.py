import os
import re

pattern = re.compile(r'\s*<button[^>]*class="see-all-reviews"[^>]*>.*?</button>', re.IGNORECASE)

removed = []
for f in os.listdir('pages'):
    if f.endswith('.html'):
        p = os.path.join('pages', f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
            content = fl.read()

        if pattern.search(content):
            new_content = pattern.sub('', content)
            with open(p, 'w', encoding='utf-8') as fl:
                fl.write(new_content)
            removed.append(f)

print(f"Total de paginas alteradas: {len(removed)}")
for f in removed:
    print(f"  Removido de: {f}")
