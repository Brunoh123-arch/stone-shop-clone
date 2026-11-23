import os
import glob

def scan_dir(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if f.endswith('.mp4') or f.endswith('.webm'):
                fp = os.path.join(root, f)
                sz = os.path.getsize(fp)
                print(f'{fp}: {sz / (1024*1024):.2f} MB')

print('=== Scanning videosprodutos ===')
scan_dir('videosprodutos')
