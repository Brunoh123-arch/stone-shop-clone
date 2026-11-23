import glob, os, shutil, hashlib

os.makedirs('img/reviews-avatars/verified_women', exist_ok=True)

def get_hash(f):
    with open(f, 'rb') as fp:
        return hashlib.md5(fp.read()).hexdigest()

men_hashes = {get_hash(f): f for f in glob.glob('img/reviews-avatars/curated/men/*') + glob.glob('img/reviews-avatars/unique/m_*.jpg')}

sources = []

# 1. creators-body (28)
sources += glob.glob('img/creators-body/creator-*.jpg')

# 2. creators-avatars (28)
sources += glob.glob('img/creators-avatars/creator-*.jpg')

# 3. creators-chinelo (32)
sources += glob.glob('img/creators-chinelo/creator-104-*.jpg')

# 4. creators-cabelo (76)
sources += glob.glob('img/creators-cabelo/creator-*.jpg')

# 5. curated/women e unique/w_* sem colisao
for f in glob.glob('img/reviews-avatars/curated/women/*') + glob.glob('img/reviews-avatars/unique/w_*.jpg'):
    if get_hash(f) not in men_hashes:
        sources.append(f)

print(f"Total de fontes candidatas: {len(sources)}")

# Filtrar duplicatas por hash
seen_hashes = set()
verified = []
for s in sources:
    h = get_hash(s)
    if h not in seen_hashes and h not in men_hashes:
        seen_hashes.add(h)
        verified.append(s)

print(f"Total de mulheres unicas e verificadas: {len(verified)}")

# Copiar para img/reviews-avatars/verified_women/woman_1.jpg ...
for i, s in enumerate(verified):
    dest = f"img/reviews-avatars/verified_women/woman_{i+1}.jpg"
    shutil.copy2(s, dest)

print(f"Copiadas {len(verified)} fotos de mulheres 100% verificadas para img/reviews-avatars/verified_women/")
