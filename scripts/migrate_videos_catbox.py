import os
import re
import json
import uuid
import time
import urllib.request
from pathlib import Path

BASE_DIR = Path(r"c:\Users\Dell\Downloads\ds")
MAP_FILE = BASE_DIR / "catbox_video_map.json"

def get_code_content():
    code = ""
    for root, dirs, files in os.walk(BASE_DIR):
        if any(skip in root for skip in [".git", ".vercel", "node_modules"]):
            continue
        for f in files:
            if f.endswith((".html", ".js")):
                try:
                    with open(os.path.join(root, f), "r", encoding="utf-8", errors="ignore") as fp:
                        code += " " + fp.read()
                except:
                    pass
    return code

def find_active_videos(code):
    active = []
    target_dirs = [BASE_DIR / "videosprodutos", BASE_DIR / "videosdoscriadorespneu"]
    for td in target_dirs:
        if not td.exists():
            continue
        for root, dirs, files in os.walk(td):
            for f in files:
                if f.lower().endswith(".mp4"):
                    full_p = Path(root) / f
                    rel_p = full_p.relative_to(BASE_DIR).as_posix()
                    base_n = f
                    # check if either relative path or basename is present in code
                    if rel_p in code or base_n in code:
                        active.append({
                            "rel": rel_p,
                            "base": base_n,
                            "full": str(full_p),
                            "size": full_p.stat().st_size
                        })
    return active

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    boundary = uuid.uuid4().hex
    filename = Path(file_path).name
    
    with open(file_path, "rb") as fp:
        file_bytes = fp.read()
    
    header = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
        f"fileupload\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"\r\n'
        f"Content-Type: video/mp4\r\n\r\n"
    ).encode("utf-8")
    
    footer = f"\r\n--{boundary}--\r\n".encode("utf-8")
    body = header + file_bytes + footer
    
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "Mozilla/5.0"
        }
    )
    
    with urllib.request.urlopen(req, timeout=120) as resp:
        res = resp.read().decode("utf-8").strip()
        if res.startswith("https://files.catbox.moe/"):
            return res
        raise Exception(f"Catbox error: {res}")

def main():
    print("Mapeando arquivos de código...")
    code = get_code_content()
    active_videos = find_active_videos(code)
    print(f"Total de vídeos MP4 ativos no código: {len(active_videos)}")
    
    # Load existing map if any
    vmap = {}
    if MAP_FILE.exists():
        try:
            with open(MAP_FILE, "r", encoding="utf-8") as fp:
                vmap = json.load(fp)
        except:
            vmap = {}
            
    print(f"Vídeos já mapeados anteriormente: {len(vmap)}")
    
    # Upload loop with retries
    success = 0
    errors = 0
    for idx, v in enumerate(active_videos, 1):
        rel = v["rel"]
        base = v["base"]
        full = v["full"]
        size_mb = v["size"] / (1024 * 1024)
        
        if rel in vmap and vmap[rel].startswith("https://files.catbox.moe/"):
            continue
            
        print(f"[{idx}/{len(active_videos)}] Subindo: {rel} ({size_mb:.2f} MB)...", end=" ", flush=True)
        uploaded = False
        for attempt in range(3):
            try:
                c_url = upload_to_catbox(full)
                vmap[rel] = c_url
                vmap[base] = c_url
                # Save incremental map
                with open(MAP_FILE, "w", encoding="utf-8") as fp:
                    json.dump(vmap, fp, indent=2)
                print(f"OK -> {c_url}")
                uploaded = True
                success += 1
                time.sleep(0.5)
                break
            except Exception as e:
                print(f"Tentativa {attempt+1} falhou ({e})...", end=" ", flush=True)
                time.sleep(2)
        if not uploaded:
            print("FALHA DEFINITIVA")
            errors += 1

    print("\nUploads concluídos!")
    print(f"Sucessos no mapa: {len(vmap)}")
    print(f"Erros: {errors}")

if __name__ == "__main__":
    main()
