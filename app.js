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
    (document.querySelector('dialog[open]') || document.body).append($('#toast'));
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
    currentPanel = panel; lastTrigger = trigger || $(`.brand-open[data-brand="${slug}"]`);
    $('#dialogLabel').textContent = `${panel.dataset.name} / Brand resources`;
    dialogContent.append(panel);
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    if (updateHash) history.replaceState(null, '', `#bp-${slug}`);
  }
  $$('.brand-open').forEach(a => a.addEventListener('click', e => {
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
  const sharedFiles = new Map();
  const mimeTypes = { png: 'image/png', jpg: 'image/jpeg', jpeg: 'image/jpeg', svg: 'image/svg+xml', pdf: 'application/pdf' };
  const prepareFile = async button => {
    const path = button.dataset.file;
    if (!navigator.canShare || sharedFiles.has(path) || Number(button.dataset.bytes) > 5 * 1024 * 1024) return;
    sharedFiles.set(path, null);
    try {
      const response = await fetch(path);
      if (!response.ok) throw new Error('File unavailable');
      const blob = await response.blob();
      const extension = path.split('.').pop().toLowerCase();
      sharedFiles.set(path, new File([blob], button.dataset.filename, { type: mimeTypes[extension] || blob.type }));
    } catch (_) { sharedFiles.delete(path); }
  };
  async function shareResource(title, path, file) {
    const url = new URL(path, location.href).href;
    if (!navigator.share) { await copy(url); return; }
    try {
      const data = file && navigator.canShare?.({ files: [file] }) ? { title, files: [file] } : { title, url };
      await navigator.share(data);
    } catch (error) {
      if (error.name !== 'AbortError') await copy(url);
    }
  }
  $$('.share-kit').forEach(button => button.addEventListener('click', () => shareResource(button.dataset.title, `brands.html#bp-${button.dataset.brand}`)));
  $$('.share-asset').forEach(button => button.addEventListener('click', () => shareResource(button.dataset.title, button.dataset.file, sharedFiles.get(button.dataset.file))));
  $$('.copy-asset').forEach(button => button.addEventListener('click', () => copy(new URL(button.dataset.file, location.href).href)));
  $$('.resource-jump').forEach(link => link.addEventListener('click', e => {
    e.preventDefault();
    document.getElementById(link.getAttribute('href').slice(1))?.scrollIntoView({ block: 'start' });
  }));
  if ('IntersectionObserver' in window && navigator.canShare) {
    const ready = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { prepareFile(entry.target); ready.unobserve(entry.target); }
    }), { rootMargin: '100px' });
    $$('.share-asset').forEach(button => ready.observe(button));
  }
  $$('.logo-downloads').forEach(section => {
    const applyFormat = format => {
      $$('.logo-filter', section).forEach(button => {
        button.classList.toggle('active', button.dataset.logoFormat === format);
        button.setAttribute('aria-pressed', String(button.dataset.logoFormat === format));
      });
      let count = 0;
      $$('.logo-file', section).forEach(card => {
        card.hidden = format !== 'all' && card.dataset.format !== format;
        if (!card.hidden) count++;
      });
      $('.logo-visible-count', section).textContent = `${count} file${count === 1 ? '' : 's'}`;
    };
    $$('.logo-filter', section).forEach(button => button.addEventListener('click', () => applyFormat(button.dataset.logoFormat)));
    applyFormat(section.dataset.defaultFormat);
  });
  const fromHash = () => {
    if (!location.hash.startsWith('#film-') && videoDialog?.open) closeVideoForNavigation();
    if (location.hash.startsWith('#bp-')) openBrand(location.hash.slice(4), null, false);
    else if (dialog?.open) dialog.close();
  };
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
  let currentVideoLink = '', currentVideoBrand = '';
  let videoReturnFocus = null, videoClosedForNavigation = false;
  function openVideo(a, autoplay = true, returnFocus = a) {
    if (dialog?.open) dialog.close();
    videoReturnFocus = returnFocus;
    videoClosedForNavigation = false;
    $('#videoTitle').textContent = a.dataset.title;
    $('#videoDownload').href = a.dataset.video;
    $('#videoCollection').href = a.dataset.download;
    currentVideoLink = new URL(`./#${a.dataset.videoId}`, location.href).href;
    currentVideoBrand = a.dataset.videoBrand;
    $('#videoError').hidden = true; player.poster = a.dataset.poster || ''; player.src = a.dataset.video;
    if (!videoDialog.open) videoDialog.showModal();
    if (autoplay) player.play().catch(() => {});
  }
  function closeVideoForNavigation() {
    videoClosedForNavigation = true;
    player.pause();
    videoDialog.close();
  }
  $$('[data-video]').forEach(a => a.addEventListener('click', e => {
    if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    e.preventDefault(); openVideo(a);
  }));
  player?.addEventListener('error', () => { $('#videoError').hidden = false; });
  $('#closeVideo')?.addEventListener('click', () => videoDialog.close());
  videoDialog?.addEventListener('close', () => {
    player.pause(); player.removeAttribute('src'); player.removeAttribute('poster'); player.load();
    if (!videoClosedForNavigation) {
      if (location.hash.startsWith('#film-')) history.replaceState(null, '', `#videos-${currentVideoBrand}`);
      if (videoReturnFocus?.isConnected) videoReturnFocus.focus({ preventScroll: true });
    }
    videoClosedForNavigation = false;
  });
  videoDialog?.addEventListener('click', e => {
    const r = videoDialog.getBoundingClientRect();
    if (e.target === videoDialog && (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom)) videoDialog.close();
  });
  $('#copyVideo')?.addEventListener('click', () => copy(currentVideoLink));
  function videoFromHash() {
    if (!location.hash.startsWith('#film-')) return;
    const trigger = document.getElementById(location.hash.slice(1))?.querySelector('[data-video]');
    if (trigger) openVideo(trigger, false);
    else if (videoDialog?.open) closeVideoForNavigation();
  }
  fromHash(); videoFromHash();
  window.addEventListener('hashchange', () => { fromHash(); videoFromHash(); });
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
    $$('.logo-file', panel).forEach(card => {
      const a = $('.logo-save', card), title = `${$('.logo-name', card).textContent.trim()} · ${card.dataset.format}`;
      index.push({ title, context: `${name} · Download logo`, href: a.getAttribute('href'), download: a.getAttribute('download'), text: `${name} logo logos ${title}`.toLowerCase() });
    });
    $$('a[href]', panel).forEach(a => {
      if (a.closest('.logo-file')) return;
      const title = $('.nm', a)?.textContent.trim() || $('.cl', a)?.textContent.trim() || a.textContent.trim();
      if (!title) return;
      index.push({ title, context: name, href: a.getAttribute('href'), download: a.getAttribute('download'), text: `${name} ${title} ${$('.mt', a)?.textContent || ''}`.toLowerCase() });
    });
  });
  $$('.video-card, a.collection-card, .social-card, .background-card').forEach(card => {
    const link = card.matches('a') ? card : $('a', card);
    const title = $('h3, h4', card)?.textContent.trim();
    if (!title || !link) return;
    const context = card.classList.contains('video-card') ? `${card.dataset.brandLabel || ''} · Video` : card.classList.contains('social-card') ? 'Social content' : card.classList.contains('background-card') ? 'Call background' : 'Collection';
    index.push({ title, context, href: link.getAttribute('href'), video: link.dataset.video ? link : null, text: `${title} ${context} ${card.textContent}`.toLowerCase() });
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
      if (row.download !== undefined && row.download !== null) a.setAttribute('download', row.download);
      const span = document.createElement('span'), name = document.createElement('b'), meta = document.createElement('small');
      name.textContent = row.title; meta.textContent = row.context; span.append(name, meta); a.append(span);
      if (row.slug) a.addEventListener('click', e => { e.preventDefault(); clearSearch(); openBrand(row.slug, search); });
      else if (row.video) a.addEventListener('click', e => {
        if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
        e.preventDefault(); clearSearch(); openVideo(row.video, true, search);
      });
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
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); if (dialog?.open) { focusSearchOnClose = true; dialog.close(); } if (videoDialog?.open) { videoReturnFocus = search; videoDialog.close(); } search.focus(); }
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
