import subprocess
import os
import json
import concurrent.futures

data = json.load(open('scripts/found_piscina_videos.json', encoding='utf-8'))
valid = [d for d in data if 8 <= (d.get('duration') or 0) <= 120][:32]

os.makedirs('videosprodutos/piscina_32', exist_ok=True)
os.makedirs('img/posters-piscina', exist_ok=True)

urls_file = 'scripts/piscina_32_catbox_urls.json'
if os.path.exists(urls_file):
    try:
        uploaded = json.load(open(urls_file, encoding='utf-8'))
    except:
        uploaded = {}
else:
    uploaded = {}

def process_item(item):
    idx, v = item
    vid_id = v['id']
    title = v['title']
    channel = v['channel']
    key = f"pool_{idx:02d}"
    
    mp4_file = f"videosprodutos/piscina_32/{key}.mp4"
    poster_file = f"img/posters-piscina/poster-piscina-{idx:02d}.jpg"
    
    if key in uploaded and uploaded[key].get('catbox'):
        print(f"[{idx:02d}] Already uploaded: {uploaded[key]['catbox']}")
        return key, uploaded[key]
        
    # Download
    if not os.path.exists(mp4_file) or os.path.getsize(mp4_file) < 50000:
        url = f"https://www.youtube.com/watch?v={vid_id}"
        cmd_dl = [
            "yt-dlp",
            "-f", "mp4[height<=720]/best[ext=mp4]/best",
            "--force-overwrites",
            "-o", mp4_file,
            url
        ]
        subprocess.run(cmd_dl, capture_output=True)
        
    if not os.path.exists(mp4_file) or os.path.getsize(mp4_file) < 50000:
        print(f"[{idx:02d}] DL failed: {vid_id}")
        return key, None
        
    # Poster
    if not os.path.exists(poster_file) or os.path.getsize(poster_file) < 5000:
        cmd_ff = [
            "ffmpeg", "-y", "-ss", "00:00:01", "-i", mp4_file,
            "-vframes", "1", "-q:v", "2", poster_file
        ]
        subprocess.run(cmd_ff, capture_output=True)
        
    # Catbox upload
    cmd_up = [
        "curl.exe", "-s",
        "-F", "reqtype=fileupload",
        f"-FfileToUpload=@{mp4_file}",
        "https://catbox.moe/user/api.php"
    ]
    res_up = subprocess.run(cmd_up, capture_output=True, text=True)
    cat_url = res_up.stdout.strip()
    if cat_url.startswith("https://files.catbox.moe/"):
        print(f"[{idx:02d}] Catbox OK: {cat_url}")
        res_data = {
            "catbox": cat_url,
            "title": title,
            "channel": channel,
            "poster": f"../img/posters-piscina/poster-piscina-{idx:02d}.jpg"
        }
        return key, res_data
    else:
        print(f"[{idx:02d}] Catbox err: {cat_url}")
        return key, None

items = [(i + 1, v) for i, v in enumerate(valid)]

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(process_item, items)
    for key, res_data in results:
        if res_data:
            uploaded[key] = res_data

with open(urls_file, 'w', encoding='utf-8') as f:
    json.dump(uploaded, f, ensure_ascii=False, indent=2)

print(f"\nALL DONE! Uploaded: {len(uploaded)}/32")
