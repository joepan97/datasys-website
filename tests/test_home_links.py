import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ('index.html', 'netapp.html', 'lto.html', 'parts.html', 'rental.html', 'security.html', 'ai.html', 'cases.html', 'about.html')


class HomepageLinksTest(unittest.TestCase):
    def test_sitewide_logo_and_home_nav_point_to_root(self):
        for name in PAGES + ('contact.html',):
            html = (ROOT / 'site' / name).read_text(encoding='utf-8')
            with self.subTest(page=name):
                self.assertGreaterEqual(html.count('href="/"'), 2)
                self.assertNotIn('href="index.html"', html)

    def test_hero_images_are_preloaded_before_stylesheet_with_matching_version(self):
        css = (ROOT / 'site' / 'style.css').read_text(encoding='utf-8')
        for page, image in [('index.html', 'hero-home'), ('ai.html', 'hero-ai')]:
            with self.subTest(page=page):
                html = (ROOT / 'site' / page).read_text(encoding='utf-8')
                preload = f'<link rel="preload" as="image" href="image/{image}.webp?v=20261110" fetchpriority="high">'
                self.assertIn(preload, html)
                self.assertLess(html.index(preload), html.index('<link rel="stylesheet"'))
                self.assertIn(f'url(image/{image}.webp?v=20261110)', css)

    def test_build_header_uses_root_homepage_link_and_preserves_active_state(self):
        source = (ROOT / 'build.py').read_text(encoding='utf-8')
        self.assertIn('"/" if h == "index.html" else h', source)
        self.assertIn('h == active', source)
        self.assertIn('<a class="logo" href="/">', source)


if __name__ == '__main__':
    unittest.main()
