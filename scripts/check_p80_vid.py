import subprocess

# check duration and info of 3a2qhi.mp4
cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "https://files.catbox.moe/3a2qhi.mp4"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("3a2qhi info:", res.stdout)
