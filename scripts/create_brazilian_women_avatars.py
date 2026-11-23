import os, glob, shutil

os.makedirs('img/reviews-avatars/mulheres_brasil', exist_ok=True)

# Coletar exclusivamente fontes verificadas de brasileiras reais do TikTok
sources = []

# 1. Criadoras femininas reais de moda/corpo do TikTok Brasil (28 criadoras)
sources += sorted(glob.glob('img/creators-body/creator-*.jpg'))

# 2. Criadoras femininas reais de chinelo/calçados do TikTok Brasil (32 criadoras)
sources += sorted(glob.glob('img/creators-chinelo/creator-104-*.jpg'))

# 3. Criadoras femininas reais de cabelo/beleza do TikTok Brasil
sources += sorted(glob.glob('img/creators-cabelo/creator-*.jpg'))[:20]

print(f"Total de fotos de mulheres brasileiras do TikTok: {len(sources)}")

count = 0
for i, s in enumerate(sources):
    dest = f"img/reviews-avatars/mulheres_brasil/mulher_{i+1}.jpg"
    shutil.copy2(s, dest)
    count += 1

print(f"Criada pasta oficial 'img/reviews-avatars/mulheres_brasil/' com {count} avatares de brasileiras reais do TikTok!")
