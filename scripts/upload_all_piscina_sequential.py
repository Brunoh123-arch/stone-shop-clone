import subprocess
import os
import json
import time

replacements = {
    7: ("MvqcRGqBgTA", "EU JÁ COMPREI and TUDO DE PISCINA", "Piscina inflável infantil montagem e teste"),
    27: ("OeuG9cJ_f8E", "IRS Garage 87", "Piscina 1000 Litros Mor vale a pena no calor"),
    32: ("lMn819mEw84", "Ajtech Lazer", "Piscina Inflável Mor Splash Fun para quintal")
}

for idx, (vid_id, ch, tt) in replacements.items():
    mp4_file = f"videosprodutos/piscina_32/pool_{idx:02d}.mp4"
    if not os.path.exists(mp4_file) or os.path.getsize(mp4_file) < 50000:
        url = f"https://www.youtube.com/watch?v={vid_id}"
        print(f"Downloading replacement {idx:02d} ({vid_id})...")
        cmd = ["yt-dlp", "-f", "mp4[height<=720]/best[ext=mp4]/best", "--force-overwrites", "-o", mp4_file, url]
        subprocess.run(cmd, capture_output=True)

print("Checking all 32 files...")
missing = []
for i in range(1, 33):
    f = f"videosprodutos/piscina_32/pool_{i:02d}.mp4"
    if not os.path.exists(f) or os.path.getsize(f) < 50000:
        missing.append(i)

print(f"Missing files: {missing}")

# Now upload all 32 sequentially to Catbox with retry
urls_file = 'scripts/piscina_32_catbox_urls.json'
if os.path.exists(urls_file):
    try:
        uploaded = json.load(open(urls_file, encoding='utf-8'))
    except:
        uploaded = {}
else:
    uploaded = {}

for i in range(1, 33):
    key = f"pool_{i:02d}"
    mp4_file = f"videosprodutos/piscina_32/{key}.mp4"
    poster_file = f"img/posters-piscina/poster-piscina-{i:02d}.jpg"
    
    if key in uploaded and uploaded[key].get('catbox') and uploaded[key]['catbox'].startswith('https://files.catbox.moe/'):
        print(f"[{i:02d}] Already on Catbox: {uploaded[key]['catbox']}")
        continue
        
    if not os.path.exists(mp4_file):
        print(f"[{i:02d}] File missing: {mp4_file}")
        continue
        
    # Generate poster
    if not os.path.exists(poster_file) or os.path.getsize(poster_file) < 5000:
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:01", "-i", mp4_file,
            "-vframes", "1", "-q:v", "2", poster_file
        ], capture_output=True)
        
    print(f"[{i:02d}] Uploading {mp4_file} to Catbox...")
    cmd = ["curl.exe", "-s", "-F", "reqtype=fileupload", f"-FfileToUpload=@{mp4_file}", "https://catbox.moe/user/api.php"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout.strip()
    
    if not out.startswith("https://files.catbox.moe/"):
        time.sleep(2)
        res = subprocess.run(cmd, capture_output=True, text=True)
        out = res.stdout.strip()
        
    if out.startswith("https://files.catbox.moe/"):
        print(f"  -> {out}")
        uploaded[key] = {
            "catbox": out,
            "poster": f"../img/posters-piscina/poster-piscina-{i:02d}.jpg"
        }
    else:
        print(f"  FAILED: {out}")
        
    time.sleep(0.5)

with open(urls_file, 'w', encoding='utf-8') as f:
    json.dump(uploaded, f, ensure_ascii=False, indent=2)

print(f"\nCOMPLETED! Total Catbox URLs: {len(uploaded)}/32")
