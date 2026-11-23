with open("pages/produto-56.html", "r", encoding="utf-8") as f:
    c = f.read()

idx = c.find('class="review-card"')
print("Exemplo card P56:")
print(c[idx:idx+700])
