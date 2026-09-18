# Sequent resource library

A redesigned, static resource library with three entry points:

- `index.html` — the complete library.
- `brands.html` — brand kits and retail partner standards.
- `backgrounds.html` — 20 downloadable call backgrounds.

Open `index.html` to review locally, or serve this folder with any static web server. Keep the folders together so local downloads and images work. External collections, previews, and social links require an internet connection.

## What changed

- One-click logo ZIPs for all 16 brand kits and 214 individually downloadable files, hosted on this site.
- PNG/SVG/JPG and design-file filters, lightweight previews, direct file links, and quick access to guidelines.
- Native sharing where supported, with file sharing when supported and prepared; other browsers copy a shareable link. Source collections remain available as secondary links.
- Calmer dark and light themes, with the original white and full-color brand marks.
- Persistent section navigation, resource search, family/retailer filters, and responsive layouts.
- Accessible brand drawers with shareable links, native expandable file groups, and keyboard controls.
- Video previews, downloadable local assets, and a filterable background gallery.
- One shared content source for both brand pages; gallery counts are derived automatically.
- Content remains accessible without JavaScript.

## Edit and rebuild

Update `source/content.json`, then run `python build.py`. This uses Python's standard library only. The generated HTML works without Python, a framework, a build server, or installed packages. Styling is in `styles.css`; interactions are in `app.js`.

All 16 original brand kits, 12 corporate videos, 9 video collections, 9 photography entries, 8 social cards, and 20 background files are retained. Four inaccessible collections remain visible as unavailable entries, with their source destinations preserved in the content file.

## Access notes — checked September 17, 2026

These collections redirected anonymous visitors to Bynder's no-access page, so their links are inactive in the redesign:

- OGO distributor assets.
- Ranch Road Brand Anthem.
- 2301 Industrial Drive photography.
- Customer Installs / UGC.

The general brand portal requires team sign-in and is labeled accordingly. Representative Sequent, Energize, and USE guideline previews were accessible anonymously. A Sequent PDF download timed out; not every third-party file download has been verified. External sharing settings remain controlled by their owners. Instagram may require sign-in.

Social metrics retain the original August 19, 2026 snapshot date; they are not presented as live. Existing refresh automations were not modified. Any future automation should update `source/content.json` and rebuild the pages.

## Site routes

The existing GitHub Pages routes are preserved: https://sequent-hq.github.io/sequent-resources/ is the full board, https://sequent-hq.github.io/sequent-resources/brands.html is the focused brand standards and logos page, and backgrounds.html is the background gallery. Brand kits keep their established assets and local download paths.

Checked: local resource paths, fragment targets, duplicate IDs, brand-page parity, search, filters, representative drawer groups, themes, keyboard shortcut, mobile overflow at 390px and 320px, and a script-free fallback.

## Logo files — September 17, 2026

The catalog contains 209 existing/source original files and five clearly labeled source-provided web renditions. Four blank white JPGs from the OGO source collection are excluded; their usable PNG/EPS variants remain. Filenames, formats, dimensions, and file sizes are shown in each kit. Per-brand ZIPs contain the same selectable files. Small or low-resolution source logos are retained at their real resolution; no logos were redrawn or upscaled. Downloads and previews are local. Source links still point to the original brand collections.

Add or update logo records under each brand's `logos` array and keep `logo_pack` ZIP contents in sync, then rebuild. The share button uses the device share menu when supported; the copy button always copies the direct local file URL. The library never sends files to a recipient automatically.
