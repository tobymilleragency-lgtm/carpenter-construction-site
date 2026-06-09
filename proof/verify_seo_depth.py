#!/usr/bin/env python3
from pathlib import Path
from html.parser import HTMLParser
import html, re, sys
root = Path(__file__).resolve().parents[1]
services = [
'remodels','home-builds-additions','kitchen-remodeling','bathroom-remodeling','basements-bonus-rooms','windows-doors-trim','flooring','framing-drywall','decks','fences','exterior-repairs','gc-trade-coordination']
areas = ['joplin-mo','webb-city-mo','carl-junction-mo','neosho-mo','carthage-mo','galena-ks']
errors=[]
rows=[]
def words_for(p):
    s=p.read_text(errors='ignore')
    for banned in ['approval','candidate','public Facebook','do not claim','self-perform','draft/spec','draft website','/home/toby','Source ledger','fbcdn.net','licensed and insured','years in business','emergency service','24/7 emergency']:
        if banned.lower() in s.lower(): errors.append(f'{p.relative_to(root)} forbidden phrase: {banned}')
    h1=len(re.findall(r'<h1\b', s, re.I))
    if h1 != 1: errors.append(f'{p.relative_to(root)} expected one h1 got {h1}')
    txt=re.sub(r'<script.*?</script>|<style.*?</style>', ' ', s, flags=re.S|re.I)
    txt=re.sub(r'<[^>]+>', ' ', txt)
    txt=html.unescape(txt)
    return len(re.findall(r"\b[\w’'-]+\b", txt))
for slug in services:
    p=root/'services'/slug/'index.html'
    wc=words_for(p); rows.append((f'/services/{slug}/', wc))
    if not (1000 <= wc <= 1200): errors.append(f'/services/{slug}/ word count {wc}')
for slug in areas:
    p=root/'service-area'/slug/'index.html'
    wc=words_for(p); rows.append((f'/service-area/{slug}/', wc))
    if not (1000 <= wc <= 1200): errors.append(f'/service-area/{slug}/ word count {wc}')
for route,wc in rows: print(f'{route}: {wc} words')
if errors:
    print('\nFAIL')
    print('\n'.join(errors))
    sys.exit(1)
print('PASS SEO depth: 12 service pages + 6 service-area pages are 1000-1200 visible words and forbidden phrases are clean')
