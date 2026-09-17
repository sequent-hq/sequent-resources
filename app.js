(() => {
  'use strict';
  const $ = (s, root = document) => root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const root = document.documentElement;
  const intro = $('.intro');
  const dismissIntro = () => intro?.classList.add('dismissed');
  intro?.addEventListener('click', dismissIntro);
  setTimeout(dismissIntro, 1200);
  const theme = $('#themeToggle');
  const labelTheme = () => theme?.setAttribute('aria-label', `Switch to ${root.classList.contains('light') ? 'dark' : 'light'} theme`);
  labelTheme();
  theme?.addEventListener('click', () => {
    root.classList.toggle('light');
    try { localStorage.setItem('sequent-theme', root.classList.contains('light') ? 'light' : 'dark'); } catch (_) {}
    labelTheme();
  });
  const menu = $('.menu-button');
  menu?.addEventListener('click', () => {
    document.body.classList.toggle('nav-open');
    menu.setAttribute('aria-expanded', String(document.body.classList.contains('nav-open')));
  });
  $$('.sidebar a').forEach(a => a.addEventListener('click', () => {
    document.body.classList.remove('nav-open');
    menu?.setAttribute('aria-expanded', 'false');
  }));
  let toastTimer;
  const notify = message => {
    $('#toast').textContent = message;
    $('#toast').classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => $('#toast').classList.remove('show'), 2800);
  };
  async function copy(value) {
    try {
      if (navigator.clipboard && window.isSecureContext) await navigator.clipboard.writeText(value);
      else {
        const input = document.createElement('textarea');
        input.value = value; input.style.position = 'fixed'; input.style.opacity = '0';
        const container = document.querySelector('dialog[open]') || document.body;
        container.append(input); input.select();
        const success = document.execCommand('copy'); input.remove();
        if (!success) throw new Error('Copy unavailable');
      }
      notify('Link copied');
    } catch (_) { notify('Could not copy. Copy the address from your browser.'); }
  }
  const dialog = $('#brandDialog'), store = $('#panelStore'), dialogContent = $('#brandDialogContent');
  let currentPanel = null, lastTrigger = null, focusSearchOnClose = false;
  const restorePanel = () => {
    if (currentPanel && store) store.append(currentPanel);
    currentPanel = null;
  };
  const clearBrandHash = () => {
    if (location.hash.startsWith('#bp-')) history.replaceState(null, '', location.pathname + location.search + '#brands');
  };
  function openBrand(slug, trigger, updateHash = true) {
    const panel = document.getElementById(`bp-${slug}`);
    if (!panel || !store) return;
    restorePanel();
    currentPanel = panel; lastTrigger = trigger || $(`.brand-card[data-brand="${slug}"]`);
    $('#dialogLabel').textContent = `${panel.dataset.name} / Brand resources`;
    dialogContent.append(panel);
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    if (updateHash) history.replaceState(null, '', `#bp-${slug}`);
  }
  $$('.brand-card').forEach(a => a.addEventListener('click', e => {
    if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    e.preventDefault(); openBrand(a.dataset.brand, a);
  }));
  $('#closeBrand')?.addEventListener('click', () => dialog.close());
  dialog?.addEventListener('click', e => { if (e.target === dialog && e.clientX < dialog.getBoundingClientRect().left) dialog.close(); });
  dialog?.addEventListener('close', () => { restorePanel(); clearBrandHash(); if (focusSearchOnClose) { focusSearchOnClose = false; $('#search')?.focus(); } else lastTrigger?.focus({ preventScroll: true }); });
  $('#copyBrand')?.addEventListener('click', () => {
    if (!currentPanel) return;
    const url = new URL('brands.html', location.href);
    url.hash = currentPanel.id; copy(url.href);
  });
  const fromHash = () => {
    if (location.hash.startsWith('#bp-')) openBrand(location.hash.slice(4), null, false);
    else if (dialog?.open) dialog.close();
  };
  fromHash(); window.addEventListener('hashchange', fromHash);
  $$('.filter[data-filter]').forEach(button => button.addEventListener('click', () => {
    $$('.filter[data-filter]').forEach(b => { b.classList.toggle('active', b === button); b.setAttribute('aria-pressed', String(b === button)); });
    let count = 0;
    $$('.brand-card').forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter; if (!card.hidden) count++; });
    $('#brandCount').textContent = `${count} collections`;
  }));
  const bgFilters = $$('.filter[data-bg]');
  function filterBackgrounds(value) {
    bgFilters.forEach(b => { b.classList.toggle('active', b.dataset.bg === value); b.setAttribute('aria-pressed', String(b.dataset.bg === value)); });
    $$('[data-gallery]').forEach(s => { s.hidden = value !== 'all' && s.dataset.gallery !== value; });
  }
  bgFilters.forEach(b => b.addEventListener('click', () => { filterBackgrounds(b.dataset.bg); history.replaceState(null, '', b.dataset.bg === 'all' ? location.pathname : `#${b.dataset.bg}`); }));
  if (bgFilters.some(b => b.dataset.bg === location.hash.slice(1))) filterBackgrounds(location.hash.slice(1));
  const videoDialog = $('#videoDialog'), player = $('video', videoDialog);
  $$('[data-video]').forEach(a => a.addEventListener('click', e => {
    if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    e.preventDefault(); $('#videoTitle').textContent = a.dataset.title;
    $('#videoDownload').href = a.dataset.download;
    $('#videoError').hidden = true; player.src = a.dataset.video;
    videoDialog.showModal(); player.play().catch(() => {});
  }));
  player?.addEventListener('error', () => { $('#videoError').hidden = false; });
  $('#closeVideo')?.addEventListener('click', () => videoDialog.close());
  videoDialog?.addEventListener('close', () => { player.pause(); player.removeAttribute('src'); player.load(); });
  videoDialog?.addEventListener('click', e => {
    const r = videoDialog.getBoundingClientRect();
    if (e.target === videoDialog && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom)) videoDialog.close();
  });
  $('#copyVideo')?.addEventListener('click', () => copy($('#videoDownload').href));
  $$('.copy-link').forEach(b => b.addEventListener('click', () => copy(b.dataset.copy)));
  $$('img').forEach(img => {
    const fallback = () => {
      img.hidden = true;
      if (img.closest('.cbx') && !$('.image-missing', img.parentElement)) {
        const label = document.createElement('span'); label.className = 'image-missing'; label.textContent = 'Preview unavailable'; img.parentElement.append(label);
      }
    };
    img.addEventListener('error', fallback);
    if (img.complete && !img.naturalWidth) fallback();
  });
  const search = $('#search'), results = $('#searchResults'), items = $('#searchItems');
  const index = [];
  $$('.brand-panel').forEach(panel => {
    const slug = panel.id.slice(3), name = panel.dataset.name;
    index.push({ title: name, context: 'Brand kit', slug, text: name.toLowerCase() });
    $$('a[href]', panel).forEach(a => {
      const title = $('.nm', a)?.textContent.trim() || $('.cl', a)?.textContent.trim() || a.textContent.trim();
      if (!title) return;
      index.push({ title, context: name, href: a.getAttribute('href'), text: `${name} ${title} ${$('.mt', a)?.textContent || ''}`.toLowerCase() });
    });
  });
  $$('.video-card, a.collection-card, .social-card, .background-card').forEach(card => {
    const link = card.matches('a') ? card : $('a', card);
    const title = $('h3', card)?.textContent.trim();
    if (!title || !link) return;
    const context = card.classList.contains('video-card') ? 'Video' : card.classList.contains('social-card') ? 'Social content' : card.classList.contains('background-card') ? 'Call background' : 'Collection';
    index.push({ title, context, href: link.getAttribute('href'), text: `${title} ${context} ${card.textContent}`.toLowerCase() });
  });
  function clearSearch() { search.value = ''; results.hidden = true; items.replaceChildren(); }
  $('#closeSearch')?.addEventListener('click', () => { clearSearch(); search.focus(); });
  search?.addEventListener('input', () => {
    const words = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    if (!words.length) { clearSearch(); return; }
    const matches = index.filter(row => words.every(word => row.text.includes(word)));
    const unique = matches.filter((row, i, all) => all.findIndex(other => other.title === row.title && other.context === row.context && other.href === row.href) === i);
    results.hidden = false; items.replaceChildren();
    $('#searchCount').textContent = `${unique.length} result${unique.length === 1 ? '' : 's'}${unique.length > 40 ? ' · showing the first 40' : ''}`;
    unique.slice(0, 40).forEach(row => {
      const a = document.createElement('a'); a.className = 'search-result'; a.href = row.slug ? `#bp-${row.slug}` : row.href;
      const span = document.createElement('span'), name = document.createElement('b'), meta = document.createElement('small');
      name.textContent = row.title; meta.textContent = row.context; span.append(name, meta); a.append(span);
      if (row.slug) a.addEventListener('click', e => { e.preventDefault(); clearSearch(); openBrand(row.slug, search); });
      else if (/^https?:/.test(row.href)) { a.target = '_blank'; a.rel = 'noopener'; }
      items.append(a);
    });
    if (!unique.length) { const p = document.createElement('p'); p.className = 'search-empty'; p.textContent = 'No matching resources. Try a brand name, “logos,” or “PowerPoint.”'; items.append(p); }
  });
  search?.addEventListener('keydown', e => { if (e.key === 'ArrowDown') { e.preventDefault(); $('a', items)?.focus(); } });
  items?.addEventListener('keydown', e => {
    const links = $$('a', items), at = links.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); links[Math.min(at + 1, links.length - 1)]?.focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); at <= 0 ? search.focus() : links[at - 1].focus(); }
  });
  document.addEventListener('click', e => { if (!e.target.closest('.search-area')) results.hidden = true; });
  search?.addEventListener('focus', () => { if (search.value.trim()) results.hidden = false; });
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); if (dialog?.open) { focusSearchOnClose = true; dialog.close(); } if (videoDialog?.open) videoDialog.close(); search.focus(); }
    if (e.key === 'Escape') { dismissIntro(); clearSearch(); document.body.classList.remove('nav-open'); menu?.setAttribute('aria-expanded','false'); }
  });
  const sections = $$('.library-section');
  if (sections.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { if (entry.isIntersecting) $$('.nav-link[data-section]').forEach(a => a.classList.toggle('active', a.dataset.section === entry.target.id)); });
    }, { rootMargin: '-12% 0px -65% 0px', threshold: 0 });
    sections.forEach(section => observer.observe(section));
  }
})();
