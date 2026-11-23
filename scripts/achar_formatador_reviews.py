import glob

for f in glob.glob('js/*.js'):
    c = open(f, encoding='utf-8', errors='ignore').read()
    if 'review-card-formatted' in c:
        print(f"Found in {f}")
        idx = c.find('review-card-formatted')
        print(c[idx-100:idx+400])
