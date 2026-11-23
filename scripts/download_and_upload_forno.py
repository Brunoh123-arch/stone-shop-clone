import os
import subprocess
import requests

os.makedirs('videosprodutos/forno_hq', exist_ok=True)
os.makedirs('img/posters-forno-hq', exist_ok=True)

targets = [
    {"id": "W_gwAzpo3q0", "clips": [(30, 20), (75, 20), (130, 20), (220, 20)]},
    {"id": "USHt2ig_6qU", "clips": [(10, 20), (45, 20), (80, 20)]},
    {"id": "1plO_yV6DUo", "clips": [(40, 20), (120, 20), (210, 20)]},
    {"id": "SagVnZmIE1Q", "clips": [(20, 20), (60, 20)]},
    {"id": "WhcvWXCrK8A", "clips": [(15, 20), (50, 20)]}
]

def upload_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    with open(file_path, "rb") as f:
        data = {"reqtype": "fileupload"}
        files = {"fileToUpload": f}
        r = requests.post(url, data=data, files=files, timeout=60)
        if r.status_code == 200 and r.text.startswith("https://files.catbox.moe/"):
            return r.text.strip()
    return None

results = []
count = 1

for t in targets:
    vid = t["id"]
    yt_url = f"https://www.youtube.com/watch?v={vid}"
    print(f"Obtendo stream para {vid}...")
    
    cmd_url = f'yt-dlp -g -f "best[ext=mp4]/best" "{yt_url}"'
    try:
        proc = subprocess.run(cmd_url, shell=True, capture_output=True, text=True, timeout=30)
        stream_url = proc.stdout.strip().split('\n')[0]
        if not stream_url.startswith("http"):
            print(f"Falha ao obter stream para {vid}")
            continue
            
        for start, dur in t["clips"]:
            out_mp4 = f"videosprodutos/forno_hq/forno-c{count}.mp4"
            out_poster = f"img/posters-forno-hq/poster-forno-c{count}.jpg"
            
            # Recorta 20s do stream direto em alta velocidade sem baixar o vídeo inteiro
            # Corta em 9:16 ou mantém proporção original
            cmd_cut = f'ffmpeg -y -ss {start} -i "{stream_url}" -t {dur} -c:v libx264 -preset ultrafast -crf 26 -c:a aac -b:a 96k "{out_mp4}"'
            subprocess.run(cmd_cut, shell=True, capture_output=True, timeout=60)
            
            if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 10000:
                # Gera poster frame
                cmd_poster = f'ffmpeg -y -ss 1 -i "{out_mp4}" -vframes 1 -q:v 2 "{out_poster}"'
                subprocess.run(cmd_poster, shell=True, capture_output=True, timeout=15)
                
                print(f"Vídeo {count} gerado: {out_mp4} ({os.path.getsize(out_mp4)} bytes). Fazendo upload Catbox...")
                catbox_url = upload_catbox(out_mp4)
                if catbox_url:
                    print(f"  -> Catbox: {catbox_url}")
                    results.append({
                        "index": count,
                        "local_video": f"../{out_mp4}",
                        "catbox_url": catbox_url,
                        "poster": f"../{out_poster}"
                    })
                else:
                    results.append({
                        "index": count,
                        "local_video": f"../{out_mp4}",
                        "catbox_url": f"../{out_mp4}",
                        "poster": f"../{out_poster}"
                    })
                count += 1
    except Exception as e:
        print(f"Erro em {vid}: {e}")

print("Total de clipes gerados:", len(results))
with open("scripts/forno_clips_result.json", "w", encoding="utf-8") as f:
    import json
    json.dump(results, f, indent=2)
