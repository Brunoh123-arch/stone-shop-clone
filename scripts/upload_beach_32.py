import os
import subprocess
import json
import time

urls = {}
for i in range(1, 33):
    rel_path = f"videosprodutos\\praia_32\\beach_{i:02d}.mp4"
    if not os.path.exists(rel_path):
        print(f"File not found: {rel_path}")
        continue
    
    cmd = [
        "curl.exe",
        "-s",
        "-F", "reqtype=fileupload",
        "-F", f"fileToUpload=@{rel_path}",
        "https://catbox.moe/user/api.php"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    out = res.stdout.strip()
    if out.startswith("https://files.catbox.moe/"):
        print(f"{i:02d}: {out}", flush=True)
        urls[f"beach_{i:02d}"] = out
    else:
        print(f"Retry {i:02d}... {out}", flush=True)
        time.sleep(1)
        res = subprocess.run(cmd, capture_output=True, text=True)
        out = res.stdout.strip()
        print(f"{i:02d} (retry): {out}", flush=True)
        if out.startswith("https://files.catbox.moe/"):
            urls[f"beach_{i:02d}"] = out

with open("beach_32_catbox_urls.json", "w", encoding="utf-8") as f:
    json.dump(urls, f, indent=2)

print(f"FINISHED! Total uploaded: {len(urls)}/32", flush=True)
