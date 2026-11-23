import os, glob

all_local = glob.glob("videosprodutos/**/*.*", recursive=True)
print(f"Total files in videosprodutos: {len(all_local)}")
for f in all_local[:30]:
    print(f, os.path.getsize(f))
