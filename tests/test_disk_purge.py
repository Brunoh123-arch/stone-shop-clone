import unittest
import os
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MANIFEST_PATH = os.path.join(ROOT_DIR, 'data', 'purged_videos_manifest.json')
CATBOX_MAP_PATH = os.path.join(ROOT_DIR, 'catbox_video_map.json')

class TestDiskPurge(unittest.TestCase):
    def test_purged_manifest_exists_and_complete(self):
        self.assertTrue(os.path.exists(MANIFEST_PATH), f"Manifesto {MANIFEST_PATH} não encontrado")
        with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
            manifest = json.load(f)

        purged_list = manifest.get("purged_files", manifest) if isinstance(manifest, dict) else manifest
        self.assertGreaterEqual(len(purged_list), 141, f"Manifesto deve conter ao menos 141 itens purgados, encontrou {len(purged_list)}")

        total_bytes = manifest.get("metadata", {}).get("total_bytes_purged", 0)
        self.assertGreater(total_bytes, 600 * 1024 * 1024, "Espaço purgado deve ser superior a 600 MB")

    def test_no_mapped_mp4_files_remain_on_disk(self):
        with open(CATBOX_MAP_PATH, 'r', encoding='utf-8') as f:
            catbox_map = json.load(f)

        paths = [k for k in catbox_map if '/' in k or '\\' in k]
        remaining = []
        for p in paths:
            full_p = os.path.join(ROOT_DIR, p)
            if os.path.exists(full_p):
                remaining.append(p)

        self.assertEqual(remaining, [], f"Arquivos mp4 mapeados ainda presentes em disco: {remaining}")

    def test_zero_mp4_files_in_video_directories(self):
        remaining_mp4 = []
        for d in ['videosprodutos', 'videosdoscriadorespneu']:
            target_dir = os.path.join(ROOT_DIR, d)
            if os.path.exists(target_dir):
                for r, _, files in os.walk(target_dir):
                    for f in files:
                        if f.lower().endswith(('.mp4', '.webm')):
                            remaining_mp4.append(os.path.join(r, f))
        self.assertEqual(remaining_mp4, [], f"Encontrados arquivos .mp4 residuais em disco: {remaining_mp4}")

    def test_posters_and_images_preserved(self):
        # 1. videosprodutos/posters deve existir e ter posters
        posters_dir = os.path.join(ROOT_DIR, 'videosprodutos', 'posters')
        self.assertTrue(os.path.exists(posters_dir), "Diretório videosprodutos/posters/ deve existir")
        poster_files = [f for f in os.listdir(posters_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        self.assertGreater(len(poster_files), 10, "Posters em videosprodutos/posters devem ser preservados")

        # 2. img/posters-piscina deve existir e ter 32 posters
        piscina_dir = os.path.join(ROOT_DIR, 'img', 'posters-piscina')
        self.assertTrue(os.path.exists(piscina_dir), "Diretório img/posters-piscina deve existir")
        piscina_files = [f for f in os.listdir(piscina_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        self.assertGreaterEqual(len(piscina_files), 32, "Posters de piscina devem ser preservados")

        # 3. videosdoscriadorespneu/posters deve existir
        pneu_posters = os.path.join(ROOT_DIR, 'videosdoscriadorespneu', 'posters')
        self.assertTrue(os.path.exists(pneu_posters), "videosdoscriadorespneu/posters deve existir")
        pneu_files = [f for f in os.listdir(pneu_posters) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        self.assertGreaterEqual(len(pneu_files), 13, "Posters de pneu devem ser preservados")

if __name__ == '__main__':
    unittest.main()
