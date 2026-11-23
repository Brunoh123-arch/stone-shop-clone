import os

print("--- img/reviews-unboxing/ ---")
if os.path.exists('img/reviews-unboxing'):
    for root, dirs, files in os.walk('img/reviews-unboxing'):
        if files:
            print(root, len(files), files[:4])

print("\n--- img/portugal/ ---")
if os.path.exists('img/portugal'):
    print(os.listdir('img/portugal'))

print("\n--- img/posters-praia/ ---")
if os.path.exists('img/posters-praia'):
    print(os.listdir('img/posters-praia'))
