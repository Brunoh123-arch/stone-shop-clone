import os, glob

for p in [5, 61, 74]:
    print(f"=== Procurando imagens para P{p} ===")
    matches = glob.glob(f"img/*{p}*")
    print(matches[:10])
