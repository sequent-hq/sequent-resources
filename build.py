"""Rebuild the three static pages from one shared content source. Python 3 only."""
from pathlib import Path
from html import escape as esc
from collections import Counter
import json, re

ROOT=Path(__file__).resolve().parent
DATA=json.loads((ROOT/'source/content.json').read_text(encoding='utf-8'))
BLOCKED=['ade1559657f00829','cdc29c298c968996','b33fb907e847b2ed','7f746c7dded54655']
COUNTS=Counter(x['brand'] for x in DATA['backgrounds'])
ICONS={
 'music':'<path d="M14 3v12a4 4 0 1 1-4-4h1M14 3c1 4 3 5 7 5v4c-3 0-5-1-7-3"/>',
 'share':'<path d="M12 16V3m-5 5 5-5 5 5M5 13v7h14v-7"/>',
 'grid':'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 'film':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m10 9 5 3-5 3z"/>',
 'image':'<rect x="3" y="3" width="18" height="18" rx="3"/><circle cx="8" cy="8" r="1.5"/><path d="m3 17 6-6 4 4 3-3 5 5"/>',
 'social':'<rect x="3" y="3" width="18" height="18" rx="6"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
 'monitor':'<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8m-4-4v4"/>',
 'help':'<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 0 1 5 0c0 2-2.5 2-2.5 4m0 3h.01"/>',
 'arrow':'<path d="M7 17 17 7M7 7h10v10"/>',
 'right':'<path d="M4 12h16m-6-6 6 6-6 6"/>',
 'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
 'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5"/>',
 'close':'<path d="m6 6 12 12M6 18 18 6"/>',
 'download':'<path d="M12 3v12m-5-5 5 5 5-5M4 15v5h16v-5"/>',
 'copy':'<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M15 8V4H4v11h4"/>',
 'play':'<path d="m8 5 11 7-11 7z"/>',
 'folder':'<path d="M3 7V5a2 2 0 0 1 2-2h5l2 3h7a2 2 0 0 1 2 2v11H3z"/>',
 'menu':'<path d="M4 6h16M4 12h16M4 18h16"/>',
 'check':'<path d="m5 12 4 4L19 6"/>',
 'link':'<path d="m10 13 4-4m-6 6-2 2a4 4 0 0 1-6-6l3-3a4 4 0 0 1 6 0m6 0 2-2a4 4 0 0 1 6 6l-3 3a4 4 0 0 1-6 0" transform="translate(2 0) scale(.9)"/>'
}
def icon(name): return f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
def logo(slug, cls=''):
    return f'<span class="brand-logo {cls}"><img class="lg-d" src="assets/logos/{slug}-d.png" alt="" width="460" height="124"><img class="lg-l" src="assets/logos/{slug}-l.png" alt="" width="460" height="124"></span>'
def external(url,label,cls='button'):
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener">{label}{icon("arrow")}</a>'

def social_profiles(compact=False):
    links=''
    for p in DATA.get('socialProfiles',[]):
        text=f'<span>{esc(p["name"])}</span>' if compact else f'<span><b>Kreate {esc(p["name"])}</b><small>{esc(p["handle"])}</small></span>'
        links+=f'<a href="{esc(p["url"])}" target="_blank" rel="noopener" aria-label="Open Kreate {esc(p["name"])}">{icon(p["icon"])}{text}{icon("arrow")}</a>'
    return f'<nav class="social-profile-links{" compact" if compact else ""}" aria-label="Kreate social profiles">{links}</nav>'
