import os
import glob

pids = [14, 114, 118, 119, 120, 121, 122, 123]

for pid in pids:
    imgs = glob.glob(f"img/*{pid}*.*") + glob.glob(f"img/reviews/*{pid}*.*")
    print(f"P{pid} images found: {len(imgs)}")
    for img in imgs[:5]:
        print(f"  {img}")
