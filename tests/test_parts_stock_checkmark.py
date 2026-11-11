import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PartsStockCheckmarkTest(unittest.TestCase):
    def test_stock_card_items_reserve_space_for_checkmark(self):
        css = (ROOT / 'site' / 'style.css').read_text(encoding='utf-8')
        rule = css.split('.stock-card li{', 1)[1].split('}', 1)[0]
        self.assertIn('padding:4px 0 4px 26px', rule)
        self.assertIn('position:relative', rule)


if __name__ == '__main__':
    unittest.main()
