import subprocess
import os

links = [
    ("sergia_gt", "https://www.tiktok.com/@achadinhos.by.sergia/video/7677808936585579796"),
    ("renato_bike", "https://www.tiktok.com/@renatosantos214/video/7661337005921455378"),
    ("vitrine_gt", "https://www.tiktok.com/@vitrineesperta.achados/video/7685077822209035538"),
    ("pterous_mtb", "https://www.tiktok.com/@pterous.dream/video/7691851471272381697")
]

os.makedirs("temp_p20_tiktok", exist_ok=True)

for name, url in links:
    out_path = f"temp_p20_tiktok/{name}.mp4"
    print(f"Downloading {name} from {url}...")
    cmd = ["yt-dlp", "-o", out_path, url]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(out_path):
        print(f"Success: {out_path} ({os.path.getsize(out_path)} bytes)")
        # Extract frame
        frame_path = f"temp_p20_tiktok/{name}.jpg"
        subprocess.run(["ffmpeg", "-y", "-i", out_path, "-ss", "00:00:02", "-vframes", "1", frame_path], capture_output=True)
    else:
        print(f"Failed {name}: {res.stderr}")
