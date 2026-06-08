#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import sys, re
root=Path(__file__).parent
routes=[p for p in root.rglob('index.html') if 'node_modules' not in str(p)]
errors=[]
for p in routes:
    s=p.read_text(errors='ignore')
    rel='/' if p.parent==root else '/' + p.parent.relative_to(root).as_posix() + '/'
    if '<nav' not in s or '<footer' not in s: errors.append(f'{rel}: missing nav/footer')
    h1=len(re.findall(r'<h1\b', s, re.I))
    if h1!=1: errors.append(f'{rel}: expected one h1 got {h1}')
    if 'fbcdn.net' in s: errors.append(f'{rel}: hotlinks fbcdn')
    if any(x in s.lower() for x in ['licensed and insured','years in business','emergency service','24/7 emergency']): errors.append(f'{rel}: forbidden claim')
    if len(re.sub('<[^<]+?>',' ',s))<900: errors.append(f'{rel}: thin content')
for asset in ['assets/styles.css','assets/site.js','sitemap.xml','robots.txt']:
    if not (root/asset).exists(): errors.append(f'missing {asset}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'PASS static verification: {len(routes)} html routes')
