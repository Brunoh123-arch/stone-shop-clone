import subprocess
import os
import json
import time

data = json.load(open('scripts/found_piscina_videos.json', encoding='utf-8'))
valid = [d for d in data if 8 <= (d.get('duration') or 0) <= 120][:32]

os.makedirs('videosprodutos/piscina_32', exist_ok=True)
os.makedirs('img/posters-piscina', exist_ok=True)

uploaded = {}

for i, v in enumerate(valid):
    idx = i + 1
    vid_id = v['id']
    title = v['title']
    channel = v['channel']
    
    mp4_file = f"videosprodutos/piscina_32/pool_{idx:02d}.mp4"
    poster_file = f"img/posters-piscina/poster-piscina-{idx:02d}.jpg"
    
    print(f"\n[{idx:02d}/32] {channel} - {title[:40]}...")
    
    # Download video if not already present
    if not os.path.exists(mp4_file) or os.path.getsize(mp4_file) < 50000:
        url = f"https://www.youtube.com/watch?v={vid_id}"
        cmd_dl = [
            "yt-dlp",
            "-f", "mp4[height<=720]/best[ext=mp4]/best",
            "--force-overwrites",
            "-o", mp4_file,
            url
        ]
        res = subprocess.run(cmd_dl, capture_output=True, text=True)
        if not os.path.exists(mp4_file) or os.path.getsize(mp4_file) < 50000:
            print(f"  DL failed for {vid_id}: {res.stderr[:100]}")
            continue
            
    # Extract poster
    if not os.path.exists(poster_file) or os.path.getsize(poster_file) < 5000:
        cmd_ff = [
            "ffmpeg", "-y", "-ss", "00:00:01", "-i", mp4_file,
            "-vframes", "1", "-q:v", "2", poster_file
        ]
        subprocess.run(cmd_ff, capture_output=True)
        
    # Upload to Catbox
    cmd_up = [
        "curl.exe", "-s",
        "-F", "reqtype=fileupload",
        f"-FfileToUpload=@{mp4_file}",
        "https://catbox.moe/user/api.php"
    ]
    res_up = subprocess.run(cmd_up, capture_output=True, text=True)
    cat_url = res_up.stdout.strip()
    if cat_url.startswith("https://files.catbox.moe/"):
        print(f"  -> Catbox: {cat_url}")
        uploaded[f"pool_{idx:02d}"] = {
            "catbox": cat_url,
            "title": title,
            "channel": channel,
            "poster": f"../img/posters-piscina/poster-piscina-{idx:02d}.jpg"
        }
    else:
        print(f"  Catbox error: {cat_url}")
        time.sleep(1)

with open('scripts/piscina_32_catbox_urls.json', 'w', encoding='utf-8') as f:
    json.dump(uploaded, f, ensure_ascii=False, indent=2)

print(f"\nFINISHED! Uploaded {len(uploaded)}/32 videos.")
