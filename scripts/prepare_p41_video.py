import subprocess
import os
import requests

os.makedirs("temp_p41", exist_ok=True)
video_url = "https://www.youtube.com/watch?v=86z5u73vbWs"
raw_p41 = "temp_p41/oven_raw.mp4"
cut_p41 = "temp_p41/oven_cut.mp4"
poster_p41 = "img/poster-oven-41-desc.jpg"

print("Downloading Air Fryer Mondial Oven video...")
# Download best 720p or 1080p
subprocess.run([
    "yt-dlp", "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    "--merge-output-format", "mp4",
    "-o", raw_p41,
    video_url
], check=True)

print("Cutting dynamic 35s presentation...")
# Let's cut from 01:10 to 01:45 where the product is shown running
subprocess.run([
    "ffmpeg", "-y", "-ss", "00:01:12", "-to", "00:01:46", "-i", raw_p41,
    "-c:v", "libx264", "-preset", "fast", "-crf", "23",
    "-c:a", "aac", "-b:a", "128k",
    "-movflags", "+faststart",
    cut_p41
], check=True)

# Generate poster at 2s
subprocess.run([
    "ffmpeg", "-y", "-i", cut_p41, "-ss", "00:00:02", "-vframes", "1", poster_p41
], check=True)

print("Uploading to Catbox...")
with open(cut_p41, "rb") as f:
    r = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f}, timeout=60)
    catbox_url = r.text.strip()
    print("Catbox URL for P41 video:", catbox_url)

with open("temp_p41/catbox_url.txt", "w") as f:
    f.write(catbox_url)