def nav(page):
    if page=='brands':
        return f'''<aside class="sidebar" id="sidebar"><a class="brand-home" href="brands.html" aria-label="Sequent brand standards and logos">{logo('sequent')}</a><div class="workspace-label">BRAND STANDARDS &amp; LOGOS</div><nav aria-label="Brand resources"><a class="nav-link active" href="#brands" data-section="brands">{icon('grid')}<span>Brand library</span><span class="nav-count">{len(DATA['brands'])}</span></a><a class="nav-link" href="index.html">{icon('arrow')}<span>Full board</span></a></nav><div class="sidebar-bottom"><div class="sidebar-note"><span class="small-label">THE SEQUENT FAMILY</span><p>One place for every brand.</p></div></div></aside>'''
    prefix='' if page=='index' else 'index.html'
    entries=[('brands','Brand library','grid',16),('videos','Videos','film',len(DATA['videos'])),('photo','Photography','image',len(DATA['photos'])),('backgrounds','Call backgrounds','monitor',len(DATA['backgrounds'])),('social','Social content','social',len(DATA['social']))]
    items=''
    for section,title,ico,n in entries:
        href='backgrounds.html' if section=='backgrounds' else f'{prefix}#{section}'
        if page=='brands' and section=='brands': href='#brands'
        active=(section=='backgrounds' if page=='backgrounds' else section=='brands')
        items+=f'<a class="nav-link {"active" if active else ""}" href="{href}" data-section="{section}">{icon(ico)}<span>{title}</span><span class="nav-count">{n}</span></a>'
    return f'''<aside class="sidebar" id="sidebar"><a class="brand-home" href="index.html" aria-label="Sequent resource library">{logo('sequent')}</a><div class="workspace-label">RESOURCE LIBRARY</div><nav aria-label="Resource sections">{items}</nav><div class="sidebar-bottom"><a class="nav-link" href="{prefix}#help">{icon('help')}<span>Help & downloads</span></a><div class="sidebar-note"><span class="small-label">THE SEQUENT FAMILY</span><p>One place for every brand.</p></div>{social_profiles(compact=True)}<a class="team-link" href="https://brand.kreate.com/media/" target="_blank" rel="noopener">Team portal {icon('arrow')}<small>Team sign-in required</small></a></div></aside>'''
def section_heading(number,title,desc,extra=''):
    return f'<div class="section-heading"><div><div class="eyebrow">{number} / THE LIBRARY</div><h2>{title}</h2><p>{desc}</p></div>{extra}</div>'
def file_size(size):
    return f'{size/1048576:.1f} MB' if size>=1048576 else f'{max(1,round(size/1024))} KB'

def logo_downloads(brand):
    assets=brand.get('logos',[])
    if not assets: return ''
    formats=sorted(set(a['format'] for a in assets), key=lambda f:({'PNG':0,'SVG':1,'PDF':2,'JPG':3,'AI':4,'EPS':5}.get(f,9),f))
    filters='<button class="logo-filter active" type="button" data-logo-format="all" aria-pressed="true">All files</button>'
    filters+=''.join(f'<button class="logo-filter" type="button" data-logo-format="{esc(f)}" aria-pressed="false">{esc(f)}</button>' for f in formats)
    cards=''
    for a in assets:
        name=f"{brand['name']} — {a['label']}"
        file=esc(a['file'])
        picture=a.get('preview') or (a['file'] if a['format'] in ['PNG','SVG','JPG','JPEG','WEBP','GIF'] else '')
        art=f'<img src="{esc(picture)}" alt="{esc(name)}" loading="lazy">' if picture else f'<span class="logo-format-art">{icon("folder")}<b>{esc(a["format"])}</b></span>'
        dimensions=f' · {a["width"]} × {a["height"]}' if a.get('width') and a.get('height') and a['format']!='SVG' else ''
        source=external(a['source'],'Source','logo-source') if a.get('source','').startswith('http') else ''
        download_name=esc(a.get('download_name',Path(a['file']).name))
        cards+=f'''<article class="logo-file" data-format="{esc(a['format'])}"><a class="logo-preview {esc(a.get('tone','light'))}" href="{file}" download="{download_name}" aria-label="Download {esc(name)} ({esc(a['format'])})">{art}<span class="logo-format-badge">{esc(a['format'])}</span></a><div class="logo-file-body"><h3 class="logo-name">{esc(a['label'])}</h3><p class="logo-meta">{esc(a['format'])}{dimensions} · {file_size(a.get('bytes',0))}</p><div class="logo-file-actions"><a class="button logo-save" href="{file}" download="{download_name}" aria-label="Download {esc(name)} {esc(a['format'])}">{icon('download')}Download</a><button class="icon-button jsonly share-asset" type="button" data-file="{file}" data-title="{esc(name)}" data-filename="{download_name}" data-bytes="{a.get('bytes',0)}" aria-label="Share {esc(name)} {esc(a['format'])}" title="Share file or link">{icon('share')}</button><button class="icon-button jsonly copy-asset" type="button" data-file="{file}" aria-label="Copy direct link to {esc(name)} {esc(a['format'])}" title="Copy direct file link">{icon('copy')}</button></div>{source}</div></article>'''
    pack=f'<a class="button logo-pack" href="{esc(brand["logo_pack"])}" download>{icon("download")}Download all <span>ZIP</span></a>' if brand.get('logo_pack') else ''
    default='PNG' if 'PNG' in formats else 'JPG' if 'JPG' in formats else 'SVG' if 'SVG' in formats else 'all'
    return f'''<div class="logo-downloads" data-default-format="{default}"><div class="logo-downloads-heading"><div><h3>Ready-to-use logos</h3><p><span class="logo-visible-count">{len(assets)} files</span> · Save a logo or share it directly.</p><a class="resource-jump" href="#resources-{brand['slug']}">Guidelines &amp; resources ↓</a></div>{pack}</div><div class="logo-filters jsonly" aria-label="Logo file formats">{filters}</div><div class="logo-grid">{cards}</div></div>'''

