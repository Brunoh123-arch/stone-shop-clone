import shutil
import os

print("--- Updating Avatars for Produto 124 ---")
# 124 Avatars
src_juliana = 'img/avatars-churras/creator-juliana.jpg'
src_camilav = 'img/avatars-mesa/creator-camilav.jpg'
src_bruno_cand = 'img/reviews-avatars/review-user-117-c2.jpg'

for repo in ['c:/Users/Dell/Downloads/ds', 'c:/Users/Dell/Downloads/stone_shop_clone']:
    target_dir = os.path.join(repo, 'img/reviews-avatars')
    shutil.copy(src_juliana, os.path.join(target_dir, 'review-user-124-c1.jpg'))
    shutil.copy(src_juliana, os.path.join(target_dir, 'review-user-124-mariana.jpg'))
    
    shutil.copy(src_camilav, os.path.join(target_dir, 'review-user-124-c2.jpg'))
    shutil.copy(src_camilav, os.path.join(target_dir, 'review-user-124-camila.jpg'))
    
    shutil.copy(src_bruno_cand, os.path.join(target_dir, 'review-user-124-c3.jpg'))
    shutil.copy(src_bruno_cand, os.path.join(target_dir, 'review-user-124-bruno.jpg'))

print("Updated 124 avatars in ds and stone_shop_clone")

print("\n--- Updating Avatars for Produto 119 ---")
# 119 Avatars (Authentic Brazilian mothers on TikTok)
src_leticia = 'img/reviews-avatars/review-user-115-c2.jpg'
src_mariana_v = 'img/avatars-churras/creator-larissa.jpg'
src_priscila = 'img/reviews-avatars/review-user-107-c1.jpg'

for repo in ['c:/Users/Dell/Downloads/ds', 'c:/Users/Dell/Downloads/stone_shop_clone']:
    target_dir = os.path.join(repo, 'img/reviews-avatars')
    shutil.copy(src_leticia, os.path.join(target_dir, 'review-user-119-c1.jpg'))
    shutil.copy(src_mariana_v, os.path.join(target_dir, 'review-user-119-c2.jpg'))
    shutil.copy(src_priscila, os.path.join(target_dir, 'review-user-119-c3.jpg'))

print("Updated 119 avatars in ds and stone_shop_clone")
