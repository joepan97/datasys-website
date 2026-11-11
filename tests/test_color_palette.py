import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ColorPaletteTest(unittest.TestCase):
    def test_stylesheet_uses_only_the_primary_palette_for_targeted_colors(self):
        css = (ROOT / 'site' / 'style.css').read_text(encoding='utf-8')
        self.assertNotIn('--color-', css)
        self.assertIsNone(re.search(r'(?i)#(?:2563eb|22d3ee|0b1f3a|111827|f8fafc|e2e8f0|64748b)\b', css))
        for name in ('--navy:', '--navy-d:', '--navy-xd:', '--accent:', '--accent-d:', '--ink:', '--muted:', '--line:', '--bg:', '--bg-soft:'):
            self.assertIn(name, css)


if __name__ == '__main__':
    unittest.main()
