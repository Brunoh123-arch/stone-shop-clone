import os, shutil

os.makedirs('img/reviews-avatars/mulheres_validadas', exist_ok=True)

# Lista dos IDs 100% verificados visualmente com os próprios olhos de mulher_brasil
valid_mulher_brasil_ids = [
    1, 2, 7,
    29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
    42, 45, 46, 47, 48, 50, 54, 55, 56, 57, 58, 60,
    61, 62, 67, 68, 72, 73, 74, 75, 76, 77, 78, 80
]

# Lista dos IDs 100% verificados visualmente dos tt_avatars (grids 1, 2 e 3)
valid_tt_avatar_ids = [
    1, 2, 3, 6, 7, 9, 10, 13, 14, 15, 16, 18, 20,
    21, 22, 25, 26, 28, 30, 34, 35, 36, 38, 40,
    41, 42, 45, 47, 48, 49, 50, 51, 53, 58, 59, 60
]

validated_files = []

# Adiciona de mulher_brasil
for mid in valid_mulher_brasil_ids:
    src = f"img/reviews-avatars/mulheres_brasil/mulher_{mid}.jpg"
    if os.path.exists(src):
        validated_files.append(src)

# Adiciona de tt_avatar
for tid in valid_tt_avatar_ids:
    src = f"img/reviews-avatars/tiktok_real/tt_avatar_{tid}.jpg"
    if os.path.exists(src):
        validated_files.append(src)

print(f"Total de mulheres 100% validadas visualmente: {len(validated_files)}")

# Copia para img/reviews-avatars/mulheres_validadas/mulher_1.jpg ...
for i, f in enumerate(validated_files):
    dest = f"img/reviews-avatars/mulheres_validadas/mulher_{i+1}.jpg"
    shutil.copy2(f, dest)

print(f"Copiadas {len(validated_files)} fotos para img/reviews-avatars/mulheres_validadas/ com SUCESSO!")
