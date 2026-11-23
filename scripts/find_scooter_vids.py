import glob
import re

catbox_links = set()
for f in glob.glob('**/*.js', recursive=True) + glob.glob('**/*.html', recursive=True):
    try:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
            for m in re.findall(r'https?://(?:files\.)?catbox\.moe/[a-zA-Z0-9_\-]+\.mp4', c):
                catbox_links.add(m)
    except:
        pass

print(f'Total catbox mp4 links found across codebase: {len(catbox_links)}')

# Check if any mentions scooter
with open('js/videos-criadores.js', 'r', encoding='utf-8') as fp:
    c = fp.read()
    for m in re.findall(r'scooter.*?\.mp4', c, re.IGNORECASE):
        print('Scooter mp4 mention:', m)
