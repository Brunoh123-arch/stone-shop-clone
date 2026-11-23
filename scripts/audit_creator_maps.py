import re

with open('js/videos-criadores-v3.js', 'r', encoding='utf-8') as f:
    code = f.read()

maps = {}
for m in re.finditer(r'const\s+([A-Za-z0-9_]+_VIDEOS_MAP)\s*=\s*\[([\s\S]*?)\];', code):
    var_name = m.group(1)
    body = m.group(2)
    video_count = len(re.findall(r'video:\s*[\'"]', body))
    maps[var_name] = video_count

single_video_maps = {k: v for k, v in maps.items() if v == 1}
multi_video_maps = {k: v for k, v in maps.items() if v > 1}

print(f"Total de mapas de video encontrados: {len(maps)}")
print(f"Mapas com multiplos videos: {len(multi_video_maps)}")
print(f"Mapas com apenas 1 video: {len(single_video_maps)}")

print("\nLista dos mapas com apenas 1 video:")
for k, v in sorted(single_video_maps.items()):
    print(f"  {k}: {v} video")
