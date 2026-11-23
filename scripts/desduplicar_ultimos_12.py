import re

with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    content = f.read()

def clean_remaining_dupes(match):
    array_name = match.group(1)
    array_body = match.group(2)
    
    # Extrair objetos { ... }
    items = re.findall(r'(\{[^{}]*\})', array_body)
    if not items:
        return match.group(0)
        
    seen_videos = set()
    unique_items = []
    
    for it in items:
        v_m = re.search(r'(https://files\.catbox\.moe/[a-zA-Z0-9_-]+\.mp4|videosprodutos/[^"\']+\.mp4)', it)
        video_url = v_m.group(1) if v_m else None
        
        if video_url:
            if video_url in seen_videos:
                continue
            seen_videos.add(video_url)
            
        unique_items.append(it)
        
    if len(unique_items) < len(items):
        print(f"Limpando {array_name}: de {len(items)} para {len(unique_items)} únicos!")
        new_body = "\n  " + ",\n  ".join(unique_items) + "\n"
        return f"const {array_name} = [{new_body}];"
    else:
        return match.group(0)

target_arrays = [
    'CREATORS_CLIMATIZADOR_OSTER_11',
    'CREATORS_CLIMATIZADOR_MIDEA_30',
    'CREATORS_CLIMATIZADOR_VENTISOL_44',
    'CREATORS_AR_HQ_29',
    'CREATORS_AR_HQ_9',
    'CREATORS_AR_HISENSE_10',
    'CREATORS_AR_LG_27',
    'CREATORS_PISCINA_PIXLAR_13',
    'CREATORS_CHURRASQUEIRA_ARKE_14',
    'CREATORS_CHURRASQUEIRA_BISCUITT_15',
    'CREATORS_CADEIRAS_PRAIA_MOR_17',
    'CREATORS_KIT_PRAIA_MOR_18'
]

for t in target_arrays:
    pattern = rf'const\s+{t}\s*=\s*\[([\s\S]*?)\];'
    m = re.search(pattern, content)
    if m:
        rep = clean_remaining_dupes(re.match(rf'const\s+({t})\s*=\s*\[([\s\S]*?)\];', m.group(0)))
        content = content[:m.start()] + rep + content[m.end():]

with open("js/videos-criadores.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Todos os 12 arrays restantes desduplicados!")
