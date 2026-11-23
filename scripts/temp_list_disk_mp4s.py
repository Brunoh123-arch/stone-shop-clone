import glob, os

mp4s = glob.glob("videosprodutos/**/*.mp4", recursive=True) + glob.glob("**/*.mp4", recursive=True)
print(f"Total mp4s on disk: {len(mp4s)}")
for m in sorted(set(mp4s)):
    print(f"{m} ({os.path.getsize(m)} bytes)")
