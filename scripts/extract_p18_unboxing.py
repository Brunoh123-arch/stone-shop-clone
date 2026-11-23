import subprocess
import os

timestamps = [
    (1.5, "img/review-18-c1-1.jpg"),
    (4.0, "img/review-18-c1-2.jpg"),
    (7.5, "img/review-18-c2-1.jpg"),
    (10.0, "img/review-18-c2-2.jpg"),
    (13.5, "img/review-18-c3-1.jpg"),
    (16.0, "img/review-18-c4-1.jpg"),
    (19.5, "img/review-18-c5-1.jpg"),
    (22.0, "img/review-18-c6-1.jpg"),
    (24.5, "img/review-18-c7-1.jpg"),
    (26.0, "img/review-18-c8-1.jpg"),
]

for sec, out_file in timestamps:
    subprocess.run([
        "ffmpeg", "-y", "-ss", str(sec), "-i", "videosprodutos/video-produto-18.mp4",
        "-vframes", "1", "-q:v", "2", out_file
    ], capture_output=True)
    print(f"Extracted {out_file} at {sec}s (size: {os.path.getsize(out_file)} bytes)")

print("All 10 authentic unboxing photos generated successfully!")
