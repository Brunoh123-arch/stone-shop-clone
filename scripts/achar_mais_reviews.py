with open("pages/produto-56.html", "r", encoding="utf-8") as f:
    c = f.read()

idx = c.find('id="mais-reviews-56"')
print("Índice de mais-reviews-56:", idx)
if idx != -1:
    print(c[idx-50:idx+200])
