import subprocess
import glob
import os
import json

files = sorted(glob.glob("videosprodutos/praia/*.mp4"))
urls = {}

for f in files:
    filename = os.path.basename(f)
    print(f"Uploading {filename} to Catbox via curl.exe...")
    cmd = ["curl.exe", "-s", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{f}", "https://catbox.moe/user/api.php"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout.strip()
    if out.startswith("https://files.catbox.moe/"):
        print(f"  -> {out}")
        urls[filename] = out
    else:
        print(f"  Failed: {out} {res.stderr}")

with open("scripts/beach_catbox_urls.json", "w", encoding="utf-8") as fp:
    json.dump(urls, fp, indent=2)

print("Done! Uploaded count:", len(urls))
