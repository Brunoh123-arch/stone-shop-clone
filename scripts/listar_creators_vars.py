import re

with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

# Achar todas as declarações const CREATORS_... =
creators_vars = re.findall(r'const\s+(CREATORS_[A-Za-z0-9_]+)\s*=', text)
print(f"Total de const CREATORS_... encontradas: {len(creators_vars)}")
for cv in sorted(set(creators_vars)):
    print(" ", cv)
