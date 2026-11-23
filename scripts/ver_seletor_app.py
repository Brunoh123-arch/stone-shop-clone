with open('js/app.js', encoding='utf-8') as f:
    text = f.read()

idx = text.find("photosContainer.querySelectorAll('img.review-photo")
if idx != -1:
    print("Found selector at", idx)
    print(text[idx-50:idx+200])
else:
    print("Selector not found!")
