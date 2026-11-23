import os
import json
import re
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CATBOX_MAP_PATH = os.path.join(ROOT_DIR, 'catbox_video_map.json')
BEACH_MAP_PATH = os.path.join(ROOT_DIR, 'scripts', 'beach_catbox_urls.json')

def load_catbox_maps():
    with open(CATBOX_MAP_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mapping = {}
    for k, v in data.items():
        norm_k = k.replace('\\', '/')
        mapping[norm_k] = v
        mapping[os.path.basename(norm_k)] = v

    # Mescla URLs de praia se existirem
    if os.path.exists(BEACH_MAP_PATH):
        try:
            with open(BEACH_MAP_PATH, 'r', encoding='utf-8') as bf:
                beach_data = json.load(bf)
                for k, v in beach_data.items():
                    mapping[k] = v
                    mapping[f"videosprodutos/praia/{k}"] = v
                    mapping[f"../videosprodutos/praia/{k}"] = v
        except Exception:
            pass

    return mapping

def migrate_file(file_path, catbox_map):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original_content = content
    replacement_count = 0

    # Padrão regex permitindo espaços no nome do arquivo (ex: WhatsApp Video...)
    pattern = re.compile(r'(\.{0,2}/)?(videosprodutos|videosdoscriadorespneu)/([^"\'<>\?]+?\.(?:mp4|webm))(\?[^"\'<>]*)?', re.IGNORECASE)

    def replacer(match):
        nonlocal replacement_count
        folder = match.group(2)
        rel_subpath = match.group(3)
        full_subpath = f"{folder}/{rel_subpath}".replace('\\', '/')
        filename = os.path.basename(rel_subpath)

        target_url = None
        if full_subpath in catbox_map:
            target_url = catbox_map[full_subpath]
        elif filename in catbox_map:
            target_url = catbox_map[filename]

        if target_url:
            replacement_count += 1
            return target_url
        else:
            return match.group(0)

    new_content = pattern.sub(replacer, content)

    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return replacement_count
    return 0

def update_scripts_data(catbox_map):
    files = glob.glob(os.path.join(ROOT_DIR, 'scripts', '**', '*.json'), recursive=True)
    updated = 0
    for f in files:
        # Pular arquivos mestres
        if os.path.basename(f) in ['catbox_video_map.json', 'products_video_catalog.json', 'purged_videos_manifest.json', 'sentinel_health_report.json']:
            continue
        try:
            with open(f, 'r', encoding='utf-8') as jf:
                d = json.load(jf)
            changed = False

            def process_entry(c):
                nonlocal changed
                if not isinstance(c, dict):
                    return
                # Se localVideo contém videosprodutos ou videosdoscriadorespneu
                for key in ['localVideo', 'video']:
                    if key in c and isinstance(c[key], str) and any(k in c[key] for k in ['videosprodutos', 'videosdoscriadorespneu']):
                        filename = os.path.basename(c[key])
                        clean_path = c[key].lstrip('./')
                        if clean_path in catbox_map:
                            c[key] = catbox_map[clean_path]
                            changed = True
                        elif filename in catbox_map:
                            c[key] = catbox_map[filename]
                            changed = True
                        elif c.get('video') and 'catbox' in c['video']:
                            c[key] = c['video']
                            changed = True

            if isinstance(d, dict) and 'creators' in d and isinstance(d['creators'], list):
                for c in d['creators']:
                    process_entry(c)
            elif isinstance(d, list):
                for item in d:
                    process_entry(item)

            if changed:
                with open(f, 'w', encoding='utf-8') as out:
                    json.dump(d, out, indent=2, ensure_ascii=False)
                updated += 1
        except Exception as e:
            print(f"Erro em {f}: {e}")
    print(f"scripts json datasets atualizados: {updated} arquivos.")

def update_videos_criadores_js_dedications(catbox_map):
    js_path = os.path.join(ROOT_DIR, 'js', 'videos-criadores.js')
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Mapear video-produto-X
    dedicated_dict = {}
    for k, v in catbox_map.items():
        if 'video-produto-' in k:
            m = re.search(r'video-produto-(\d+)', k)
            if m:
                dedicated_dict[int(m.group(1))] = v

    dedicated_json = json.dumps(dedicated_dict, indent=4)

    # Substituir no bloco dynamic add
    old_block = 'add(`../videosprodutos/video-produto-${prodId}.mp4`);'
    new_block = f"""const DEDICATED_CATBOX_VIDEOS = {dedicated_json};
    if (prodId && DEDICATED_CATBOX_VIDEOS[prodId]) {{
      add(DEDICATED_CATBOX_VIDEOS[prodId]);
    }}"""

    if old_block in content:
        content = content.replace(old_block, new_block)
        print("Substituído fallback dinâmico de video-produto-${prodId} em js/videos-criadores.js")

    # Ajustar PNEU_POSTERS para não depender de replace em PNEU_VIDEOS
    old_pneu_posters = "const PNEU_POSTERS = PNEU_VIDEOS.map(v => v.replace('/videosdoscriadorespneu/', '/videosdoscriadorespneu/posters/').replace('.mp4', '.jpg'));"
    new_pneu_posters = """const PNEU_POSTER_FILES = [
    "WhatsApp Video 2026-07-27 at 19.36.22.jpg", "WhatsApp Video 2026-07-27 at 19.36.26.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.27.jpg", "WhatsApp Video 2026-07-27 at 19.36.32.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.35.jpg", "WhatsApp Video 2026-07-27 at 19.36.40.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.41.jpg", "WhatsApp Video 2026-07-27 at 19.36.43.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.48.jpg", "WhatsApp Video 2026-07-27 at 19.36.52.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.53.jpg", "WhatsApp Video 2026-07-27 at 19.37.01.jpg",
    "WhatsApp Video 2026-07-27 at 19.37.04.jpg"
  ];
  const PNEU_POSTERS = PNEU_POSTER_FILES.map(f => (isPagesDir ? '../' : '') + 'videosdoscriadorespneu/posters/' + f);"""

    if old_pneu_posters in content:
        content = content.replace(old_pneu_posters, new_pneu_posters)
        print("Ajustado PNEU_POSTERS em js/videos-criadores.js")

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(content)

def run_migration():
    catbox_map = load_catbox_maps()
    print(f"Mapa do Catbox carregado com {len(catbox_map)} chaves indexadas.")

    update_videos_criadores_js_dedications(catbox_map)
    update_scripts_data(catbox_map)

    files_to_check = set()
    for js_file in glob.glob(os.path.join(ROOT_DIR, 'js', '**', '*.js'), recursive=True):
        files_to_check.add(js_file)
    for page in glob.glob(os.path.join(ROOT_DIR, 'pages', '**', '*.html'), recursive=True):
        files_to_check.add(page)
    for page in glob.glob(os.path.join(ROOT_DIR, '_pages', '**', '*.html'), recursive=True):
        files_to_check.add(page)
    for j in glob.glob(os.path.join(ROOT_DIR, 'scripts', '**', '*.json'), recursive=True):
        if os.path.basename(j) not in ['catbox_video_map.json', 'products_video_catalog.json', 'purged_videos_manifest.json', 'sentinel_health_report.json']:
            files_to_check.add(j)
    for root_html in glob.glob(os.path.join(ROOT_DIR, '*.html')):
        files_to_check.add(root_html)

    total_replacements = 0
    modified_files = 0
    for fp in sorted(files_to_check):
        count = migrate_file(fp, catbox_map)
        if count > 0:
            modified_files += 1
            total_replacements += count
            print(f"  [OK] {os.path.relpath(fp, ROOT_DIR)}: {count} substituições realizadas")

    print("=" * 60)
    print(f"MIGRAÇÃO CONCLUÍDA:")
    print(f"Arquivos modificados: {modified_files}")
    print(f"Total de referências adicionais substituídas: {total_replacements}")

if __name__ == '__main__':
    run_migration()
