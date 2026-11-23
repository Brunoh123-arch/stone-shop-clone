import os
import sys
import unittest
import subprocess
import time
from playwright.sync_api import sync_playwright

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

class TestPlaywrightE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8802
        cls.server_proc = subprocess.Popen(
            [sys.executable, "-m", "http.server", str(cls.port), "--bind", "127.0.0.1"],
            cwd=ROOT_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(1.0)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.server_proc.terminate()
            cls.server_proc.wait(timeout=2)
        except Exception:
            cls.server_proc.kill()

    def test_produto_104_catbox_videos(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"http://127.0.0.1:{self.port}/pages/produto-104.html?test=1"
            page.goto(url, wait_until="domcontentloaded")

            # 1. Vídeo principal do produto deve vir do Catbox CDN
            main_vid = page.wait_for_selector("#tt-product-video", state="attached", timeout=5000)
            self.assertIsNotNone(main_vid)
            src = main_vid.get_attribute("src")
            self.assertTrue(src.startswith("https://files.catbox.moe/"), f"Vídeo principal deve ser Catbox: {src}")

            # 2. Carrossel de criadores deve existir no DOM
            creators_sec = page.wait_for_selector("#creators-section", state="attached", timeout=5000)
            self.assertIsNotNone(creators_sec)

            # 3. Validar que o carrossel renderizou cards de criadores
            page.wait_for_selector("#creators-section .creator-card", state="attached", timeout=5000)
            creator_cards = page.query_selector_all("#creators-section .creator-card")
            self.assertGreater(len(creator_cards), 0, "Deve haver cards de criadores renderizados")

            browser.close()

    def test_admin_sentinel_view(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            url = f"http://127.0.0.1:{self.port}/admin.html"
            page.goto(url, wait_until="domcontentloaded")

            pin_input = page.query_selector("#pinInput")
            if pin_input and pin_input.is_visible():
                pin_input.fill("stone123")
                page.keyboard.press("Enter")
                page.wait_for_timeout(200)

            page.evaluate("trocarAba('sentinel')")
            page.wait_for_timeout(200)

            # 1. Verificar se #view-sentinel está ativa
            self.assertTrue(page.evaluate("document.getElementById('view-sentinel').classList.contains('active')"))

            # 2. Verificar se os 141 cards foram renderizados
            cards_count = page.evaluate("document.querySelectorAll('#sentinelGrid > div').length")
            self.assertEqual(cards_count, 141, f"Grid do Sentinel deve ter 141 cards, encontrou {cards_count}")

            # 3. Testar busca no Sentinel
            page.evaluate("""
                document.getElementById('sentinelSearchInput').value = 'arke';
                filtrarSentinel();
            """)
            page.wait_for_timeout(100)

            filtered_count = page.evaluate("document.querySelectorAll('#sentinelGrid > div').length")
            self.assertEqual(filtered_count, 8, f"Busca por 'arke' deve retornar 8 vídeos, encontrou {filtered_count}")

            # 4. Testar modal de preview
            page.evaluate("abrirModalPreview('https://files.catbox.moe/jwkiqt.mp4', 'Teste Arke')")
            self.assertTrue(page.evaluate("document.getElementById('sentinelModalPreview').style.display === 'flex'"))

            page.evaluate("fecharModalPreview()")
            self.assertTrue(page.evaluate("document.getElementById('sentinelModalPreview').style.display === 'none'"))

            browser.close()

    def test_admin_sentinel_browser_live_scan(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Mock Catbox CDN to return fast 206 responses
            page.route("https://files.catbox.moe/**", lambda route: route.fulfill(
                status=206,
                headers={
                    "Content-Range": "bytes 0-10/2500000",
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "video/mp4"
                },
                body=b"video_bytes"
            ))

            url = f"http://127.0.0.1:{self.port}/admin.html"
            page.goto(url, wait_until="domcontentloaded")

            pin_input = page.query_selector("#pinInput")
            if pin_input and pin_input.is_visible():
                pin_input.fill("stone123")
                page.keyboard.press("Enter")
                page.wait_for_timeout(200)

            page.evaluate("trocarAba('sentinel')")
            page.wait_for_timeout(200)

            # Dispara a varredura live no browser
            page.evaluate("iniciarVarreduraBrowser()")

            # Aguardar o progresso atingir 100%
            page.wait_for_function("document.getElementById('sentinelProgressFill').style.width === '100%'", timeout=15000)

            # Verificar se o texto do progresso foi atualizado corretamente (não preso em '0%')
            progress_text = page.evaluate("document.getElementById('sentinelProgressText').textContent")
            self.assertIn("100%", progress_text, f"Texto de progresso deve conter 100%: {progress_text}")
            self.assertIn("141/141", progress_text, f"Texto de progresso deve indicar 141/141: {progress_text}")

            # Verificar KPI de taxa de sucesso atualizado
            kpi_rate = page.evaluate("document.getElementById('sentinelKpiRate').textContent")
            self.assertEqual(kpi_rate, "100%", f"Taxa de sucesso deve ser 100%: {kpi_rate}")

            browser.close()

if __name__ == '__main__':
    unittest.main()
