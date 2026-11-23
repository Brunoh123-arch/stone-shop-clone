import os
import subprocess

videos = [
    ("H4olkS0fO9Y", "videosprodutos/criador-4-1.mp4", "img/poster-criador-4-1.jpg"),
    ("rTLOatAxBDo", "videosprodutos/criador-4-2.mp4", "img/poster-criador-4-2.jpg"),
    ("PZfrQABXIRo", "videosprodutos/criador-4-3.mp4", "img/poster-criador-4-3.jpg")
]

os.makedirs('videosprodutos', exist_ok=True)
os.makedirs('img', exist_ok=True)
os.makedirs('videosprodutos/posters', exist_ok=True)

for vid, out_vid, out_post in videos:
    print(f"Downloading {vid} -> {out_vid}...")
    temp_file = f"videosprodutos/temp_{vid}.mp4"
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", temp_file,
        f"https://www.youtube.com/watch?v={vid}"
    ]
    subprocess.run(cmd, check=True)
    
    # Check orientation with ffprobe
    probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "{temp_file}"'
    res = subprocess.check_output(probe_cmd, shell=True).decode().strip()
    print(f"Resolution of {vid}: {res}")
    w, h = [int(x) for x in res.split('x')]
    
    if h > w:
        vf = "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black"
    else:
        # horizontal to vertical: fit centered with black bars or crop
        # TikTok standard pillarbox / crop:
        vf = "scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:black"
        
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
    
    poster_alt = f"videosprodutos/posters/poster-criador-4-{out_vid[-5]}.jpg"
    cmd_post2 = ["ffmpeg", "-y", "-ss", "00:00:00.2", "-i", out_vid, "-vframes", "1", "-q:v", "2", poster_alt]
    subprocess.run(cmd_post2, check=True)
    
    if os.path.exists(temp_file):
        os.remove(temp_file)
    print(f"Done: {out_vid} ({os.path.getsize(out_vid)} bytes), Poster: {out_post}")
