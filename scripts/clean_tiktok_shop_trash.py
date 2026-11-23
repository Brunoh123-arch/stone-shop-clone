import os, shutil, stat

def remove_readonly(func, path, excinfo):
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"Error deleting {path}: {e}")

tt_path = r"C:\Users\Dell\Downloads\tiktok shop"

# Exact targets to delete
folders_to_delete = [
    "videosdoscriadorespneu",
    "avaliacaodospneus",
    "videoscooterintroducao",
    "fotosavaliacaoscooter",
    "criativos_concorrente",
    "criativos_tiktok_ads",
    "scratch",
    "Temp",
    "_pages",
    "wix",
    "versions",
    os.path.join("videosprodutos", "raw")
]

# Add imagemscooter* folders
for d in os.listdir(tt_path):
    if d.startswith("imagemscooter"):
        folders_to_delete.append(d)

files_to_delete = [
    os.path.join("videosprodutos", "temp_8kmaxra3pgY.f401.mp4.part")
]

deleted_bytes = 0

for item in folders_to_delete:
    full = os.path.join(tt_path, item)
    if os.path.exists(full):
        # Calculate size before deleting
        sz = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(full) for f in fs)
        deleted_bytes += sz
        shutil.rmtree(full, onerror=remove_readonly)
        print(f"Deleted DIR: {item} ({sz / (1024*1024):.2f} MB)")

for item in files_to_delete:
    full = os.path.join(tt_path, item)
    if os.path.exists(full):
        sz = os.path.getsize(full)
        deleted_bytes += sz
        try:
            os.chmod(full, stat.S_IWRITE)
            os.remove(full)
            print(f"Deleted FILE: {item} ({sz / (1024*1024):.2f} MB)")
        except Exception as e:
            print(f"Error removing file {item}: {e}")

print(f"\nTOTAL PURGED: {deleted_bytes / (1024*1024):.2f} MB")
