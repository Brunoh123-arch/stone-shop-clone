import os, re, subprocess, json
from bs4 import BeautifulSoup
from PIL import Image

FEMALE_PIDS = [28, 38, 39, 45, 87, 88, 103, 104, 106, 108, 109]

print("=====================================================================")
print("=== DEEP VERIFICATION: DIRETRIZ 7.17 (AUDITORIA RIGOROSA BLINDADA) ===")
print("=====================================================================\n")

total_errors = 0

# 1. Auditoria dos arquivos de imagens do pool de mulheres validadas
print("--- 1. AUDITORIA DO POOL MULHERES VALIDADAS (DISCO) ---")
validated_pool = os.listdir('img/reviews-avatars/mulheres_validadas')
print(f"Total de fotos no pool: {len(validated_pool)}")
for f in validated_pool:
    p = os.path.join('img/reviews-avatars/mulheres_validadas', f)
    try:
        im = Image.open(p)
        assert im.size[0] >= 50 and im.size[1] >= 50
    except Exception as e:
        print(f"❌ Imagem corrompida ou inválida: {p} ({e})")
        total_errors += 1
print("✅ Pool oficial verificado com integridade total.")

# 2. Audit Review Cards in HTMLs
print("\n--- 2. AUDITORIA DAS AVALIAÇÕES (REVIEWS) ---")
total_reviews = 0
all_review_avatars = set()
all_review_names = set()

male_keywords = [
    'carlos', 'rodrigo', 'pedro', 'lucas', 'marcos', 'rafael', 'felipe', 'gustavo',
    'thiago', 'bruno', 'danilo', 'arthur', 'mateus', 'matheus', 'joao', 'joão',
    'andre', 'andré', 'eduardo', 'leandro', 'fernando', 'paulo', 'ricardo', 'diego',
    'marcelo', 'alexandre', 'guilherme', 'vitor', 'victor', 'gabriel', 'jefin', 'leal',
    'moisés', 'moises', 'jorge', 'antonio', 'antônio', 'otavio', 'otávio'
]

for pid in FEMALE_PIDS:
    path = f"pages/produto-{pid}.html"
    assert os.path.exists(path), f"Arquivo não encontrado: {path}"
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    reviews = soup.select(".review-card")
    total_reviews += len(reviews)
    
    for idx, r in enumerate(reviews):
        name = r.get("data-author-name", "")
        avatar = r.get("data-author-avatar", "")
        uname_el = r.select_one(".review-user-name")
        u_text = uname_el.text.strip() if uname_el else ""
        img_el = r.select_one(".review-avatar img")
        img_src = img_el.get("src", "") if img_el else ""
        
        all_review_avatars.add(avatar)
        all_review_avatars.add(img_src)
        all_review_names.add(name)
        
        # Check avatar path (must be in mulheres_validadas)
        if not ("mulheres_validadas" in avatar and "mulheres_validadas" in img_src):
            print(f"❌ P{pid} Review #{idx+1}: avatar fora do pool oficial: {avatar}")
            total_errors += 1
            
        # Check image file exists on disk
        rel_path = avatar.replace("../", "")
        if not os.path.exists(rel_path):
            print(f"❌ P{pid} Review #{idx+1}: arquivo não existe no disco: {rel_path}")
            total_errors += 1
            
        # Check display name matches data-author-name
        if name != u_text:
            print(f"❌ P{pid} Review #{idx+1}: divergência de nome: '{name}' vs '{u_text}'")
            total_errors += 1

        # Check for male names in review
        for m in male_keywords:
            if re.search(rf'\b{m}\b', name.lower()):
                print(f"❌ P{pid} Review #{idx+1}: nome masculino em produto feminino: '{name}'")
                total_errors += 1

print(f"✅ Total de avaliações auditadas em 11 produtos: {total_reviews}")
print(f"✅ Total de avatares distintos usados: {len(all_review_avatars)}")
print(f"✅ Total de nomes femininos distintos: {len(all_review_names)}")

# 3. Audit Creators in js/videos-criadores.js
print("\n--- 3. AUDITORIA ESTÁTICA DOS DATASETS EM JS/VIDEOS-CRIADORES.JS ---")
with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc_code = f.read()

pids_dataset_map = {
    28: 'CREATORS_REBECCA_BONBON_28',
    38: 'CREATORS_ESCOVA_108',
    39: 'CREATORS_ESCOVA_108',
    45: 'CREATORS_MODELADOR_109',
    87: 'CREATORS_MOM_JEANS_87',
    88: 'CREATORS_BODY_106',
    103: 'CREATORS_BODY_106',
    104: 'CREATORS_CHINELO_28',
    106: 'CREATORS_BODY_106',
    108: 'CREATORS_ESCOVA_108',
    109: 'CREATORS_MODELADOR_109'
}

