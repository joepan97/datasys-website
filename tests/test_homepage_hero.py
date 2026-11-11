import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def source_homepage():
    tree = ast.parse((ROOT / 'build.py').read_text(encoding='utf-8'))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'INDEX' for target in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError('INDEX template not found')


class HomepageHeroTest(unittest.TestCase):
    def test_approved_headline_and_inquiry_links_match_template(self):
        for name, html in [('site', (ROOT / 'site/index.html').read_text(encoding='utf-8')), ('template', source_homepage())]:
            with self.subTest(name=name):
                match = re.search(r'<section class="hero hero-home">(.*?)</section>', html, re.S)
                self.assertIsNotNone(match)
                if match is None:
                    continue
                hero = match.group(1)
                self.assertRegex(hero, r'企業儲存與備份<br\s*/?><span>從建置到維護，都有人支援。</span>')
                self.assertIn('href="contact.html"', hero)
                self.assertIn('href="tel:0226973311"', hero)
                self.assertIn('data-track-cta', hero)
                self.assertIn('IBM LTO', hero)


if __name__ == '__main__':
    unittest.main()
