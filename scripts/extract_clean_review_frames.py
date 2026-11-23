import subprocess
import os

os.makedirs('scratch/frames_111', exist_ok=True)

# Extract frames from video_1 and video_2 of projetornatalinousb and projetorde
videos = [
    ('criativos_concorrente/1033811266480714/projetornatalinousb/video_1.mp4', 'usb1'),
    ('criativos_concorrente/1033811266480714/projetornatalinousb/video_2.mp4', 'usb2'),
    ('criativos_concorrente/1033811266480714/projetorde/video_1.mp4', 'pde1'),
    ('criativos_concorrente/1033811266480714/projetorde/video_2.mp4', 'pde2'),
]

for vpath, prefix in videos:
    for sec in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        out = f'scratch/frames_111/{prefix}_{sec}s.jpg'
        subprocess.run(['ffmpeg', '-y', '-ss', str(sec), '-i', vpath, '-vframes', '1', '-q:v', '2', out], capture_output=True)

print("Frames extracted:", len(os.listdir('scratch/frames_111')))
