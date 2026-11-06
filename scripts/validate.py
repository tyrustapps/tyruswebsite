"""Dependency-free build gate: links, metadata, baseline accessibility, security, size."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'dist'
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes = []
    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))
p = Page()
p.feed((SITE / 'index.html').read_text())
nodes = p.nodes
checks = 0
def check(value, message):
    global checks
    assert value, message
    checks += 1
ids = [a['id'] for _, a in nodes if 'id' in a]
check(len(ids) == len(set(ids)), 'Duplicate HTML IDs')
check(next(a for t,a in nodes if t == 'html').get('lang') == 'en', 'Missing document language')
for tag in ['main', 'h1', 'title']:
    check(sum(t == tag for t,_ in nodes) == 1, f'Expected one {tag}')
check(any(t == 'nav' and a.get('aria-label') for t,a in nodes), 'Navigation needs a label')
check(any(a.get('href') == '#main' for _,a in nodes), 'Missing skip link')
last = 0
for tag, attrs in nodes:
    if re.fullmatch('h[1-6]', tag):
        level = int(tag[1])
        check(level <= last + 1, 'Skipped heading level')
        last = level
    if tag == 'img':
        check('alt' in attrs, 'Image without alt')
    for label in ['aria-controls', 'aria-labelledby']:
        for target in attrs.get(label, '').split():
            check(target in ids, f'Broken {label}: {target}')
    href = attrs.get('href', '')
    if href.startswith('#') and href != '#':
        check(href[1:] in ids, f'Broken anchor: {href}')
    if href.startswith('mailto:'):
        check(href == 'mailto:jay@tyrus.com', 'Wrong email target')
    for attr in ['src','href']:
        value = attrs.get(attr,'')
        if value and not value.startswith(('#','https:','mailto:')):
            check((SITE / value).is_file(), f'Missing local asset: {value}')
check(sum(a.get('href') == 'mailto:jay@tyrus.com' for _,a in nodes) == 5, 'Expected all five contact links')
for name in ['description','viewport']:
    check(any(t == 'meta' and a.get('name') == name and a.get('content') for t,a in nodes), f'Missing {name}')
for name in ['og:type','og:title','og:description','og:url']:
    check(any(a.get('property') == name and a.get('content') for _,a in nodes), f'Missing {name}')
check(any(a.get('rel') == 'canonical' and a.get('href') == 'https://www.tyrus.com/' for _,a in nodes), 'Wrong canonical')
check(len([1 for t,a in nodes if t == 'article' and a.get('class') == 'service']) == 6, 'Expected six services')
css = (SITE / 'styles.css').read_text()
check('prefers-reduced-motion:reduce' in css, 'Missing reduced motion')
check(':focus-visible' in css, 'Missing focus styling')
# WCAG normal-text contrast for all semantic foreground/background pairings.
def luminance(color):
    values = [int(color[i:i+2],16)/255 for i in (0,2,4)]
    values = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in values]
    return sum(x*y for x,y in zip(values,[.2126,.7152,.0722]))
for fg,bg in [('132c3a','f7f8f5'),('596c74','f7f8f5'),('596c74','eef2ee'),('087571','f7f8f5'),('087571','eef2ee'),('81d0c2','132c3a'),('c2d0d3','132c3a'),('132c3a','d4eee4')]:
    a,b = sorted([luminance(fg),luminance(bg)])
    check((b+.05)/(a+.05) >= 4.5, f'Insufficient contrast: #{fg} on #{bg}')
config = json.loads((SITE / 'staticwebapp.config.json').read_text())
for key in ['Content-Security-Policy','X-Content-Type-Options','Referrer-Policy','Permissions-Policy','Strict-Transport-Security']:
    check(key in config['globalHeaders'], f'Missing security header: {key}')
ET.parse(SITE / 'sitemap.xml')
check('https://www.tyrus.com/' in (SITE / 'sitemap.xml').read_text(), 'Sitemap domain')
size = sum(f.stat().st_size for f in SITE.iterdir() if f.is_file())
check(size < 100000, 'Static page exceeds 100 KB budget')
check(not any(t == 'script' and a.get('src','').startswith('http') for t,a in nodes), 'Third-party script')
print(f'PASS: {checks} build, link, metadata, baseline accessibility, contrast and security checks; static payload {size:,} bytes.')
print('These baseline checks are not a full WCAG conformance audit. Browser interaction and visual review are separate.')
