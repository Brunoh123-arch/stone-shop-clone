import glob
import re
import os

def main():
    # Coletar todos os avatares reais do TikTok
    tt_avatars = []

    # 1. Da pasta tiktok_real
    tt_real_dir = "img/reviews-avatars/tiktok_real"
    if os.path.exists(tt_real_dir):
        for f in sorted(os.listdir(tt_real_dir)):
            if f.endswith(".jpg") and os.path.getsize(os.path.join(tt_real_dir, f)) > 1000:
                tt_avatars.append(f"../img/reviews-avatars/tiktok_real/{f}")

    # 2. Avatares do TikTok Shop oficiais extraídos dos produtos canônicos 104 a 124
    avatars_dir = "img/reviews-avatars"
    for f in sorted(os.listdir(avatars_dir)):
        if f.startswith("review-user-1") and f.endswith(".jpg") and os.path.getsize(os.path.join(avatars_dir, f)) > 1000:
            tt_avatars.append(f"../img/reviews-avatars/{f}")

    print(f"Total de avatares autênticos do TikTok disponíveis: {len(tt_avatars)}")

    INTERNET_AVATAR_PATTERN = re.compile(
        r'(?:\.\./)?img/reviews-avatars/(?:unique/(?:w|m)_\d+|review-user-\d+)\.jpg'
    )

    files = glob.glob("pages/*.html")
    total_replaced = 0
    files_modified = 0

    for file_path in sorted(files):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        m_id = re.search(r'produto-(\d+)\.html', file_path)
        pid = int(m_id.group(1)) if m_id else 1

        offset = (pid * 7) % len(tt_avatars)
        idx = 0

        def replace_avatar(match):
            nonlocal idx
            chosen = tt_avatars[(offset + idx) % len(tt_avatars)]
            idx += 1
            return chosen

        new_content, count = INTERNET_AVATAR_PATTERN.subn(replace_avatar, content)

        if count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            total_replaced += count
            files_modified += 1
            print(f"[{pid:3d}] {file_path}: {count} avatares substituídos por avatares do TikTok")

    print(f"\nResultado final: {total_replaced} avatares de internet substituídos em {files_modified} páginas!")

if __name__ == '__main__':
    main()
