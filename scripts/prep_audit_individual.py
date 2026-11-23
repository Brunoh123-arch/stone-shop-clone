import os, glob
from PIL import Image

# Vamos criar miniaturas com número grande e borda para auditar cada uma das 75
os.makedirs('scripts/audit_thumbs', exist_ok=True)
for i in range(1, 76):
    p = f'img/reviews-avatars/mulheres_validadas/mulher_{i}.jpg'
    if os.path.exists(p):
        im = Image.open(p).convert('RGB')
        im.save(f'scripts/audit_thumbs/m_{i:02d}.jpg')

print("Todas as 75 miniaturas salvas em scripts/audit_thumbs/")