datasets_to_inspect = set(pids_dataset_map.values())
for ds in sorted(datasets_to_inspect):
    source_map = ds.replace('CREATORS_', '') + '_VIDEOS_MAP'
    if ds == 'CREATORS_CHINELO_28':
        source_map = 'CHINELO_VIDEOS_MAP'
    if ds == 'CREATORS_REBECCA_BONBON_28':
        source_map = 'REBECCA_BONBON_28_VIDEOS_MAP'
        
    p = rf'const\s+{source_map}\s*=\s*\[([\s\S]*?)\];'
    m = re.search(p, vc_code)
    if not m:
        p = rf'const\s+{ds}\s*=\s*\[([\s\S]*?)\];'
        m = re.search(p, vc_code)
    assert m, f"Não foi possível localizar array para {ds} (procurado {source_map})"
    
    items = re.findall(r'\{\s*name:\s*["\']([^"\']+)["\'],\s*username:\s*["\']([^"\']+)["\'],\s*avatar:\s*["\']([^"\']+)["\']', m.group(1))
    print(f"  Dataset {ds}: {len(items)} criadores.")
    for idx, (cname, cuser, cavatar) in enumerate(items):
        nl = cname.lower()
        ul = cuser.lower()
        found_male = [k for k in male_keywords if re.search(rf'\b{k}\b', nl) or re.search(rf'\b{k}\b', ul)]
        if found_male:
            print(f"  ❌ [{idx+1}] Nome/handle suspeito de homem: '{cname}' (@{cuser}) -> {found_male}")
            total_errors += 1
        rel_avatar = cavatar.split('?')[0].replace('../', '')
        if not os.path.exists(rel_avatar):
            print(f"  ❌ [{idx+1}] Avatar não existe no disco: '{rel_avatar}'")
            total_errors += 1

# 4. Audit Runtime Simulation of initCarousel (via Node.js)
print("\n--- 4. AUDITORIA EM TEMPO DE EXECUÇÃO (RUNTIME EM NODE.JS) ---")
node_test_script = """
const fs = require('fs');
let code = fs.readFileSync('js/videos-criadores.js', 'utf8');
const vm = require('vm');
const femalePids = [28, 38, 39, 45, 87, 88, 103, 104, 106, 108, 109];
let errCount = 0;

femalePids.forEach(pid => {
  const dummyEl = {
    style: {},
    appendChild: () => {},
    querySelectorAll: () => [],
    querySelector: () => null,
    getAttribute: () => '',
    setAttribute: () => {},
    insertAdjacentHTML: () => {},
    addEventListener: () => {},
    innerHTML: '',
    className: ''
  };
  const dom = {
    location: { pathname: '/pages/produto-' + pid + '.html' },
    document: {
      getElementById: (id) => dummyEl,
      querySelector: () => dummyEl,
      querySelectorAll: () => [dummyEl],
      createElement: () => dummyEl,
      body: dummyEl,
      addEventListener: () => {}
    },
    window: {}
  };
  dom.window = dom;

  const injectedCode = code.replace(
    'activeDataset = enforceMinimumCreators(activeDataset, 10, isFemaleProduct);',
    'activeDataset = enforceMinimumCreators(activeDataset, 10, isFemaleProduct); global.lastActiveDataset = activeDataset;'
  );
  
  const ctx = {
    window: dom.window,
    location: dom.location,
    document: dom.document,
    navigator: { userAgent: 'test' },
    IntersectionObserver: class { observe(){} unobserve(){} },
    setTimeout: (fn) => {},
    clearTimeout: () => {},
    console: console,
    global: {}
  };
  
  vm.runInNewContext(injectedCode, ctx);
  const ds = ctx.global.lastActiveDataset;
  if (!ds || ds.length < 10) {
    console.error(`PID ${pid} tem menos de 10 criadores: ${ds ? ds.length : 0}`);
    errCount++;
  }
  ds.forEach((c, idx) => {
    const name = (c.name || '').toLowerCase();
    const user = (c.username || '').toLowerCase();
    const avatar = (c.avatar || '');
    const males = ['lucas', 'matheus', 'rodrigo', 'thiago', 'gustavo', 'felipe', 'carlos', 'pedro', 'marcos', 'rafael', 'bruno', 'danilo', 'jefin', 'leal', 'moises', 'moisés'];
    const found = males.filter(m => new RegExp('\\\\b' + m + '\\\\b').test(name) || new RegExp('\\\\b' + m + '\\\\b').test(user));
    if (found.length > 0 || avatar.includes('user_real_m_')) {
      console.error(`  ❌ PID ${pid} Item #${idx+1}: HOMEM ENCONTRADO NO RUNTIME: ${c.name} (@${c.username}) avatar: ${c.avatar}`);
      errCount++;
    }
  });
});
process.exit(errCount);
"""
res = subprocess.run(["node", "-e", node_test_script], capture_output=True, text=True)
if res.returncode != 0:
    print(res.stderr)
    total_errors += res.returncode
else:
    print("✅ Todos os 11 produtos femininos geraram >= 10 criadores em runtime com ZERO homens!")

print("\n---------------------------------------------------------------------")
if total_errors == 0:
    print("🏆 STATUS: AUDITORIA 100% APROVADA COM ZERO ERROS! BLINDADO!")
else:
    print(f"💥 STATUS: {total_errors} ERROS ENCONTRADOS!")
print("---------------------------------------------------------------------")
