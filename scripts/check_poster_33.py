import os

poster = 'videosprodutos/posters/video-produto-33.jpg'
print("Poster exists:", os.path.exists(poster))
if os.path.exists(poster):
    print("Poster size:", os.path.getsize(poster))
