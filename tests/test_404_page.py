import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'netapp.html', 'lto.html', 'parts.html', 'rental.html', 'security.html', 'ai.html', 'cases.html', 'about.html', 'contact.html')


class NotFoundPageTest(unittest.TestCase):
    def test_404_template_has_sitewide_shell_and_required_content(self):
        html = (ROOT / '404.html').read_text(encoding='utf-8')
        self.assertIn('<title>找不到頁面｜元僑科技</title>', html)
        self.assertIn('<meta name="robots" content="noindex">', html)
        self.assertIn('找不到這個頁面', html)
        self.assertIn('02-2697-3311', html)
        self.assertIn('<header>', html)
        self.assertIn('<footer>', html)
        self.assertNotRegex(html, r'(?i)<link[^>]+canonical|<meta[^>]+(?:property="og:|name="twitter:)|application/ld\+json')

    def test_404_template_uses_root_relative_local_assets_and_links(self):
        html = (ROOT / '404.html').read_text(encoding='utf-8')
        for attr, value in __import__('re').findall(r'\b(href|src)="([^"]+)"', html):
            if value.startswith(('https://', 'http://', 'tel:', 'mailto:', '#', '/')):
                continue
            self.fail(f'{attr} must be root-relative or external: {value}')

    def test_build_404_only_updates_deployable_404_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'generated'
            subprocess.run(
                [sys.executable, str(ROOT / 'build.py'), '404.html', '--output', str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual((output / '404.html').read_text(encoding='utf-8'), (ROOT / '404.html').read_text(encoding='utf-8'))

    def test_server_config_snippet_contains_required_directives(self):
        config = (ROOT / 'server-config-snippet.conf').read_text(encoding='utf-8')
        self.assertIn('error_page 404 /404.html;', config)
        self.assertIn('location = /404.html { internal; }', config)
        self.assertIn('try_files $uri $uri.html $uri/ =404;', config)
        self.assertIn('server_tokens off;', config)


class LogoMarkupTest(unittest.TestCase):
    def test_all_primary_pages_have_well_formed_logo_image_markup(self):
        expected = '<img src="image/datasys-logo.png?v=20261110" alt="元僑科技 DataSys" width="130" height="43">'
        for name in PAGES:
            html = (ROOT / 'site' / name).read_text(encoding='utf-8')
            with self.subTest(page=name):
                self.assertEqual(html.count(expected), 1)
                self.assertNotIn('v=20261110 alt=', html)


if __name__ == '__main__':
    unittest.main()
