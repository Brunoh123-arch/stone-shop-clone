# -*- coding: utf-8 -*-
import re

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Testar regex mais seguro
arrays = re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*(\[\s*\{[\s\S]*?\n\s*\]);', js_content)
print(f"Total de arrays encontrados com regex balanceado: {len(arrays)}")

for name, body in arrays:
    if name in ['JOOG_ONE_57_VIDEOS_MAP', 'WAAW_HYPERBOOM_73_VIDEOS_MAP']:
        vids = re.findall(r'video:\s*["\']([^"\']+)["\']', body)
        print(f"Array {name}: {len(vids)} videos -> {vids}")
