import os
import shutil
import subprocess
from PIL import Image

print("[*] Iniciando preparação de vídeos e fotos de avaliação do Produto 111...")

# 1. Copiar vídeos para videosprodutos/
videos_info = [
    {
        'src': 'scratch/real_creators/bruna_spider.mp4',
        'dest': 'videosprodutos/video-produto-111.mp4',
        'poster': 'videosprodutos/posters/poster-produto-111.jpg',
        'avatar_src': 'scratch/real_creators/avatar_bruna_spider.jpg',
        'avatar_dest': 'img/creators-auto/avatar-brukaxpp.jpg',
        'name': 'Bruna spider',
        'user': 'brukaxpp',
        'desc': 'Projetor Natalino Led Natal 16 desenhos em alta definição para parede e teto #tiktokshopbr #projetornatalino #natal'
    },
    {
        'src': 'scratch/real_creators/marcelo_mipim.mp4',
        'dest': 'videosprodutos/video-produto-111-criadora2.mp4',
        'poster': 'videosprodutos/posters/poster-produto-111-criadora2.jpg',
        'avatar_src': 'scratch/real_creators/avatar_marcelo_mipim.jpg',
        'avatar_dest': 'img/creators-auto/avatar-marceloknesh.jpg',
        'name': 'MiPim',
        'user': 'marceloknesh',
        'desc': 'Projetor natalino com 16 desenhos e alcance de projeção de até 8 metros 🎅❄️✨ #natal #decoracaodenatal #tiktokshop'
    },
    {
        'src': 'scratch/real_creators/alendica100.mp4',
        'dest': 'videosprodutos/video-produto-111-criadora3.mp4',
        'poster': 'videosprodutos/posters/poster-produto-111-criadora3.jpg',
        'avatar_src': 'scratch/real_creators/avatar_alendica100.jpg',
        'avatar_dest': 'img/creators-auto/avatar-alendica100.jpg',
        'name': 'Alê indica',
        'user': 'alendica100',
        'desc': 'Projetor Natalino Refletor Luzes de Natal Com 16 Desenhos 3D Laser Bivolt Portátil #projetornatalino #tiktokshop1111'
    },
    {
        'src': 'scratch/real_creators/kahena_rodrigues.mp4',
        'dest': 'videosprodutos/video-produto-111-criadora4.mp4',
        'poster': 'videosprodutos/posters/poster-produto-111-criadora4.jpg',
        'avatar_src': 'scratch/real_creators/avatar_kahena_rodrigues.jpg',
        'avatar_dest': 'img/creators-auto/avatar-kahenar.jpg',
        'name': 'Kahena Rodrigues',
        'user': 'kahenar',
        'desc': 'Esse projetor natalino transforma o ambiente em segundos e já deixa a casa com clima de Natal com 16 padrões #TikTokShopBR'
    }
]

os.makedirs('videosprodutos/posters', exist_ok=True)
os.makedirs('img/creators-auto', exist_ok=True)

for v in videos_info:
    shutil.copy2(v['src'], v['dest'])
    print(f"Copiado vídeo: {v['dest']}")
    
    # Gerar poster a 0.2s
    subprocess.run([
        'ffmpeg', '-y', '-ss', '00:00:00.2', '-i', v['dest'],
        '-vframes', '1', '-q:v', '2', v['poster']
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Gerado poster: {v['poster']}")
    
    if os.path.exists(v['avatar_src']):
        shutil.copy2(v['avatar_src'], v['avatar_dest'])
        print(f"Copiado avatar: {v['avatar_dest']}")

# 2. Preparar fotos reais de compradores para avaliações
# Foto 1: Sala escura com projetor no tapete e parede projetada (de vid_0)
img1 = Image.open('scratch/test_vids/vid0_f2.jpg')
# Cortar levemente as bordas (8%) para purgar qualquer artefato
w, h = img1.size
crop_box1 = (int(w * 0.05), int(h * 0.05), int(w * 0.95), int(h * 0.95))
img1_cropped = img1.crop(crop_box1)
img1_cropped.save('img/review-111-real-1.jpg', quality=92)
print("Salvo img/review-111-real-1.jpg")

# Foto 2: Mão apontando para a parede com Papai Noel e sinos (de vid_0)
img2 = Image.open('scratch/test_vids/vid0_f3.jpg')
w, h = img2.size
crop_box2 = (int(w * 0.05), int(h * 0.05), int(w * 0.95), int(h * 0.95))
img2_cropped = img2.crop(crop_box2)
img2_cropped.save('img/review-111-real-2.jpg', quality=92)
print("Salvo img/review-111-real-2.jpg")

# Foto 3: Projetor na mesa na sala iluminada (scratch/real_creators/poster_alendica100.jpg sem a parte inferior do texto)
img3 = Image.open('scratch/real_creators/poster_alendica100.jpg')
w, h = img3.size
# Cortar 12% da base para remover seta/texto
crop_box3 = (0, 0, w, int(h * 0.88))
img3_cropped = img3.crop(crop_box3)
img3_cropped.save('img/review-111-real-3.jpg', quality=92)
print("Salvo img/review-111-real-3.jpg")

# Foto 4: Projeção dos bonecos de neve e árvore no teto/parede (de vid_1 sem cabeçalho)
img4 = Image.open('scratch/test_vids/vid1_f3.jpg')
w, h = img4.size
# Cortar topo (20% para remover texto do topo) e base (15% para remover sticker)
crop_box4 = (0, int(h * 0.22), w, int(h * 0.85))
img4_cropped = img4.crop(crop_box4)
img4_cropped.save('img/review-111-real-4.jpg', quality=92)
print("Salvo img/review-111-real-4.jpg")

print("[OK] Todas as mídias e fotos reais de avaliação preparadas com sucesso!")
