with open("pages/produto-78.html", "r", encoding="utf-8") as f:
    c = f.read()

print("Length of P78:", len(c))
print("First 1000 chars of P78:")
print(c[:1000])
