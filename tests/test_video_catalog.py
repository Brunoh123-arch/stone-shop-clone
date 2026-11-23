import unittest
import json
import os
import re

CATALOG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config', 'products_video_catalog.json')
CATBOX_MAP_PATH = os.path.join(os.path.dirname(__file__), '..', 'catbox_video_map.json')

class TestVideoCatalog(unittest.TestCase):
    def setUp(self):
        self.catalog_path = os.path.abspath(CATALOG_PATH)
        self.map_path = os.path.abspath(CATBOX_MAP_PATH)

    def test_catalog_file_exists(self):
        self.assertTrue(os.path.exists(self.catalog_path), f"Catálogo {self.catalog_path} não encontrado")

    def test_catalog_structure_and_counts(self):
        if not os.path.exists(self.catalog_path):
            self.fail("Catálogo não existe")

        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)

        # Deve conter chave "videos" ou lista direta
        videos = catalog.get("videos", catalog) if isinstance(catalog, dict) else catalog
        self.assertIsInstance(videos, list, "O catálogo deve ser uma lista ou conter a chave 'videos' como lista")
        self.assertEqual(len(videos), 141, f"O catálogo deve conter exatamente 141 vídeos, encontrou {len(videos)}")

        catbox_url_pattern = re.compile(r"^https://files\.catbox\.moe/[a-z0-9]+\.mp4$")
        required_keys = {"namespace", "product_id", "video_id", "original_path", "catbox_url", "poster_path"}

        unique_urls = set()
        namespaces = set()

        for idx, item in enumerate(videos):
            for k in required_keys:
                self.assertIn(k, item, f"Vídeo no índice {idx} ({item.get('original_path')}) não possui o campo obrigatório '{k}'")

            url = item["catbox_url"]
            self.assertRegex(url, catbox_url_pattern, f"URL do Catbox inválida: {url}")
            unique_urls.add(url)
            namespaces.add(item["namespace"])

            # Validar que original_path tem formato normalizado
            self.assertTrue(item["original_path"].endswith(".mp4"), f"Caminho original deve ser .mp4: {item['original_path']}")

        # Validar deduplicação esperada: 136 URLs únicas para 141 caminhos
        self.assertEqual(len(unique_urls), 136, f"Esperado 136 URLs únicas do Catbox, encontrou {len(unique_urls)}")

        # Validar 48 namespaces
        self.assertEqual(len(namespaces), 48, f"Esperado 48 namespaces únicos, encontrou {len(namespaces)}")

if __name__ == '__main__':
    unittest.main()
