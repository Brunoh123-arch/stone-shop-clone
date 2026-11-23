import glob, os

posters = glob.glob("videosprodutos/posters/*.*")
print(f"Total posters: {len(posters)}")
for p in sorted(posters):
    name = os.path.basename(p)
    if any(k in name for k in ['7', '5', '35', '76', '82', '98', 'aiwa', 'jbl']):
        print(name)
