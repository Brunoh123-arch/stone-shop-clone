import os, subprocess, sys, glob
sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('videosprodutos/posters', exist_ok=True)

targets = [
    ("fymilzrJ_LI", "videosprodutos/video-produto-110-criadora4.mp4", "videosprodutos/posters/poster-produto-110-criadora4.jpg"),
    ("9IBkpUw62cI", "videosprodutos/video-produto-110-criadora5.mp4", "videosprodutos/posters/poster-produto-110-criadora5.jpg")
]

for vid, out_vid, out_post in targets:
    if os.path.exists(out_vid) and os.path.getsize(out_vid) > 50000:
        print(f"Already exists: {out_vid}")
        continue
    print(f"Downloading {vid} for {out_vid}...")
    cmd_dl = [
        "yt-dlp",
        "--js-runtimes", "node:C:/Program Files/nodejs/node.exe",
        "-o", f"videosprodutos/temp_{vid}.%(ext)s",
        f"https://www.youtube.com/watch?v={vid}"
    ]
    try:
        subprocess.run(cmd_dl, check=True)
        found = glob.glob(f"videosprodutos/temp_{vid}.*")
        if not found:
            print(f"Downloaded file not found for {vid}")
            continue
        actual_input = found[0]
        print(f"Found input file: {actual_input}")

        # Re-encode / trim to 25s max with vertical crop
        cmd_ff = [
            "ffmpeg", "-y", "-i", actual_input,
            "-t", "25",
            "-vf", "scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280",
            "-c:v", "libx264", "-crf", "23", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            out_vid
        ]
        res = subprocess.run(cmd_ff)
        if res.returncode != 0:
            subprocess.run(["ffmpeg", "-y", "-i", actual_input, "-t", "25", "-c:v", "libx264", "-c:a", "aac", out_vid], check=True)

        for f in found:
            try: os.remove(f)
            except: pass

        # Generate poster at 00:00:00.2
        subprocess.run([
            "ffmpeg", "-y", "-ss", "00:00:00.2", "-i", out_vid,
            "-vframes", "1", "-q:v", "2", out_post
        ], check=True)
        print(f"Success for {out_vid} and {out_post}")
    except Exception as e:
        print(f"Error processing {vid}: {e}")

print("Remaining Kappa videos processed!")
