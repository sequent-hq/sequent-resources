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
    return f'''<aside class="sidebar" id="sidebar"><a class="brand-home" href="index.html" aria-label="Sequent resource library">{logo('sequent')}</a><div class="workspace-label">RESOURCE LIBRARY</div><nav aria-label="Resource sections">{items}</nav><div class="sidebar-bottom"><a class="nav-link" href="{prefix}#help">{icon('help')}<span>Help & downloads</span></a><div class="sidebar-note"><span class="small-label">THE SEQUENT FAMILY</span><p>One place for every brand.</p></div><a class="team-link" href="https://brand.kreate.com/media/" target="_blank" rel="noopener">Team portal {icon('arrow')}<small>Team sign-in required</small></a></div></aside>'''
def section_heading(number,title,desc,extra=''):
    return f'<div class="section-heading"><div><div class="eyebrow">{number} / THE LIBRARY</div><h2>{title}</h2><p>{desc}</p></div>{extra}</div>'
def brand_library(focused=False):
    tiles=''
    for b in DATA['brands']:
        tiles+=f'''<a class="brand-card" href="#bp-{b['slug']}" data-brand="{b['slug']}" data-category="{b['category']}" data-name="{esc(b['name'])}" aria-label="Open {esc(b['name'])} brand kit"><div class="brand-card-top"><span>{'RETAIL PARTNER' if b['category']=='retail' else 'SEQUENT FAMILY'}</span>{icon('arrow')}</div>{logo(b['slug'])}<div class="brand-card-bottom"><span class="brand-card-title">{esc(b['name'])}</span><span class="brand-card-tags">{' · '.join(b['tags'])}</span></div></a>'''
    panels=''
    for b in DATA['brands']:
        content=b['content']
        if b['slug'] in COUNTS:
            content=re.sub(r'GALLERY\s*[·•]\s*\d+',f"GALLERY · {COUNTS[b['slug']]}",content)
        for key in BLOCKED:
            content=re.sub(r'<a\b([^>]*href="[^"]*'+key+r'[^"]*"[^>]*)>(.*?)</a>',r'<span class="rl unavailable" aria-disabled="true">\2<span class="availability">Unavailable</span></span>',content,flags=re.S)
        panels+=f'''<section class="brand-panel" id="bp-{b['slug']}" data-name="{esc(b['name'])}"><div class="panel-art">{logo(b['slug'])}</div><div class="panel-heading"><div><div class="eyebrow">{'RETAIL PARTNER' if b['category']=='retail' else 'SEQUENT FAMILY'}</div><h2>{esc(b['name'])}</h2><p>{esc(b['description'])}</p></div>{external(b['collection'],'All files','button small') if b['collection'] else ''}</div>{content}</section>'''
    view_link='' if focused else '<a class="text-link" href="brands.html">Brand-only view '+icon('arrow')+'</a>'
    return f'''<section id="brands" class="library-section">{section_heading('01','Find your brand.','Logos, guidelines, templates, and the details that make us recognizable.', view_link)}<div class="library-toolbar"><div class="filters jsonly" aria-label="Filter brands"><button type="button" class="filter active" data-filter="all" aria-pressed="true">All brands <span>16</span></button><button type="button" class="filter" data-filter="family" aria-pressed="false">Sequent family <span>13</span></button><button type="button" class="filter" data-filter="retail" aria-pressed="false">Retail partners <span>3</span></button></div><span class="results-count" id="brandCount" aria-live="polite">16 collections</span></div><div class="brand-grid">{tiles}</div><div id="panelStore">{panels}</div><div class="library-footnote">{icon('folder')} Looking for presentation masters or fonts? Open a brand kit to explore its files.</div></section>'''
def collection_cards(items,ico):
    cards=''
    for c in items:
        unavailable=any(key in c['url'] for key in BLOCKED)
        team='/media/' in c['url']
        label='Collection unavailable' if unavailable else 'Team sign-in' if team else 'Open collection'
        inside=f'<span class="collection-icon">{icon(ico)}</span><h3>{esc(c["title"])}</h3><p>{esc(c["description"])}</p><span class="collection-bottom">{label}{icon("arrow") if not unavailable else ""}</span>'
        cards+=f'<div class="collection-card unavailable" aria-disabled="true">{inside}</div>' if unavailable else f'<a class="collection-card" href="{esc(c["url"])}" target="_blank" rel="noopener">{inside}</a>'
    return '<div class="collection-grid">'+cards+'</div>'
def videos():
    cards=''
    for v in DATA['videos']:
        cards+=f'''<article class="video-card"><a class="video-cover" href="{esc(v['src'])}" data-video="{esc(v['src'])}" data-download="{esc(v['download'])}" data-title="{esc(v['title'])}" aria-label="Play {esc(v['title'])}"><span class="image-fallback">{icon('film')}<span>Video preview</span></span><img src="{esc(v['image'])}" alt="{esc(v['title'])}" loading="lazy"><span class="play-circle">{icon('play')}</span><span class="resolution">{esc(v['resolution'])}</span></a><div class="video-body"><h3>{esc(v['title'])}</h3><p>{esc(v['description'])}</p><div class="video-actions">{external(v['download'],icon('download')+'Download','text-link')}<button class="icon-button jsonly copy-link" data-copy="{esc(v['download'])}" aria-label="Copy link to {esc(v['title'])}">{icon('copy')}</button></div></div></article>'''
    return f'<section id="videos" class="library-section">{section_heading("02","Stories in motion.","Preview a film, then open its collection for the full-resolution download.")}<div class="video-grid">{cards}</div><h3 class="subsection-title">Explore video collections</h3>{collection_cards(DATA["videoCollections"],"film")}</section>'
