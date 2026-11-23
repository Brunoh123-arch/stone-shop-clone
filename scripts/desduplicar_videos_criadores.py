import re

with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    content = f.read()

# Função para desduplicar objetos dentro de um array JS
# Formato: { video: "...", poster: "...", ... } ou [ { url: "...", ... } ]
def deduplicate_js_array(match):
    array_name = match.group(1)
    array_body = match.group(2)
    
    # Se não for array de vídeos ou criadores, não mexe
    if not any(k in array_name for k in ['CREATORS', 'VIDEOS', 'MAP', 'DATASET']):
        return match.group(0)
        
    # Extrair objetos { ... }
    # Usa regex para pegar cada item entre chaves { ... }
    items = re.findall(r'(\{[^{}]*\})', array_body)
    if not items:
        return match.group(0)
        
    seen_videos = set()
    seen_users = set()
    unique_items = []
    
    for it in items:
        # Achar url de video
        v_m = re.search(r'(https://files\.catbox\.moe/[a-zA-Z0-9_-]+\.mp4|videosprodutos/[^"\']+\.mp4)', it)
        u_m = re.search(r'username:\s*["\']([^"\']+)["\']', it)
        
        video_url = v_m.group(1) if v_m else None
        user_name = u_m.group(1) if u_m else None
        
        # Se tem vídeo e já vimos esse vídeo neste array, descarta a duplicata!
        if video_url:
            if video_url in seen_videos:
                continue
            seen_videos.add(video_url)
            
        if user_name:
            if user_name in seen_users:
                continue
            seen_users.add(user_name)
            
        unique_items.append(it)
        
    if len(unique_items) < len(items):
        print(f"Array {array_name}: Reduzido de {len(items)} para {len(unique_items)} vídeos 100% ÚNICOS!")
        new_body = "\n  " + ",\n  ".join(unique_items) + "\n"
        return f"const {array_name} = [{new_body}];"
    else:
        return match.group(0)

# Substituir arrays
new_content = re.sub(r'const\s+([A-Z0-9_]+)\s*=\s*\[([\s\S]*?)\];', deduplicate_js_array, content)

with open("js/videos-criadores.js", "w", encoding="utf-8") as f:
    f.write(new_content)

print("js/videos-criadores.js desduplicado com sucesso!")
