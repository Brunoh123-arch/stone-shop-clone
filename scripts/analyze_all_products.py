import os
import re
import glob

def analyze():
    pages = sorted(glob.glob("pages/produto-*.html"), key=lambda p: int(re.search(r'\d+', p).group()) if re.search(r'\d+', p) else 999)
    print(f"Total product pages: {len(pages)}")

    modern_104_count = 0
    missing_creators = []
    missing_desc_expand = []
    has_tables = []
    has_padrao = []
    has_shopee_ml = []
    old_reviews_structure = []

    for path in pages:
        filename = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        # Check creators
        if "creators-section" not in html and "videos-criadores" not in html:
            missing_creators.append(filename)

        # Check description expandable
        if "description-expandable" not in html and "desc-fade-overlay" not in html:
            missing_desc_expand.append(filename)

        # Check tables
        if "<table" in html:
            has_tables.append(filename)

        # Check generic "Padrão"
        if re.search(r'·\s*Padrão\b', html, re.IGNORECASE) or re.search(r'data-author-variation="Padrão"', html, re.IGNORECASE):
            has_padrao.append(filename)

        # Check Shopee / ML images
        if "susercontent.com" in html or "mlstatic.com" in html:
            has_shopee_ml.append(filename)

        # Check review card standard (like 104)
        if 'class="review-card"' not in html or 'review-user-name' not in html:
            old_reviews_structure.append(filename)

    print("\n--- DIAGNÓSTICO DO CATÁLOGO ---")
    print(f"Páginas sem seção de criadores ({len(missing_creators)}): {missing_creators[:10]}...")
    print(f"Páginas sem expansor de descrição ({len(missing_desc_expand)}): {missing_desc_expand[:10]}...")
    print(f"Páginas com tabelas HTML obsoletas ({len(has_tables)}): {has_tables[:10]}...")
    print(f"Páginas com variação genérica 'Padrão' ({len(has_padrao)}): {has_padrao[:10]}...")
    print(f"Páginas com URLs da Shopee/ML ({len(has_shopee_ml)}): {has_shopee_ml[:10]}...")
    print(f"Páginas com estrutura antiga de reviews ({len(old_reviews_structure)}): {old_reviews_structure[:10]}...")

if __name__ == "__main__":
    analyze()
