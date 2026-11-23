txt = open('pages/produto-118.html', encoding='utf-8').read()
for line in txt.splitlines():
    if 'review-118' in line:
        print(line[:120])