def photos():
    return f'<section id="photo" class="library-section">{section_heading("03","A closer look.","Facilities, people, events, and products. Find the right photography collection.")}{collection_cards(DATA["photos"],"image")}</section>'
def social():
    cards=''
    for i,c in enumerate(DATA['social'],1):
        cards+=f'''<a class="social-card" href="{esc(c['url'])}" target="_blank" rel="noopener"><div class="social-cover"><img src="{esc(c['image'])}" alt="{esc(c['title'])}" loading="lazy"><span class="social-product">{esc(c['product'])}</span><span class="social-play">{icon('play')}</span><span class="social-views">{esc(c['views'])}<small>plays</small></span></div><div class="social-body"><span class="creator">{esc(c['creator'])}{icon('arrow')}</span><h3>{esc(c['title'])}</h3><p>{esc(c['stats'])}</p></div></a>'''
    sources=''.join(external(c['url'],esc(c['title']),'text-link') for c in DATA['socialSources'])
    return f'<section id="social" class="library-section">{section_heading("04","Out in the world.","Product stories from Kreate and our creator community.")}<div class="social-note">Instagram plays and engagement are a snapshot from August 19, 2026.</div><div class="social-grid">{cards}</div><div class="social-sources"><span>Source collections</span>{sources}</div></section>'
def help_section():
    return f'''<section id="help" class="help-section"><div class="eyebrow">A LITTLE GUIDANCE</div><h2>Get the right file.</h2><div class="help-grid"><div>{icon('download')}<h3>Download the original</h3><p>Open a file or collection and choose Download for the original format. Video previews stream here; full-resolution masters can be large.</p></div><div>{icon('link')}<h3>Share a brand kit</h3><p>Open a brand, then use Copy brand link. The brand-only page is a focused view for partners and collaborators.</p></div><div>{icon('help')}<h3>Need something else?</h3><p>If a collection is unavailable or you need a new asset, contact your Sequent marketing team. The team portal requires sign-in.</p><a class="text-link" href="https://drive.google.com/drive/folders/13UAU7GG64fvu6oaUX1Rw1Mo9eh7eweNr" target="_blank" rel="noopener">Central branding folder ↗</a></div></div></section>'''
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
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Sequent — {title}</title><meta name="description" content="{metadata}"><meta name="theme-color" content="#0c1015"><meta property="og:title" content="Sequent — {title}"><meta property="og:image" content="https://sequent-hq.github.io/sequent-resources/assets/og-card.png"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('sequent-theme')==='light')document.documentElement.classList.add('light')}}catch(e){{}}</script><script src="app.js" defer></script></head><body data-page="{kind}"><a class="skip-link" href="#main">Skip to content</a><div class="intro" aria-hidden="true">{logo('sequent')}<span>RESOURCE LIBRARY</span><i></i></div>{nav(kind)}<div class="page-shell"><header class="topbar"><button class="icon-button menu-button jsonly" aria-label="Open navigation" aria-expanded="false" aria-controls="sidebar">{icon('menu')}</button><div class="breadcrumb">Sequent <span>/</span> <strong>{title}</strong></div><div class="topbar-actions"><a class="text-link full-library" href="index.html">{'Full board' if brand_only else 'Full library'}</a><button class="icon-button jsonly" id="themeToggle" aria-label="Switch to light theme">{icon('sun')}</button></div></header><main id="main"><div class="hero"><div><div class="eyebrow">SHARED ASSETS. CONNECTED BRANDS.</div><h1>{headline}</h1><p>{desc}</p></div>{hero_link}</div><div class="search-area jsonly"><div class="search-field">{icon('search')}<input id="search" type="search" placeholder="{'Search backgrounds…' if bg else 'Search brands, guidelines, templates…'}" aria-label="{'Search backgrounds' if bg else 'Search brand standards and logos' if brand_only else 'Search all resources'}" aria-controls="searchResults" autocomplete="off"><kbd>Ctrl K</kbd></div><div id="searchResults" hidden><div class="search-results-header"><span id="searchCount" role="status"></span><button class="icon-button" id="closeSearch" aria-label="Clear search">{icon('close')}</button></div><div id="searchItems"></div></div></div>{content}<footer><a href="index.html" aria-label="Sequent home">{logo('sequent')}</a><span>Brand resources, all together.</span><span>© 2026 Sequent</span></footer></main></div><dialog id="brandDialog" aria-labelledby="dialogLabel"><div class="dialog-toolbar"><span id="dialogLabel">Brand resources</span><div><button class="icon-button" id="copyBrand" aria-label="Copy brand link">{icon('copy')}</button><button class="icon-button" id="closeBrand" aria-label="Close brand kit">{icon('close')}</button></div></div><div id="brandDialogContent"></div></dialog><dialog id="videoDialog" aria-labelledby="videoTitle"><div class="dialog-toolbar"><h2 id="videoTitle">Video preview</h2><button class="icon-button" id="closeVideo" aria-label="Close video">{icon('close')}</button></div><video controls playsinline preload="metadata"></video><p id="videoError" hidden>The preview could not load. Open the collection below to view or download this film.</p><div class="video-dialog-footer"><a class="button" id="videoDownload" target="_blank" rel="noopener">{icon('download')}Open full-resolution file</a><button class="button" id="copyVideo">{icon('copy')}Copy link</button></div></dialog><div class="toast" id="toast" role="status"></div></body></html>'''
for kind in ['index','brands','backgrounds']:
    (ROOT/f'{kind}.html').write_text(page(kind),encoding='utf-8')
(ROOT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0c1015"/><path d="M9 10h14v4H13v4h10v4H9v-4h10v-4H9z" fill="#62ddf5"/></svg>',encoding='utf-8')
print('Built index.html, brands.html, backgrounds.html from shared source.')
