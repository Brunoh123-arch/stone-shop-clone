import os
from PIL import Image

def optimize_images():
    print("=== OPTIMIZING REVIEW PHOTOS ===")
    total_before = 0
    total_after = 0
    
    # 1. Review images
    review_files = [f"img/review-109-real-{i}.jpg" for i in range(1, 7)]
    for rf in review_files:
        if os.path.exists(rf):
            sz_before = os.path.getsize(rf)
            total_before += sz_before
            with Image.open(rf) as im:
                im = im.convert("RGB")
                # Max dimension 640px
                im.thumbnail((640, 640), Image.Resampling.LANCZOS)
                im.save(rf, "JPEG", quality=80, optimize=True, progressive=True)
            sz_after = os.path.getsize(rf)
            total_after += sz_after
            print(f"Review photo {rf}: {sz_before//1024} KB -> {sz_after//1024} KB")
            
    # 2. Reviewer avatars (96x96)
    print("\n=== OPTIMIZING REVIEWER AVATARS ===")
    avatar_dir = "img/reviews-avatars"
    if os.path.exists(avatar_dir):
        for f in os.listdir(avatar_dir):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                p = os.path.join(avatar_dir, f)
                sz_before = os.path.getsize(p)
                total_before += sz_before
                with Image.open(p) as im:
                    im = im.convert("RGB")
                    im = im.resize((96, 96), Image.Resampling.LANCZOS)
                    im.save(p, "JPEG", quality=80, optimize=True)
                sz_after = os.path.getsize(p)
                total_after += sz_after
                print(f"Avatar {f}: {sz_before//1024} KB -> {sz_after//1024} KB")

    # 3. Creator avatars (96x96)
    print("\n=== OPTIMIZING CREATOR AVATARS (cabelo) ===")
    creators_dir = "img/creators-cabelo"
    if os.path.exists(creators_dir):
        for f in os.listdir(creators_dir):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                p = os.path.join(creators_dir, f)
                sz_before = os.path.getsize(p)
                total_before += sz_before
                with Image.open(p) as im:
                    im = im.convert("RGB")
                    im = im.resize((96, 96), Image.Resampling.LANCZOS)
                    im.save(p, "JPEG", quality=80, optimize=True)
                sz_after = os.path.getsize(p)
                total_after += sz_after
        print(f"Optimized all avatars in {creators_dir}")

    # 4. Creator posters (max height 640, quality 75)
    print("\n=== OPTIMIZING POSTERS FOR PRODUTO 109 ===")
    posters_dir = "videosprodutos/posters"
    if os.path.exists(posters_dir):
        for f in os.listdir(posters_dir):
            if "109" in f and f.lower().endswith(('.jpg', '.jpeg', '.png')):
                p = os.path.join(posters_dir, f)
                sz_before = os.path.getsize(p)
                total_before += sz_before
                with Image.open(p) as im:
                    im = im.convert("RGB")
                    im.thumbnail((480, 640), Image.Resampling.LANCZOS)
                    im.save(p, "JPEG", quality=75, optimize=True, progressive=True)
                sz_after = os.path.getsize(p)
                total_after += sz_after
                print(f"Poster {f}: {sz_before//1024} KB -> {sz_after//1024} KB")

    print("\n" + "="*50)
    print(f"TOTAL BEFORE: {total_before // 1024} KB ({total_before / (1024*1024):.2f} MB)")
    print(f"TOTAL AFTER:  {total_after // 1024} KB ({total_after / (1024*1024):.2f} MB)")
    saved = total_before - total_after
    print(f"SAVED:        {saved // 1024} KB ({saved / (1024*1024):.2f} MB) - {(saved/total_before)*100:.1f}% REDUCTION!")
    print("="*50)

if __name__ == "__main__":
    optimize_images()
