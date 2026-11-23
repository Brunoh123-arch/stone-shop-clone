for pid in [78, 79, 81, 83, 84]:
    fpath = f"pages/produto-{pid}.html"
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()
    
    print(f"=== P{pid} ===")
    print("has creators-section?", "creators-section" in c)
    print("has info-row-item-protection?", "info-row-item-protection" in c)
    print("has reviews-section?", "reviews-section" in c)
    
    pos_prot = c.find("info-row-item-protection")
    if pos_prot != -1:
        print("Around protection:", c[pos_prot:pos_prot+400])