def brand_library(focused=False):
    tiles=''
    for b in DATA['brands']:
        quick=f'<div class="brand-quick-actions"><a class="quick-download" href="{esc(b["logo_pack"])}" download aria-label="Download all {esc(b["name"])} logos">{icon("download")}<span>Download logos</span></a><button class="icon-button jsonly share-kit" data-brand="{b["slug"]}" data-title="{esc(b["name"])} brand kit" aria-label="Share {esc(b["name"])} brand kit" title="Share brand kit">{icon("share")}</button></div>' if b.get('logo_pack') else ''
        tiles+=f'''<article class="brand-card" data-brand="{b['slug']}" data-category="{b['category']}" data-name="{esc(b['name'])}"><a class="brand-open" href="#bp-{b['slug']}" data-brand="{b['slug']}" aria-label="Open {esc(b['name'])} brand kit"><div class="brand-card-top"><span>{'RETAIL PARTNER' if b['category']=='retail' else 'SEQUENT FAMILY'}</span>{icon('arrow')}</div>{logo(b['slug'])}<div class="brand-card-bottom"><span class="brand-card-title">{esc(b['name'])}</span><span class="brand-card-tags">{' · '.join(b['tags'])}</span></div></a>{quick}</article>'''
    panels=''
    for b in DATA['brands']:
        content=b.get('resource_content',b['content'])
        if b['slug'] in COUNTS:
            content=re.sub(r'GALLERY\s*[·•]\s*\d+',f"GALLERY · {COUNTS[b['slug']]}",content)
        for key in BLOCKED:
            content=re.sub(r'<a\b([^>]*href="[^"]*'+key+r'[^"]*"[^>]*)>(.*?)</a>',r'<span class="rl unavailable" aria-disabled="true">\2<span class="availability">Unavailable</span></span>',content,flags=re.S)
        panels+=f'''<section class="brand-panel" id="bp-{b['slug']}" data-name="{esc(b['name'])}"><div class="panel-art">{logo(b['slug'])}</div><div class="panel-heading"><div><div class="eyebrow">{'RETAIL PARTNER' if b['category']=='retail' else 'SEQUENT FAMILY'}</div><h2>{esc(b['name'])}</h2><p>{esc(b['description'])}</p></div>{external(b['collection'],'Source collection','button small') if b['collection'] else ''}</div>{logo_downloads(b)}{content}</section>'''
    view_link='' if focused else '<a class="text-link" href="brands.html">Brand-only view '+icon('arrow')+'</a>'
    return f'''<section id="brands" class="library-section">{section_heading('01','Find your brand.','Download a logo kit in one click. Open a brand for individual files and guidelines.', view_link)}<div class="library-toolbar"><div class="filters jsonly" aria-label="Filter brands"><button type="button" class="filter active" data-filter="all" aria-pressed="true">All brands <span>16</span></button><button type="button" class="filter" data-filter="family" aria-pressed="false">Sequent family <span>13</span></button><button type="button" class="filter" data-filter="retail" aria-pressed="false">Retail partners <span>3</span></button></div><span class="results-count" id="brandCount" aria-live="polite">16 collections</span></div><div class="brand-grid">{tiles}</div><div id="panelStore">{panels}</div><div class="library-footnote">{icon('download')} Logo downloads stay here. Original source collections are available inside each kit.</div></section>'''


