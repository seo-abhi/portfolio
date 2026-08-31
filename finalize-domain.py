#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys,json,datetime
ROOT=Path(__file__).resolve().parent
if len(sys.argv)!=2: raise SystemExit('Usage: python finalize-domain.py https://yourdomain.com')
BASE=sys.argv[1].strip().rstrip('/')+'/'
if not BASE.startswith(('https://','http://')): raise SystemExit('Use a full URL, e.g. https://example.com')
CASE_NAMES={'earthly-jewels.html':'Earthly Jewels','streamit.html':'Streamit','tinyfacets.html':'Tinyfacets','jewelite.html':'Jewelite','iqonic-tech.html':'IQONIC Tech','kivicare.html':'KiviCare','iqonic-agency.html':'IQONIC Agency','bitrix-theme.html':'Bitrix Theme','allclonescript.html':'AllCloneScript','coinremitter.html':'CoinRemitter'}
def url_for(p):
 rel=p.relative_to(ROOT).as_posix(); return BASE if rel=='index.html' else urljoin(BASE,rel)
urls=[]
for p in sorted(ROOT.rglob('*.html')):
 if p.name=='404.html': continue
 s=BeautifulSoup(p.read_text(encoding='utf-8'),'html.parser'); url=url_for(p); rel=p.relative_to(ROOT).as_posix()
 can=s.find('link',rel='canonical') or s.new_tag('link',rel='canonical'); can['href']=url
 if not can.parent: s.head.append(can)
 og=s.find('meta',property='og:url') or s.new_tag('meta'); og['property']='og:url'; og['content']=url
 if not og.parent: s.head.append(og)
 ogi=s.find('meta',property='og:image') or s.new_tag('meta'); ogi['property']='og:image'; ogi['content']=urljoin(BASE,'assets/images/social/abhi-patel-seo-portfolio.png')
 if not ogi.parent: s.head.append(ogi)
 tw=s.find('meta',attrs={'name':'twitter:image'}) or s.new_tag('meta'); tw['name']='twitter:image'; tw['content']=urljoin(BASE,'assets/images/social/abhi-patel-seo-portfolio.png')
 if not tw.parent: s.head.append(tw)
 # Existing JSON-LD URL enrichment.
 for sc in s.find_all('script',attrs={'type':'application/ld+json'}):
  try:data=json.loads(sc.string or sc.get_text())
  except:continue
  if isinstance(data,dict):
   if '@graph' in data:
    for node in data['@graph']:
     if isinstance(node,dict):
      if node.get('@type')=='WebSite': node.setdefault('url',BASE);node.setdefault('@id',BASE+'#website')
      if node.get('@type')=='Person': node.setdefault('url',BASE);node.setdefault('@id',BASE+'#person')
   else:
    data.setdefault('url',url)
    if data.get('@type')=='Article': data.setdefault('mainEntityOfPage',{'@type':'WebPage','@id':url})
   sc.string=json.dumps(data,ensure_ascii=False,indent=2)
 # Breadcrumb schema.
 breadcrumb=None
 if rel=='seo-case-studies.html':
  breadcrumb={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE},{'@type':'ListItem','position':2,'name':'SEO Case Studies','item':url}]}
 elif rel.startswith('case-studies/'):
  name=CASE_NAMES.get(p.name,p.stem.replace('-',' ').title());breadcrumb={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':BASE},{'@type':'ListItem','position':2,'name':'SEO Case Studies','item':urljoin(BASE,'seo-case-studies.html')},{'@type':'ListItem','position':3,'name':name,'item':url}]}
 if breadcrumb:
  sc=s.find('script',attrs={'data-seo-breadcrumb':'true'}) or s.new_tag('script',type='application/ld+json');sc['data-seo-breadcrumb']='true';sc.string=json.dumps(breadcrumb,ensure_ascii=False,indent=2)
  if not sc.parent:s.head.append(sc)
 p.write_text(str(s),encoding='utf-8');urls.append((url,p.stat().st_mtime))
# sitemap
lines=['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for url,mtime in urls:
 d=datetime.datetime.fromtimestamp(mtime).date().isoformat();lines+=['  <url>',f'    <loc>{url}</loc>',f'    <lastmod>{d}</lastmod>','  </url>']
lines.append('</urlset>');(ROOT/'sitemap.xml').write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+urljoin(BASE,'sitemap.xml')+'\n',encoding='utf-8')
print('Production SEO URLs finalized for',BASE);print('Pages:',len(urls))
