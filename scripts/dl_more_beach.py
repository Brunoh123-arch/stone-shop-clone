import subprocess
import os
import json

more_vids = [
    {"id": "ztm8SclT6lk", "name": "cooler_18l_mor_unboxing", "creator": "Thiago MOR", "user": "thiago.mor", "desc": "Caixa térmica de 18 litros da Mor segurando o gelo o dia inteiro na praia! 🧊🏖️"},
    {"id": "Cu1RnNNIbFU", "name": "cooler_18l_azul", "creator": "Resseg Distribuidora", "user": "ressegdistribuidora", "desc": "Demonstração da caixa térmica 18L e 34L azul original Mor com trava de segurança! ❄️✨"},
    {"id": "XE9IGwPYzHc", "name": "guarda_sol_colorido", "creator": "Ditudotem", "user": "ditudotem_lazer", "desc": "Guarda-sol Mor colorido com proteção solar UV e varetas reforçadas! ☀️⛱️"},
    {"id": "OIWeXkaW214", "name": "guarda_sol_aluminio", "creator": "Bazar De Praia", "user": "bazardepraia", "desc": "Guarda-sol de alumínio 2,00m leve e fácil de fixar na areia com o saca-areia! 🏖️💪"},
    {"id": "5HGHkoAM_pU", "name": "cadeira_summer_azul", "creator": "Espedito Soares", "user": "espedito.praia", "desc": "Cadeira reclinável Summer Mor: 4 posições, reclina super fácil e macia! 🌊🛋️"},
    {"id": "xbQVpBhpsSg", "name": "cadeira_reclinavel_5pos", "creator": "Negromonte Store", "user": "negromontestore", "desc": "Cadeira de praia reclinável em alumínio reforçado que não enferruja! ☀️🌴"},
    {"id": "4PW7-s7rKBM", "name": "cooler_compacto_mor", "creator": "Lazer e Família", "user": "lazerefamilia", "desc": "Praticidade do cooler e isolamento térmico para bebidas e lanches na praia! 🍺🧊"},
    {"id": "D6UoEGwqwac", "name": "guarda_sol_azul_mor", "creator": "Achadinhos da Luiza", "user": "achadinhosdaluiza", "desc": "Achadinho perfeito pro verão: guarda-sol articulado com tecido reforçado! ☀️⛱️"}
]

uploaded_more = {}

for v in more_vids:
    vid_url = f"https://www.youtube.com/watch?v={v['id']}"
    out_mp4 = f"videosprodutos/praia/{v['name']}.mp4"
    poster_jpg = f"img/posters-praia/poster-{v['name']}.jpg"
    
    print(f"Downloading {v['name']}...")
    if not os.path.exists(out_mp4) or os.path.getsize(out_mp4) < 100000:
        subprocess.run([
            "yt-dlp", "-f", "mp4[height<=720]/best[ext=mp4]/best",
            "--force-overwrites", "-o", out_mp4, vid_url
        ])
        
    if os.path.exists(out_mp4) and os.path.getsize(out_mp4) > 100000:
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:01", "-i", out_mp4,
            "-vframes", "1", "-q:v", "2", poster_jpg
        ], capture_output=True)
        
        print(f"Uploading {v['name']} via curl.exe...")
        cmd = ["curl.exe", "-s", "-F", "reqtype=fileupload", f"-FfileToUpload=@{out_mp4}", "https://catbox.moe/user/api.php"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        cat_url = res.stdout.strip()
        if cat_url.startswith("https://files.catbox.moe/"):
            print(f"  -> {cat_url}")
            uploaded_more[v['name']] = {
                "catbox": cat_url,
                "name": v['creator'],
                "username": v['user'],
                "desc": v['desc'],
                "poster": f"../img/posters-praia/poster-{v['name']}.jpg"
            }

with open("scripts/more_beach_uploaded.json", "w", encoding="utf-8") as fp:
    json.dump(uploaded_more, fp, ensure_ascii=False, indent=2)

print(f"Done! Downloaded and uploaded {len(uploaded_more)} more beach videos!")
