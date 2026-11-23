import unittest
import os
import glob
import re

class TestUrlReplacement(unittest.TestCase):
    def setUp(self):
        self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.mp4_pattern = re.compile(r'(\.{0,2}/)?(videosprodutos|videosdoscriadorespneu)/[^\s"\'<>]+\.mp4', re.IGNORECASE)

    def test_videos_criadores_js_has_no_local_videos(self):
        js_path = os.path.join(self.root_dir, 'js', 'videos-criadores.js')
        self.assertTrue(os.path.exists(js_path), "js/videos-criadores.js não encontrado")
        with open(js_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        matches = self.mp4_pattern.findall(content)
        self.assertEqual(len(matches), 0, f"Encontradas {len(matches)} referências locais a .mp4 em js/videos-criadores.js")
        self.assertIn("https://files.catbox.moe/", content, "js/videos-criadores.js deve conter URLs do Catbox")

    def test_pages_html_have_no_local_videos(self):
        pages = glob.glob(os.path.join(self.root_dir, 'pages', '*.html'))
        self.assertGreater(len(pages), 0, "Nenhuma página encontrada em pages/")
        violations = []
        for p in pages:
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                c = f.read()
            m = self.mp4_pattern.findall(c)
            if m:
                violations.append((os.path.basename(p), len(m)))
        self.assertEqual(violations, [], f"Páginas com referências locais a .mp4: {violations}")

    def test_underpages_html_have_no_local_videos(self):
        pages = glob.glob(os.path.join(self.root_dir, '_pages', '*.html'))
        violations = []
        for p in pages:
            with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                c = f.read()
            m = self.mp4_pattern.findall(c)
            if m:
                violations.append((os.path.basename(p), len(m)))
        self.assertEqual(violations, [], f"_pages com referências locais a .mp4: {violations}")

    def test_scripts_data_json_have_no_local_videos(self):
        json_files = glob.glob(os.path.join(self.root_dir, 'scripts', '**', '*.json'), recursive=True)
        violations = []
        ignored_names = {'catbox_video_map.json', 'products_video_catalog.json', 'purged_videos_manifest.json', 'sentinel_health_report.json'}
        for j in json_files:
            if os.path.basename(j) in ignored_names:
                continue
            with open(j, 'r', encoding='utf-8', errors='ignore') as f:
                c = f.read()
            m = self.mp4_pattern.findall(c)
            if m:
                violations.append((os.path.relpath(j, self.root_dir), len(m)))
        self.assertEqual(violations, [], f"scripts/**/*.json com referências locais a .mp4: {violations}")

if __name__ == '__main__':
    unittest.main()
