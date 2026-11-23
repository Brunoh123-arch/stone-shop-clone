import os
import hashlib

def file_hash(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

p76_hashes = {}
for i in range(1, 5):
    p = f"img/review-76-real-{i}.jpg"
    if os.path.exists(p):
        p76_hashes[p] = file_hash(p)

print("P76 hashes:", p76_hashes)

# Compare against all images in img/
for root, dirs, files in os.walk("img"):
    for file in files:
        fp = os.path.join(root, file)
        if fp in p76_hashes:
            continue
        try:
            h = file_hash(fp)
            for p76_file, p76_h in p76_hashes.items():
                if h == p76_h:
                    print(f"MATCH! {p76_file} is IDENTICAL to {fp}")
        except:
            pass
