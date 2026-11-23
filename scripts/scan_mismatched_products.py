import glob
import os
import re

def scan():
    files = sorted(glob.glob("pages/produto-*.html"), key=lambda p: int(re.search(r'\d+', p).group()) if re.search(r'\d+', p) else 999)
    print(f"Total files: {len(files)}")
    
    products = []
    for f in files:
        pid_m = re.search(r'produto-(\d+)\.html', f)
        pid = int(pid_m.group(1)) if pid_m else 0
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        # Get title
        title_m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_m.group(1).replace(' - Stone Shop', '').strip() if title_m else ''
        
        # Check creators
        has_creators = "creators-section" in content
        
        # Check ar condicionado videos on non-ar products
        has_ar_condicionado = "arcondicionado" in content or "Ultra Slim" in content or "10.000 BTUs" in content
        
        # Check Shopee / ML
        has_shopee = "susercontent.com" in content
        has_ml = "mlstatic.com" in content
        
        # Check Padrão
        has_padrao = bool(re.search(r'·\s*Padrão\b', content, re.IGNORECASE))
        
        # Check Table
        has_table = "<table" in content
        
        needs_fix = has_ar_condicionado or not has_creators or has_shopee or has_padrao or has_table
        
        if needs_fix:
            products.append({
                'id': pid,
                'file': f,
                'title': title[:50],
                'has_creators': has_creators,
                'has_ar': has_ar_condicionado,
                'has_shopee': has_shopee,
                'has_padrao': has_padrao,
                'has_table': has_table
            })
            
    print(f"Total que precisam de alinhamento/padronização: {len(products)}")
    print("\nPrimeiros 15 produtos críticos:")
    for p in products[:15]:
        flags = []
        if p['has_ar']: flags.append("VÍDEO_AR_CONDICIONADO_ERRADO")
        if not p['has_creators']: flags.append("SEM_CRIADORES")
        if p['has_shopee']: flags.append("IMG_SHOPEE")
        if p['has_padrao']: flags.append("VARIAÇÃO_PADRÃO")
        if p['has_table']: flags.append("TABELA_HTML")
        print(f"Produto {p['id']} ({p['title']}): {', '.join(flags)}")

if __name__ == '__main__':
    scan()
