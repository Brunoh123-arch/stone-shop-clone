import os

for pid in [10, 27, 29, 30, 44]:
    fpath = f"pages/produto-{pid}.html"
    print(f"{fpath} exists?", os.path.exists(fpath))