def collection_cards(items,ico):
    cards=''
    for c in items:
        unavailable=any(key in c['url'] for key in BLOCKED)
        team='/media/' in c['url']
        label='Collection unavailable' if unavailable else 'Team sign-in' if team else 'Open collection'
        inside=f'<span class="collection-icon">{icon(ico)}</span><h3>{esc(c["title"])}</h3><p>{esc(c["description"])}</p><span class="collection-bottom">{label}{icon("arrow") if not unavailable else ""}</span>'
        cards+=f'<div class="collection-card unavailable" aria-disabled="true">{inside}</div>' if unavailable else f'<a class="collection-card" href="{esc(c["url"])}" target="_blank" rel="noopener">{inside}</a>'
    return '<div class="collection-grid">'+cards+'</div>'
def video_card(v, brand):
    featured=v.get('featured',False)
    film_id='film-'+v['slug']
    share_url='https://sequent-hq.github.io/sequent-resources/#'+film_id
    playback=f'data-video="{esc(v["src"])}" data-download="{esc(v["download"])}" data-title="{esc(v["title"])}" data-poster="{esc(v["image"])}" data-video-id="{film_id}" data-video-brand="{esc(v["brand"])}"'
    watch=f'<a class="button featured-watch" href="{esc(v["src"])}" {playback}>{icon("play")}Watch film</a>' if featured else ''
    return f'''<article id="{film_id}" class="video-card{' featured-video' if featured else ''}" data-brand-label="{esc(brand)}"><a class="video-cover" href="{esc(v['src'])}" {playback} aria-label="Play {esc(v['title'])}"><span class="image-fallback">{icon('film')}<span>{esc(v['title'])}</span></span><img src="{esc(v['image'])}" alt="{esc(v['title'])}" loading="lazy"><span class="play-circle">{icon('play')}</span><span class="resolution">{esc(v['resolution'])}</span></a><div class="video-body"><span class="video-brand-label">{esc(brand)}{' · Featured film' if featured else ''}</span><h4>{esc(v['title'])}</h4><p>{esc(v['description'])}</p>{watch}<div class="video-actions">{external(v['download'],'Open collection','text-link')}<button class="icon-button jsonly copy-link" data-copy="{share_url}" aria-label="Copy link to {esc(v['title'])}">{icon('copy')}</button></div></div></article>'''

def videos():
    groups=DATA.get('videoGroups',[])
    sections=''
    jumps=''
    for group in groups:
        slug,name=group['slug'],group['name']
        films=[v for v in DATA['videos'] if v.get('brand')==slug]
        collections=[v for v in DATA['videoCollections'] if v.get('brand')==slug and not v.get('show_as_video')]
        if not films and not collections: continue
        jumps+=f'<a href="#videos-{slug}">{esc(name)}{icon("right")}</a>'
        featured=''.join(video_card(v,name) for v in films if v.get('featured'))
        regular=''.join(video_card(v,name) for v in films if not v.get('featured'))
        grid=f'<div class="video-grid">{regular}</div>' if regular else ''
        related=f'<div class="video-related"><h4>More from {esc(name)}</h4>{collection_cards(collections,"film")}</div>' if collections else ''
        count=f'{len(films)} film'+('s' if len(films)!=1 else '')
        sections+=f'<section class="video-brand-group" id="videos-{slug}" aria-labelledby="video-heading-{slug}"><div class="video-group-heading"><h3 id="video-heading-{slug}">{esc(name)}</h3><span>{count}</span></div>{featured}{grid}{related}</section>'
    other=[v for v in DATA['videoCollections'] if not v.get('brand')]
    extras=f'<h3 class="subsection-title">Product &amp; brand collections</h3>{collection_cards(other,"film")}' if other else ''
    return f'<section id="videos" class="library-section">{section_heading("02","Stories in motion.","Start with Sequent. Explore films and stories from across our brands.")}<nav class="video-jumps" aria-label="Jump to video brand">{jumps}</nav>{sections}{extras}</section>'
def photos():
    return f'<section id="photo" class="library-section">{section_heading("03","A closer look.","Facilities, people, events, and products. Find the right photography collection.")}{collection_cards(DATA["photos"],"image")}</section>'
