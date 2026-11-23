import subprocess
import os
import json
import urllib.request
import urllib.parse

# List of real beach product videos to download
videos_to_dl = [
    {"id": "6UCTrszYyk4", "name": "carrinho_praia_mor_1", "creator": "Mor Oficial", "user": "moroficial", "desc": "Lançamento oficial do carrinho de praia que carrega tudo e vira mesa com porta-copos! Praticidade total no verão ☀️🏖️"},
    {"id": "iGTWmDeiDy0", "name": "carrinho_praia_mor_2", "creator": "Mariana Santos", "user": "marisantos.praia", "desc": "Mesa portátil e suporte para copos encaixado direto na cadeira e no carrinho! Não suja nada de areia 🌊✨"},
    {"id": "z1hf7AJKA3w", "name": "carrinho_praia_mor_3", "creator": "Lucas Lazer", "user": "lucaslazerpraia", "desc": "Testando o carrinho com avanço suportando o cooler de 18L e as 4 cadeiras reclináveis na areia fofa! Puxa levíssimo! 🚀"},
    {"id": "M9x-YJ_4WS4", "name": "cadeiras_mor_reclinavel", "creator": "Camila Verão", "user": "camilaverao", "desc": "As cadeiras reclináveis em alumínio são muito confortáveis e não esquentam no sol! Super recomendo o kit! 😍"},
    {"id": "No585RkILy0", "name": "cadeiras_mor_aluminio", "creator": "Rodrigo Silva", "user": "rodrigosilva_viagens", "desc": "Cadeira de praia de alumínio da Mor: leve, resistente, não enferruja com a maresia de praia de jeito nenhum! 🏖️💪"},
    {"id": "sBxh-_whh3U", "name": "cadeiras_mor_cores", "creator": "Larissa Costa", "user": "larissacosta.home", "desc": "Cores lindas e acabamento reforçado! O kit com 4 cadeiras sortidas é a melhor economia pra família! ☀️🌈"},
    {"id": "hqtdalzRH2Q", "name": "cooler_mor_18l", "creator": "Felipe Churrasco", "user": "felipe_praia_churras", "desc": "A caixa térmica cooler segura o gelo e as latas trincando de geladas o dia todo debaixo do sol quente! Top demais! 🧊🍺"}
]

os.makedirs("videosprodutos/praia", exist_ok=True)
os.makedirs("img/posters-praia", exist_ok=True)

def upload_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(file_path)
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="reqtype"\r\n\r\nfileupload\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"\r\n'
        f"Content-Type: video/mp4\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
    
    req = urllib.request.Request(url, data=body, headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "User-Agent": "Mozilla/5.0"
    })
    
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            catbox_url = resp.read().decode("utf-8").strip()
            return catbox_url
    except Exception as e:
        print(f"Catbox upload failed for {filename}: {e}")
        return None

results = []

for v in videos_to_dl:
    vid_url = f"https://www.youtube.com/watch?v={v['id']}"
    out_mp4 = f"videosprodutos/praia/{v['name']}.mp4"
    poster_jpg = f"img/posters-praia/poster-{v['name']}.jpg"
    
    print(f"\n--- Downloading {v['name']} ({v['creator']}) ---")
    if not os.path.exists(out_mp4) or os.path.getsize(out_mp4) < 100000:
        dl_cmd = [
            "yt-dlp",
            "-f", "mp4[height<=720]/best[ext=mp4]/best",
            "--force-overwrites",
            "-o", out_mp4,
            vid_url
        ]
        subprocess.run(dl_cmd)
        
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 100000:
        # Generate clean frame poster
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:01", "-i", out_mp4,
            "-vframes", "1", "-q:v", "2", poster_jpg
        ], capture_output=True)
        print(f"Generated poster: {poster_jpg}")
        
        # Upload to catbox
        print("Uploading to Catbox...")
        catbox_link = upload_catbox(out_mp4)
        print(f"Catbox URL: {catbox_link}")
        
        results.append({
            "name": v["creator"],
            "username": v["user"],
            "poster": f"../img/posters-praia/poster-{v['name']}.jpg",
            "video": catbox_link or f"../videosprodutos/praia/{v['name']}.mp4",
            "title": v["desc"],
            "localVideo": f"../videosprodutos/praia/{v['name']}.mp4"
        })

with open("scripts/beach_creators_uploaded.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nSUCCESS! Downloaded and uploaded {len(results)} beach creator videos!")
