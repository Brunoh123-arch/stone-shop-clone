import shutil, os

replacements = [
    ('img/reviews-avatars/curated/women/woman_1.jpg', 'img/reviews-avatars/mulheres_brasil/mulher_63.jpg'),
    ('img/reviews-avatars/curated/women/woman_22.jpg', 'img/creators-chinelo/creator-104-22.jpg'),
    ('img/reviews-avatars/curated/women/woman_19.jpg', 'img/creators-cabelo/creator-108-19.jpg'),
    ('img/reviews-avatars/curated/women/woman_39.jpg', 'img/creators-cabelo/creator-109-19.jpg'),
    ('img/reviews-avatars/curated/women/woman_4.jpg', 'img/creators-body/creator-1.jpg')
]

for src, dst in replacements:
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Copied {src} -> {dst} ({os.path.getsize(dst)} bytes)")
    else:
        print(f"Source not found: {src}")
