import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def homepage_graph():
    html = (ROOT / 'site' / 'index.html').read_text(encoding='utf-8')
    match = re.search(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S)
    if match is None:
        raise AssertionError('homepage JSON-LD block not found')
    return json.loads(match.group(1))['@graph']


class HomepageStructuredDataTest(unittest.TestCase):
    def test_homepage_has_complete_local_business_data_without_breadcrumbs(self):
        graph = homepage_graph()
        self.assertNotIn('BreadcrumbList', [item.get('@type') for item in graph])
        local = next(item for item in graph if item.get('@type') == 'LocalBusiness')
        self.assertEqual(local['openingHoursSpecification'], [{
            '@type': 'OpeningHoursSpecification',
            'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            'opens': '09:00',
            'closes': '18:00',
        }])
        self.assertEqual(local['priceRange'], '$$')
        self.assertEqual(local['image'], 'https://www.datasys.com.tw/image/og-image.jpg')
        self.assertEqual(local['parentOrganization'], {'@id': 'https://www.datasys.com.tw/#organization'})
        self.assertNotIn('geo', local)


if __name__ == '__main__':
    unittest.main()
