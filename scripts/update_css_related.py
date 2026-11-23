with open('css/style.css', 'r', encoding='latin-1') as f:
    css = f.read()

count = css.count("  aspect-ratio: 1 / 1;\n")
print(f"Found {count} occurrences of 'aspect-ratio: 1 / 1;'")

css = css.replace("  aspect-ratio: 1 / 1;\n", "  /* aspect-ratio dinamico controlado pelo masonry */\n")

with open('css/style.css', 'w', encoding='latin-1') as f:
    f.write(css)

print("SUCCESS: Updated css/style.css with latin-1!")
