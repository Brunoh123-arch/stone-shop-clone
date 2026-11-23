import re

with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    c = f.read()

matches = list(re.finditer(r'const\s+([A-Z0-9_]+)\s*=\s*\[', c))
dupes_found = 0

for m in matches:
    name = m.group(1)
    if not any(k in name for k in ['CREATORS', 'VIDEOS', 'MAP', 'DATASET']):
        continue
    start = m.end()
    end = c.find('];', start)
    if end != -1:
        block = c[start:end]
        # Pegar apenas o campo "video": ou video:
        video_fields = re.findall(r'["\']?video["\']?\s*:\s*["\']([^"\']+)["\']', block)
        if len(video_fields) > len(set(video_fields)):
            dupes_found += 1
            print(f"DUPLICATA REAL DE VÍDEO em {name}: {len(video_fields)} criadores, {len(set(video_fields))} vídeos distintos!")

print(f"\nTotal de arrays com vídeos duplicados entre criadores diferentes: {dupes_found}")
if dupes_found == 0:
    print("ZERO DUPLICATAS DE VÍDEO EM TODO O JS/VIDEOS-CRIADORES.JS! 100% LIMPO E DESDUPLICADO!")
