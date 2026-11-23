import os

mp4_files = []
for root, dirs, files in os.walk('.'):
    # skip .git, node_modules
    if '.git' in root or 'node_modules' in root or '.vercel' in root:
        continue
    for f in files:
        if f.endswith('.mp4'):
            fp = os.path.join(root, f)
            sz = os.path.getsize(fp)
            mp4_files.append((fp, sz))

print(f'Total local MP4 files in project: {len(mp4_files)}')
for fp, sz in mp4_files:
    print(f'{fp}: {sz / (1024*1024):.2f} MB')
