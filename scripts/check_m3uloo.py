import subprocess

# Check if there are subtitles or description
cmd = ["ffprobe", "-v", "error", "-show_entries", "format_tags=comment,description,title", "-of", "default=noprint_wrappers=1", "https://files.catbox.moe/m3uloo.mp4"]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Tags:", res.stdout)

# Check scripts mentioning m3uloo
for f in ["scripts/update_all_missing_creators.py", "scripts/sanitize_p16_creators.py"]:
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
        for line in content.splitlines():
            if "m3uloo" in line:
                print("In", f, ":", line[:120])
