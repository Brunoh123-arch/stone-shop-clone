import io
import os
import tempfile
import unittest
from PIL import Image

from scripts.studio.studio_daemon import (
    resolve_and_classify_url,
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
        self.assertFalse(detect_captcha_or_verification("https://www.mercadolivre.com.br/p/MLB123", "<h1>Porta Joias</h1>"))


if __name__ == "__main__":
    unittest.main()
