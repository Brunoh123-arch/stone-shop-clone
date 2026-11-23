import os, shutil
from PIL import Image

# Lista de 51 mulheres originais aprovadas
orig_approved = [
    4, 5, 6, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 28, 30, 31, 32, 33, 34, 35,
    36, 37, 38, 39, 40, 41, 42, 43, 46, 48,
    50, 54, 55, 57, 58, 59, 60, 61, 62, 63,
    64, 65, 66, 68, 69, 70, 71, 72, 73, 74, 75
]

# Lista de 24 mulheres adicionais auditadas de tiktok_real
tt_approved = [
    'tt_avatar_131.jpg', 'tt_avatar_133.jpg', 'tt_avatar_134.jpg', 'tt_avatar_135.jpg',
    'tt_avatar_136.jpg', 'tt_avatar_137.jpg', 'tt_avatar_139.jpg', 'tt_avatar_14.jpg',
    'tt_avatar_142.jpg', 'tt_avatar_145.jpg', 'tt_avatar_150.jpg', 'tt_avatar_151.jpg',
    'tt_avatar_152.jpg', 'tt_avatar_154.jpg', 'tt_avatar_158.jpg', 'tt_avatar_159.jpg',
    'tt_avatar_16.jpg', 'tt_avatar_190.jpg', 'tt_avatar_191.jpg', 'tt_avatar_192.jpg',
    'tt_avatar_193.jpg', 'tt_avatar_194.jpg', 'tt_avatar_195.jpg', 'tt_avatar_197.jpg'
]

# Pasta de saida
target_dir = 'img/reviews-avatars/mulheres_validadas'
temp_dir = 'scripts/mulheres_curadas_temp'
os.makedirs(temp_dir, exist_ok=True)

# Coletar todas as 75 imagens reais
all_paths = []
for idx in orig_approved:
    src = f'{target_dir}/mulher_{idx}.jpg'
    all_paths.append(src)

for name in tt_approved:
    src = f'img/reviews-avatars/tiktok_real/{name}'
    all_paths.append(src)

print(f"Total de mulheres selecionadas: {len(all_paths)}")

# Copiar e padronizar para tamanho 150x150 JPEG
for i, src in enumerate(all_paths, 1):
    dst = f'{temp_dir}/mulher_{i}.jpg'
    try:
        im = Image.open(src).convert('RGB')
        im = im.resize((150, 150), Image.Resampling.LANCZOS)
        im.save(dst, quality=92)
    except Exception as e:
        print(f"Erro em {src}: {e}")

# Agora substituir na pasta oficial
for i in range(1, 76):
    src = f'{temp_dir}/mulher_{i}.jpg'
    dst = f'{target_dir}/mulher_{i}.jpg'
    shutil.copy2(src, dst)

print("75 mulheres 100% reais, auditadas e sem homens/logos instaladas com sucesso em mulheres_validadas!")
