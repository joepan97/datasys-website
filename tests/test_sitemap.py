import unittest
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITEMAP = ROOT / 'site' / 'sitemap.xml'
NS = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
EXPECTED_URLS = (
    'https://www.datasys.com.tw/',
    'https://www.datasys.com.tw/netapp.html',
    'https://www.datasys.com.tw/lto.html',
    'https://www.datasys.com.tw/parts.html',
    'https://www.datasys.com.tw/rental.html',
    'https://www.datasys.com.tw/security.html',
    'https://www.datasys.com.tw/ai.html',
    'https://www.datasys.com.tw/cases.html',
    'https://www.datasys.com.tw/about.html',
    'https://www.datasys.com.tw/contact.html',
    'https://www.datasys.com.tw/privacy-policy/',
    'https://www.datasys.com.tw/data-deletion/',
)


class SitemapTest(unittest.TestCase):
    def test_sitemap_contains_canonical_urls_with_lastmod_dates(self):
        root = ET.parse(SITEMAP).getroot()
        urls = root.findall('sm:url', NS)
        self.assertEqual(tuple(item.findtext('sm:loc', namespaces=NS) for item in urls), EXPECTED_URLS)
        self.assertTrue(all(item.find('sm:lastmod', NS) is not None for item in urls))
        for item in urls:
            value = item.findtext('sm:lastmod', namespaces=NS)
            self.assertIsNotNone(value)
            if value is None:
                continue
            with self.subTest(lastmod=value):
                self.assertEqual(date.fromisoformat(value).isoformat(), value)


if __name__ == '__main__':
    unittest.main()
