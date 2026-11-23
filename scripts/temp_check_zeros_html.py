for pid in [7, 35, 76, 82, 98]:
    fpath = f"pages/produto-{pid}.html"
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    import re
    vids = re.findall(r'https?://[^\s"\'<>]+\.mp4', c)
    print(f"P{pid} videos in HTML: {vids}")
