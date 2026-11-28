import io
import os
import tempfile
import unittest
from PIL import Image

from scripts.studio.studio_daemon import (
    resolve_and_classify_url,
    parse_tiktok_share_redirect,
    build_clean_pt_search_query,
    clean_review_text,
    is_person_creator_handle,
    pad_image_1to1_webp,
    detect_captcha_or_verification,
)


class StudioDaemonHelpersTest(unittest.TestCase):
    def test_classify_urls_including_short_links_without_network(self):
        _, kind1 = resolve_and_classify_url("https://produto.mercadolivre.com.br/MLB-123456-teste-_JM", follow_redirects=False)
        _, kind2 = resolve_and_classify_url("https://shop.tiktok.com/br/pdp/1738506652937389299", follow_redirects=False)
        _, kind3 = resolve_and_classify_url("https://www.tiktok.com/@maria.silva/video/741234567890", follow_redirects=False)
        _, kind4 = resolve_and_classify_url("https://www.tiktok.com/@maria.silva/video/741234567890?product=1", follow_redirects=False)
        _, kind5 = resolve_and_classify_url("https://mercadolivre.com.br/sec/2AbCdEf", follow_redirects=False)
        self.assertEqual(kind1, "mercadolivre")
        self.assertEqual(kind2, "tiktok_shop")
        self.assertEqual(kind3, "tiktok_video")
        self.assertEqual(kind4, "tiktok_video")
        self.assertEqual(kind5, "mercadolivre")

    def test_clean_review_text_filters_shopee_and_competitor_jargon(self):
        self.assertIsNone(clean_review_text("Comprei só pra ganhar moedas na shopee"))
        self.assertIsNone(clean_review_text("Qualidade do produto: boa\nParecido com anúncio: sim"))
        self.assertEqual(clean_review_text("Chegou super bem embalado e funcionando perfeitamente!"), "Chegou super bem embalado e funcionando perfeitamente!")

    def test_is_person_creator_handle_blocks_stores(self):
        self.assertFalse(is_person_creator_handle("achadinhos.da.lu", "Achadinhos Oficial"))
        self.assertFalse(is_person_creator_handle("megastorebr", "Mega Store"))
        self.assertFalse(is_person_creator_handle("tech.brasil", "Tech Brasil"))
        self.assertTrue(is_person_creator_handle("camila.oliveira92", "Camila Oliveira"))

    def test_pad_image_1to1_webp_outputs_exact_1000x1000(self):
        img = Image.new("RGB", (600, 900), (220, 40, 60))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "slide.webp")
            pad_image_1to1_webp(buf.getvalue(), out, size=1000)
            with Image.open(out) as res:
                self.assertEqual(res.size, (1000, 1000))

    def test_detect_captcha_halts_immediately(self):
        self.assertTrue(detect_captcha_or_verification("https://www.mercadolivre.com.br/gz/account-verification", "<html></html>"))
        self.assertTrue(detect_captcha_or_verification("https://shop.tiktok.com/br/pdp/123", "<div>Verify you are human</div>"))
        self.assertTrue(
            detect_captcha_or_verification(
                "https://shop.tiktok.com/view/product/1731634476484232690?region=BR",
                "<html><head><title>Security Check</title></head><body>Verify to continue: Drag the puzzle piece into place</body></html>",
            )
        )
        self.assertFalse(detect_captcha_or_verification("https://www.mercadolivre.com.br/p/MLB123", "<h1>Porta Joias</h1>"))

    def test_parse_tiktok_share_redirect_extracts_product_og_and_seed_video(self):
        sample_redirect = (
            "https://www.tiktok.com/login?redirect_url=https%253A%252F%252Fwww.tiktok.com%252Fview%252Fproduct%252F"
            "1731634476484232690%253F_svg%253D2%2526og_info%253D%25257B%252522title%252522%25253A%252522Luzes%252BDo%252BNorte%252B"
            "Estrelado%252BL%2525C3%2525A2mpada%252BProjetor%252BLED%252BAtmosfera%252BLuz%252BNoite%252BAura%252BAurora%252B"
            "Brilhante%252BPara%252BQuarto%252BFesta%252BDecora%2525C3%2525A7%2525C3%2525A3o%252522%25252C%252522image%252522%25253A"
            "%252522https%25253A%25252F%25252Fp16-oec-sg.ibyteimg.com%25252Ftos-alisg-i-aphluv4xwc-sg%25252Fbbcabd34d1984c2eb90a5a83fd7fd9e3"
            "~tplv-aphluv4xwc-resize-png%25253A630%25253A630.png%252522%25257D%2526trackParams%253D%25257B%252522traffic_source_list%252522"
            "%25253A%25255B6%25255D%25252C%252522group_id%252522%25253A%2525227686679229957803285%252522%25257D%2526unique_id%253Dalvinnxd2"
        )
        meta = parse_tiktok_share_redirect(sample_redirect)
        self.assertEqual(meta["product_id"], "1731634476484232690")
        self.assertEqual(meta["canonical_pdp_url"], "https://shop.tiktok.com/view/product/1731634476484232690?region=BR&locale=pt-BR")
        self.assertIn("Projetor LED", meta["title"])
        self.assertIn("Aurora", meta["title"])
        self.assertTrue(meta["hero_image"].startswith("https://p16-oec-sg.ibyteimg.com/"))
        self.assertEqual(meta["seed_video_url"], "https://www.tiktok.com/@alvinnxd2/video/7686679229957803285")

    def test_build_clean_pt_search_query_keeps_core_product_nouns(self):
        q = build_clean_pt_search_query(
            "Luzes Do Norte Estrelado Lâmpada Projetor LED Atmosfera Luz Noite Aura Aurora Brilhante Para Quarto Festa Decoração"
        )
        self.assertIn("projetor", q.lower())
        self.assertIn("led", q.lower())
        self.assertIn("aurora", q.lower())
        self.assertLessEqual(len(q.split()), 6)


if __name__ == "__main__":
    unittest.main()
