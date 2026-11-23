with open('js/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

idx = js.find('function formatCompactReviews')
end = js.find('function ', idx + 100)
with open('scratch/format_compact_full.txt', 'w', encoding='utf-8') as out:
    out.write(js[idx:end])

print("Wrote scratch/format_compact_full.txt")
