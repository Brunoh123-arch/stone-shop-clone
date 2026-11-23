import pypdf
import json

reader = pypdf.PdfReader('C:/Users/Dell/.gemini/antigravity/brain/626aa811-f9a0-4dad-af48-4ab6e56722e5/.user_uploaded/media_1795138492162_2652d6ee.pdf')
print(f'Total pages: {len(reader.pages)}')

text_by_page = []
for i, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    text_by_page.append(f'--- PAGE {i+1} ---\n' + txt)

full_pdf_text = '\n'.join(text_by_page)
with open('scripts/pdf_extracted.txt', 'w', encoding='utf-8') as f:
    f.write(full_pdf_text)

print('Extracted successfully. Length:', len(full_pdf_text))
print('First 1000 chars:')
print(full_pdf_text[:1000])
