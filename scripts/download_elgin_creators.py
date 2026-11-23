import os
import subprocess

videos = [
    ("Z0zB1FNOjoE", "videosprodutos/criador-5-1.mp4", "img/poster-criador-5-1.jpg"),
    ("LD23XCj4oIw", "videosprodutos/criador-5-2.mp4", "img/poster-criador-5-2.jpg"),
    ("kRlTaEfnPME", "videosprodutos/criador-5-3.mp4", "img/poster-criador-5-3.jpg")
]

os.makedirs('videosprodutos', exist_ok=True)
os.makedirs('img', exist_ok=True)
os.makedirs('videosprodutos/posters', exist_ok=True)

for vid, out_vid, out_post in videos:
    print(f"Downloading {vid} -> {out_vid}...")
    temp_file = f"videosprodutos/temp_{vid}.mp4"
    cmd = [
        "yt-dlp",
        "--js-runtimes", "node:C:/Program Files/nodejs/node.exe",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", temp_file,
        f"https://www.youtube.com/watch?v={vid}"
    ]
    subprocess.run(cmd, check=True)
    
    # Trim to 20-30s max vertical 720x1280 (standard TikTok Shop format)
    # Check orientation with ffprobe
    probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{temp_file}"'
    res = subprocess.check_output(probe_cmd, shell=True).decode().strip()
    print(f"Resolution of {vid}: {res}")
    w, h = [int(x) for x in res.split('x')]
    
    if h > w:
        # Vertical video
        vf = "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black"
    else:
        # Horizontal video - crop to vertical center or pad
        vf = "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280"
        
    cmd_ff = [
        "ffmpeg", "-y", "-i", temp_file,
        "-t", "25",
        "-vf", vf,
        "-c:v", "libx264", "-crf", "22", "-preset", "fast",
        "-c:a", "aac", "-b:a", "128k",
        out_vid
    ]
    subprocess.run(cmd_ff, check=True)
    
    # Generate poster at 00:00:00.2
    cmd_post1 = ["ffmpeg", "-y", "-ss", "00:00:00.2", "-i", out_vid, "-vframes", "1", "-q:v", "2", out_post]
    subprocess.run(cmd_post1, check=True)
    
    # Also save to videosprodutos/posters/
    poster_alt = f"videosprodutos/posters/poster-criador-5-{out_vid[-5]}.jpg"
    cmd_post2 = ["ffmpeg", "-y", "-ss", "00:00:00.2", "-i", out_vid, "-vframes", "1", "-q:v", "2", poster_alt]
    subprocess.run(cmd_post2, check=True)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print(f"Done: {out_vid} ({os.path.getsize(out_vid)} bytes), Poster: {out_post}")
