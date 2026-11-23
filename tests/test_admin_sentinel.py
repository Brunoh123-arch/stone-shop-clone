import unittest
import os
import re

ADMIN_PATH = os.path.join(os.path.dirname(__file__), '..', 'admin.html')

class TestAdminSentinel(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(ADMIN_PATH), "admin.html não encontrado")
        with open(ADMIN_PATH, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def test_nav_buttons_present(self):
        self.assertIn("trocarAba('sentinel')", self.content, "Botão desktop para trocarAba('sentinel') deve existir")
        self.assertIn("Sentinel CDN", self.content, "Label Sentinel CDN deve estar no menu")

    def test_view_sentinel_section_present(self):
        self.assertIn('id="view-sentinel"', self.content, "Seção #view-sentinel deve existir no DOM")
        self.assertIn('sentinelKpiTotal', self.content, "KPI Total deve existir")
        self.assertIn('sentinelKpiRate', self.content, "KPI Rate deve existir")
        self.assertIn('sentinelKpiLatency', self.content, "KPI Latency deve existir")
        self.assertIn('sentinelKpiSavings', self.content, "KPI Savings deve existir")
        self.assertIn('sentinelGrid', self.content, "Grid de vídeos deve existir")
        self.assertIn('sentinelNamespaceFilter', self.content, "Filtro de namespace deve existir")
        self.assertIn('sentinelSearchInput', self.content, "Campo de busca deve existir")

    def test_javascript_functions_present(self):
        self.assertIn('carregarSentinelReport', self.content, "Função carregarSentinelReport deve existir")
        self.assertIn('renderizarSentinel', self.content, "Função renderizarSentinel deve existir")
        self.assertIn('iniciarVarreduraBrowser', self.content, "Função iniciarVarreduraBrowser deve existir")
        self.assertIn('data/sentinel_health_report.json', self.content, "Deve consumir data/sentinel_health_report.json")

if __name__ == '__main__':
    unittest.main()
