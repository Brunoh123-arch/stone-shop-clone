import re

# Substituições exatas por arquivo
replacements = {
    "pages/produto-118.html": [
        ("../img/reviews-avatars/review-user-118-c1.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_80.jpg"),
        ("../img/reviews-avatars/review-user-118-c2.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_170.jpg"),
        ("../img/reviews-avatars/review-user-118-c3.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_81.jpg"),
    ],
    "pages/produto-119.html": [
        ("../img/reviews-avatars/review-user-119-c1.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_82.jpg"),
        ("../img/reviews-avatars/review-user-119-c2.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_171.jpg"),
        ("../img/reviews-avatars/review-user-119-c3.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_83.jpg"),
    ],
    "pages/produto-120.html": [
        ("../img/reviews-avatars/review-user-120-c1.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_172.jpg"),
        ("../img/reviews-avatars/review-user-120-c2.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_84.jpg"),
        ("../img/reviews-avatars/review-user-120-c3.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_173.jpg"),
    ],
    "pages/produto-121.html": [
        ("../img/reviews-avatars/tiktok_real/user_real_m_01.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_160.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_f_01.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_70.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_m_02.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_161.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_f_02.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_71.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_m_03.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_162.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_f_03.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_72.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_m_04.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_164.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_f_04.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_74.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_m_05.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_163.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_f_05.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_76.jpg"),
        ("../img/reviews-avatars/tiktok_real/user_real_m_06.jpg", "../img/reviews-avatars/tiktok_real/tt_avatar_165.jpg"),
    ],
    "pages/produto-122.html": [
        ("../img/reviews-avatars/review-user-122-c1.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_174.jpg"),
        ("../img/reviews-avatars/review-user-122-c2.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_85.jpg"),
        ("../img/reviews-avatars/review-user-122-c3.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_175.jpg"),
    ],
    "pages/produto-123.html": [
        ("../img/reviews-avatars/review-user-123-c1.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_176.jpg"),
        ("../img/reviews-avatars/review-user-123-c2.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_177.jpg"),
        ("../img/reviews-avatars/review-user-123-c3.jpg?v=2", "../img/reviews-avatars/tiktok_real/tt_avatar_178.jpg"),
    ],
}

for filepath, pairs in replacements.items():
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    count = 0
    for old_val, new_val in pairs:
        if old_val in content:
            content = content.replace(old_val, new_val)
            count += 1
    
    # Remover onerror que apontava para review-user-1.jpg em P121
    if "produto-121.html" in filepath:
        content = re.sub(r'\s*onerror=["\']this\.src=[\'"][^"\']*review-user-1\.jpg[\'"]["\']', '', content)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Sucesso: {filepath} atualizado com {count} avatares substituídos!")

print("\nTodos os avatares residuais foram 100% padronizados!")