def social_card(c):
    featured=c.get('featured',False)
    feature_label='<div class="eyebrow">Featured collaboration</div>' if featured else ''
    date=f'<span class="social-date">{esc(c["date_label"])}</span>' if c.get('date_label') else ''
    description=f'<p class="social-description">{esc(c["description"])}</p>' if c.get('description') else ''
    return f'''<a class="social-card{' social-featured' if featured else ''}" href="{esc(c['url'])}" target="_blank" rel="noopener"><div class="social-cover"><img src="{esc(c['image'])}" alt="{esc(c['title'])}" loading="lazy"><span class="social-product">{esc(c['product'])}</span><span class="social-play">{icon('play')}</span></div><div class="social-body">{feature_label}<span class="creator">{esc(c['creator'])}{icon('arrow')}</span><h3>{esc(c['title'])}</h3>{description}{date}<span class="social-watch">{icon('play')}Watch on Instagram{icon('arrow')}</span></div></a>'''

def social():
    featured=''.join(social_card(c) for c in DATA['social'] if c.get('featured'))
    recent=''.join(social_card(c) for c in DATA['social'] if not c.get('archived') and not c.get('featured'))
    old=[c for c in DATA['social'] if c.get('archived')]
    archive=f'<details class="social-archive"><summary>Earlier collaborations <span>{len(old)} videos</span>{icon("right")}</summary><div class="social-grid">{"".join(social_card(c) for c in old)}</div></details>' if old else ''
    sources=''.join(external(c['url'],esc(c['title']),'text-link') for c in DATA['socialSources'])
    return f'<section id="social" class="library-section">{section_heading("04","Out in the world.","Product stories from Kreate and our creator community.")}{social_profiles()}{featured}<h3 class="subsection-title">Recent social videos</h3><div class="social-grid">{recent}</div>{archive}<div class="social-sources"><span>Source collections</span>{sources}</div></section>'
def help_section():
    return f'''<section id="help" class="help-section"><div class="eyebrow">A LITTLE GUIDANCE</div><h2>Get the right file.</h2><div class="help-grid"><div>{icon('download')}<h3>Download the original</h3><p>Open a file or collection and choose Download for the original format. Films play here at their original resolution. Source collections retain the original masters.</p></div><div>{icon('link')}<h3>Share a brand kit</h3><p>Open a brand, then use Copy brand link. The brand-only page is a focused view for partners and collaborators.</p></div><div>{icon('help')}<h3>Need something else?</h3><p>If a collection is unavailable or you need a new asset, contact your Sequent marketing team. The team portal requires sign-in.</p><a class="text-link" href="https://drive.google.com/drive/folders/13UAU7GG64fvu6oaUX1Rw1Mo9eh7eweNr" target="_blank" rel="noopener">Central branding folder ↗</a></div></div></section>'''
def gallery():
    filters='<button class="filter active" data-bg="all" aria-pressed="true">All backgrounds <span>'+str(len(DATA['backgrounds']))+'</span></button>'
    for slug,n in COUNTS.items(): filters+=f'<button class="filter" data-bg="{slug}" aria-pressed="false">{slug.title()} <span>{n}</span></button>'
    sections=''
    for slug,n in COUNTS.items():
        cards=''
        for c in DATA['backgrounds']:
            if c['brand']!=slug: continue
            cards+=f'''<article class="background-card"><a href="{esc(c['image'])}" target="_blank" rel="noopener" aria-label="Preview {esc(c['title'])}"><img src="{esc(c['image'])}" alt="{esc(c['title'])}" width="1920" height="1080" loading="lazy"></a><div><h3>{esc(c['title'])}</h3><a class="icon-button" href="{esc(c['image'])}" download aria-label="Download {esc(c['title'])}">{icon('download')}</a></div></article>'''
        sections+=f'<section class="background-section" id="{slug}" data-gallery="{slug}"><div class="gallery-heading"><h2>{slug.title()}</h2><span>{n} backgrounds</span></div><div class="background-grid">{cards}</div></section>'
    return f'<div class="gallery-controls jsonly">{filters}</div><p class="gallery-tip">Choose a background to preview it, or download the original. Mirrored versions are included where available.</p>{sections}'
