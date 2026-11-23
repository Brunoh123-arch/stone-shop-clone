with open('js/app.js', 'rb') as f:
    raw = f.read()

# Replace any bytes ending in dos clientes (${total})
pattern = b'dos clientes (${total})'
replacement = b'dos clientes (...'

count = raw.count(pattern)
print(f"Found {count} occurrences of {pattern}")
if count > 0:
    raw = raw.replace(pattern, replacement)
    with open('js/app.js', 'wb') as f:
        f.write(raw)
    print("SUCCESS: Replaced with raw bytes!")
else:
    print("Pattern not found in bytes.")
