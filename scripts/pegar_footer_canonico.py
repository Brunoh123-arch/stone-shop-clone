with open("pages/produto-104.html", "r", encoding="utf-8") as f:
    c = f.read()

idx = c.find('class="reviews-section"')
# procurar onde fecha reviews-section
pos_store = c.find('<!-- SEÇÃO DA LOJA', idx)
if pos_store == -1:
    pos_store = c.find('<div class="shop-reviews-section"', idx)
if pos_store == -1:
    pos_store = c.find('<!-- BOTTOM BAR', idx)
if pos_store == -1:
    pos_store = c.find('class="bottom-bar', idx)

print("Posição encontrada:", pos_store)
if pos_store != -1:
    print("Trecho a partir da posição:")
    print(c[pos_store:pos_store+600])
