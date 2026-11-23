for pid in [78, 79, 81, 83, 84]:
    fpath = f"pages/produto-{pid}.html"
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    print(f"P{pid} redirect content:")
    print(c)
    print("="*40)
