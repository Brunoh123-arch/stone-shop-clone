import subprocess
import os

os.makedirs('videosprodutos', exist_ok=True)

downloads = [
    # 1. Vídeo curto oficial/criador da Arke Vitta Smart 5 espetos elétrica
    ('AM7zsJJl85g', 'videosprodutos/criador-14-1.mp4'),
    # 2. Frangos e carnes nos 5 espetos girando
    ('bb1uJmCP3B8', 'videosprodutos/criador-14-2.mp4'),
    # 3. Review caseiro da Arke 5 espetos no apartamento
    ('WgtwlxZDS-k', 'videosprodutos/criador-14-3.mp4')
]

for yt_id, out_file in downloads:
    url = f"https://www.youtube.com/watch?v={yt_id}"
    print(f"Baixando {url} -> {out_file}...")
    # Baixar em mp4 com video e audio compativeis
    cmd = f'yt-dlp -f "best[ext=mp4][height<=720]/best[ext=mp4]/best" -o "{out_file}" --force-overwrites "{url}"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if os.path.exists(out_file) and os.path.getsize(out_file) > 100000:
        print(f"  [SUCESSO] {out_file}: {os.path.getsize(out_file)} bytes")
    else:
        print(f"  [AVISO] Tentando fallback para {yt_id}...")
        cmd_fallback = f'yt-dlp -o "{out_file}" --force-overwrites "{url}"'
        subprocess.run(cmd_fallback, shell=True)
        if os.path.exists(out_file):
            print(f"  [SUCESSO FALLBACK] {out_file}: {os.path.getsize(out_file)} bytes")
        else:
            print(f"  [ERRO] Falha ao baixar {yt_id}")
