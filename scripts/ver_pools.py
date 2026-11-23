with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

for pool in ['POOL_ELETRO_COZINHA', 'POOL_PANELAS', 'POOL_TECH_DISPOSITIVOS']:
    idx = text.find(pool)
    if idx != -1:
        print(f"=== {pool} ===")
        print(text[idx:idx+800])
