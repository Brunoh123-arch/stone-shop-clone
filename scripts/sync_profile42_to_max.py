import shutil
import os

src_profile = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data\Profile 42"
dst_profile = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max\Profile 42"

os.makedirs(dst_profile, exist_ok=True)

# Copy files
for root, dirs, files in os.walk(src_profile):
    rel = os.path.relpath(root, src_profile)
    dest_dir = os.path.join(dst_profile, rel)
    os.makedirs(dest_dir, exist_ok=True)
    for f in files:
        if f.lower().endswith(('.log', '.tmp', 'lockfile')):
            continue
        s_file = os.path.join(root, f)
        d_file = os.path.join(dest_dir, f)
        try:
            shutil.copy2(s_file, d_file)
        except Exception as e:
            pass

# Also sync Local State
ls_src = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data\Local State"
ls_dst = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max\Local State"
shutil.copy2(ls_src, ls_dst)

print("Profile 42 (kaiobrunocastro12@gmail.com) synced completely to User Data Max!")
