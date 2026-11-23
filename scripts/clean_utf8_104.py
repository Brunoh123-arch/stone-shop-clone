with open('_pages/produto-104.html', 'rb') as f:
    raw = f.read()

# Let's decode with errors='replace'
text = raw.decode('utf-8', errors='replace')
print("Decoded length:", len(text))
with open('pages/produto-104.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Successfully wrote clean utf-8!")