def page(kind):
    bg=kind=='backgrounds'
    brand_only=kind=='brands'
    title='Call backgrounds' if bg else 'Brand standards' if kind=='brands' else 'Resource library'
    headline='Look the part.' if bg else 'Every detail. On brand.' if kind=='brands' else 'Good work starts here.'
    desc='A better backdrop for your next conversation.' if bg else 'Everything you need to bring the Sequent family of brands to life.'
    metadata='Brand standards, logos, and brand kits for the Sequent family and retail partners.' if brand_only else 'Brand standards, logos, templates, videos, and photography for the Sequent family.'
    hero_link='' if brand_only else f'<a class="hero-link" href="{"brands.html" if bg else "backgrounds.html"}">{icon("grid" if bg else "monitor")}<span>{"Explore brand kits" if bg else "Call backgrounds"}<small>{"16 brand collections" if bg else str(len(DATA["backgrounds"]))+" ready-to-use backgrounds"}</small></span>{icon("right")}</a>'
    content=gallery() if bg else brand_library(focused=brand_only)+(videos()+photos()+social()+help_section() if kind=='index' else '')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Sequent — {title}</title><meta name="description" content="{metadata}"><meta name="theme-color" content="#0c1015"><meta property="og:title" content="Sequent — {title}"><meta property="og:image" content="https://sequent-hq.github.io/sequent-resources/assets/og-card.png"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css?v=20260920-fullres"><script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('sequent-theme')==='light')document.documentElement.classList.add('light')}}catch(e){{}}</script><script src="app.js?v=20260920-fullres" defer></script></head><body data-page="{kind}"><a class="skip-link" href="#main">Skip to content</a><div class="intro" aria-hidden="true">{logo('sequent')}<span>RESOURCE LIBRARY</span><i></i></div>{nav(kind)}<div class="page-shell"><header class="topbar"><button class="icon-button menu-button jsonly" aria-label="Open navigation" aria-expanded="false" aria-controls="sidebar">{icon('menu')}</button><div class="breadcrumb">Sequent <span>/</span> <strong>{title}</strong></div><div class="topbar-actions"><a class="text-link full-library" href="index.html">{'Full board' if brand_only else 'Full library'}</a><button class="icon-button jsonly" id="themeToggle" aria-label="Switch to light theme">{icon('sun')}</button></div></header><main id="main"><div class="hero"><div><div class="eyebrow">SHARED ASSETS. CONNECTED BRANDS.</div><h1>{headline}</h1><p>{desc}</p></div>{hero_link}</div><div class="search-area jsonly"><div class="search-field">{icon('search')}<input id="search" type="search" placeholder="{'Search backgrounds…' if bg else 'Search brands, guidelines, templates…'}" aria-label="{'Search backgrounds' if bg else 'Search brand standards and logos' if brand_only else 'Search all resources'}" aria-controls="searchResults" autocomplete="off"><kbd>Ctrl K</kbd></div><div id="searchResults" hidden><div class="search-results-header"><span id="searchCount" role="status"></span><button class="icon-button" id="closeSearch" aria-label="Clear search">{icon('close')}</button></div><div id="searchItems"></div></div></div>{content}<footer><a href="index.html" aria-label="Sequent home">{logo('sequent')}</a><span>Brand resources, all together.</span><span>© 2026 Sequent</span></footer></main></div><dialog id="brandDialog" aria-labelledby="dialogLabel"><div class="dialog-toolbar"><span id="dialogLabel">Brand resources</span><div><button class="icon-button" id="copyBrand" aria-label="Copy brand link">{icon('copy')}</button><button class="icon-button" id="closeBrand" aria-label="Close brand kit">{icon('close')}</button></div></div><div id="brandDialogContent"></div></dialog><dialog id="videoDialog" aria-labelledby="videoTitle"><div class="dialog-toolbar"><h2 id="videoTitle">Watch film</h2><button class="icon-button" id="closeVideo" aria-label="Close video">{icon('close')}</button></div><video controls playsinline preload="metadata"></video><p id="videoError" hidden>This film could not load. Try again or open its source collection.</p><div class="video-dialog-footer"><a class="button" id="videoDownload" download>{icon('download')}Download video</a><a class="text-link" id="videoCollection" target="_blank" rel="noopener">Open collection {icon('arrow')}</a><button class="button" id="copyVideo">{icon('copy')}Copy link</button></div></dialog><div class="toast" id="toast" role="status"></div></body></html>'''
for kind in ['index','brands','backgrounds']:
    (ROOT/f'{kind}.html').write_text(page(kind),encoding='utf-8')
(ROOT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0c1015"/><path d="M9 10h14v4H13v4h10v4H9v-4h10v-4H9z" fill="#62ddf5"/></svg>',encoding='utf-8')
print('Built index.html, brands.html, backgrounds.html from shared source.')
