import os
import re

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'video:\s*["\']([^"\']+)["\']')
matches = pattern.findall(text)

local_vids = sorted(list(set([v for v in matches if not v.startswith('http')])))
print(f"Videos locais no js/videos-criadores.js: {len(local_vids)}")

# Check pages/*.html
html_vids = set()
for f in os.listdir('pages'):
    if f.endswith('.html'):
        p = os.path.join('pages', f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
            c = fl.read()
            m = re.findall(r'<video[^>]+src=["\']([^"\']+)["\']', c)
            for src in m:
                if not src.startswith('http'):
                    html_vids.add((src, f))

print(f"Videos locais em tags <video> nos HTMLs de pages/: {len(html_vids)}")
for v, src_html in sorted(html_vids):
    print(f"  {v} (em {src_html})")
