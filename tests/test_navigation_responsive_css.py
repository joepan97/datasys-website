import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NavigationResponsiveCssTest(unittest.TestCase):
    def test_desktop_nav_stays_single_line_and_switches_to_menu_below_1120px(self):
        css = (ROOT / 'site' / 'style.css').read_text(encoding='utf-8')
        self.assertIn('@media(max-width:1120px){', css)
        self.assertNotIn('@media(max-width:1000px){', css)
        self.assertIn('nav{margin-left:auto;display:flex;flex-wrap:nowrap;gap:2px}', css)
        button_rule = css.split('.btn{', 1)[1].split('}', 1)[0]
        self.assertIn('white-space:nowrap', button_rule)


if __name__ == '__main__':
    unittest.main()
