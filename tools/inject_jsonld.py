#!/usr/bin/env python3
"""Static JSON-LD injector for the datasys-website site/.

Generates one schema.org @graph <script type="application/ld+json"> per page,
embedded in <head> so it is visible to non-JS crawlers (AI bots).
Re-runnable: strips previously injected blocks (marked with data-gen), then
regenerates from the page's actual <h1> and <details class="faq"> content.

Usage: python3 tools/inject_jsonld.py   (run from repo root)
"""
import json, os, re, html as htmlmod

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, 'site')
BASE = 'https://www.datasys.com.tw/'

ORG = {
    '@type': 'Organization', '@id': BASE + '#organization',
    'name': '元僑科技有限公司',
    'alternateName': ['元僑科技', 'DataSys Technologies Co, LTD'],
    'url': BASE,
    'logo': BASE + 'image/datasys-logo.png',
    'foundingDate': '2007',
    'identifier': {'@type': 'PropertyValue', 'name': '統一編號', 'value': '28703966'},
    'email': 'sales@datasys.com.tw', 'telephone': '+886-2-2697-3311',
    'address': {'@type': 'PostalAddress', 'addressCountry': 'TW', 'addressRegion': '新北市',
                'addressLocality': '汐止區', 'streetAddress': '新台五路一段99號31樓之3'},
    'sameAs': ['https://www.netapp.com/partners/partner-connect/datasys-technology-co-ltd'],
}
LOCAL = {
    '@type': 'LocalBusiness', '@id': BASE + '#localbusiness',
    'name': '元僑科技有限公司', 'url': BASE,
    'telephone': '+886-2-2697-3311', 'email': 'sales@datasys.com.tw',
    'address': ORG['address'],
}
WEBSITE = {'@type': 'WebSite', '@id': BASE + '#website', 'url': BASE,
           'name': '元僑科技', 'inLanguage': 'zh-Hant',
           'publisher': {'@id': BASE + '#organization'}}
SERVICE = {
    'netapp.html': 'NetApp 儲存設備規劃與維護',
    'lto.html': 'IBM LTO 磁帶供應',
    'parts.html': '二手零件與設備詢料',
    'rental.html': 'Storage 短期租賃',
    'security.html': '資訊安全環境評估',
    'ai.html': 'AI 流程評估與導入',
}
# page file -> (canonical url path, breadcrumb name fallback)
PAGES = {
    'index.html': ('', '元僑科技首頁'),
    'netapp.html': ('netapp.html', None), 'lto.html': ('lto.html', None),
    'parts.html': ('parts.html', None), 'rental.html': ('rental.html', None),
    'security.html': ('security.html', None), 'ai.html': ('ai.html', None),
    'cases.html': ('cases.html', None), 'about.html': ('about.html', None),
    'contact.html': ('contact.html', None),
    'privacy-policy/index.html': ('privacy-policy', None),
    'data-deletion/index.html': ('data-deletion', None),
}

def clean_text(fragment):
    text = re.sub(r'<[^>]+>', '', fragment)
    return htmlmod.unescape(re.sub(r'\s+', ' ', text)).strip()

def build_graph(fname, page_html):
    path, fallback = PAGES[fname]
    item = BASE + path if path else BASE
    m = re.search(r'<h1[^>]*>(.*?)</h1>', page_html, flags=re.S)
    name = clean_text(m.group(1)) if m else fallback
    graph = [dict(ORG), dict(LOCAL), dict(WEBSITE)]
    key = os.path.basename(fname)
    if key in SERVICE and path:
        graph.append({'@type': 'Service', 'name': SERVICE[key],
                      'provider': {'@id': BASE + '#organization'},
                      'areaServed': {'@type': 'Country', 'name': 'Taiwan'}, 'url': item})
    crumbs = [{'@type': 'ListItem', 'position': 1, 'name': '首頁', 'item': BASE}]
    crumbs.append({'@type': 'ListItem', 'position': 2, 'name': name, 'item': item})
    graph.append({'@type': 'BreadcrumbList', 'itemListElement': crumbs})
    faqs = re.findall(r'<details class="faq"><summary>(.*?)</summary>(.*?)</details>', page_html, flags=re.S)
    if faqs:
        graph.append({'@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': clean_text(q),
             'acceptedAnswer': {'@type': 'Answer', 'text': clean_text(a)}} for q, a in faqs]})
    return {'@context': 'https://schema.org', '@graph': graph}

def main():
    marker = re.compile(r'\n?<script type="application/ld\+json" data-gen="inject_jsonld">.*?</script>', flags=re.S)
    for fname in PAGES:
        p = os.path.join(SITE, fname)
        t = open(p, encoding='utf-8').read()
        t = marker.sub('', t)  # strip previously injected block
        graph = build_graph(fname, t)
        block = ('<script type="application/ld+json" data-gen="inject_jsonld">\n'
                 + json.dumps(graph, ensure_ascii=False, separators=(',', ':'))
                 + '\n</script>')
        assert '</head>' in t, fname
        t = t.replace('</head>', block + '\n</head>', 1)
        open(p, 'w', encoding='utf-8').write(t)
        types = [g['@type'] for g in graph['@graph']]
        print(f'{fname}: {types}')

if __name__ == '__main__':
    main()
