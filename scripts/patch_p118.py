import re

file_path = 'pages/produto-118.html'
with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace review 4 avatar: review-user-real-f1-3.jpg -> ../img/reviews-avatars/unique/w_1.jpg
c = re.sub(
    r'(data-author-name="M\*\*a L\."\s+data-author-avatar=")[\.\/a-zA-Z0-9_\-\?]+(")',
    r'\g<1>../img/reviews-avatars/unique/w_1.jpg\g<2>',
    c
)
c = re.sub(
    r'(<img loading="lazy" decoding="async" src=")[^"]*review-user-real-f1-3\.jpg[^"]*(" alt="M\*\*a L\.")',
    r'\g<1>../img/reviews-avatars/unique/w_1.jpg\g<2>',
    c
)

# Replace review 7 avatar: review-user-real-f1-34.jpg -> ../img/reviews-avatars/unique/w_2.jpg
c = re.sub(
    r'(data-author-name="A\*\*e S\."\s+data-author-avatar=")[\.\/a-zA-Z0-9_\-\?]+(")',
    r'\g<1>../img/reviews-avatars/unique/w_2.jpg\g<2>',
    c
)
c = re.sub(
    r'(<img loading="lazy" decoding="async" src=")[^"]*review-user-real-f1-34\.jpg[^"]*(" alt="A\*\*e S\.")',
    r'\g<1>../img/reviews-avatars/unique/w_2.jpg\g<2>',
    c
)

# Replace review 8 avatar: review-user-real-f1-30.jpg -> ../img/reviews-avatars/unique/m_1.jpg
c = re.sub(
    r'(data-author-name="L\*\*s G\."\s+data-author-avatar=")[\.\/a-zA-Z0-9_\-\?]+(")',
    r'\g<1>../img/reviews-avatars/unique/m_1.jpg\g<2>',
    c
)
c = re.sub(
    r'(<img loading="lazy" decoding="async" src=")[^"]*review-user-real-f1-30\.jpg[^"]*(" alt="L\*\*s G\.")',
    r'\g<1>../img/reviews-avatars/unique/m_1.jpg\g<2>',
    c
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(c)

opens = len(re.findall(r'<div[\s>]', c))
closes = len(re.findall(r'</div>', c))
diff = opens - closes
print(f"P118 diff: {diff} (opens={opens}, closes={closes})")
print("P118 reviews updated successfully!")
