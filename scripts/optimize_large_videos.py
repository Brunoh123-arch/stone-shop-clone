import subprocess
import os

targets = [
    'videosprodutos/video-produto-108-criadora4.mp4',
    'videosprodutos/video-produto-108-criadora8.mp4',
    'videosprodutos/video-produto-109-criadora22.mp4'
]

for t in targets:
    if os.path.exists(t):
        sz = os.path.getsize(t) / (1024*1024)
        print(f"Comprimindo {t} ({sz:.2f} MB)...")
        tmp = t + '.opt.mp4'
        cmd = f'ffmpeg -y -i "{t}" -c:v libx264 -crf 26 -preset fast -c:a aac -b:a 128k "{tmp}"'
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(tmp) and os.path.getsize(tmp) > 0:
            new_sz = os.path.getsize(tmp) / (1024*1024)
            os.replace(tmp, t)
            print(f"  Otimizado: {sz:.2f} MB -> {new_sz:.2f} MB")
        else:
            print(f"  FFmpeg falhou ou gerou arquivo vazio para {t}")
