# Sequent resource library

A redesigned, static resource library with three entry points:

- `index.html` — the complete library.
- `brands.html` — brand kits and retail partner standards.
- `backgrounds.html` — 20 downloadable call backgrounds.

Open `index.html` to review locally, or serve this folder with any static web server. Keep the folders together so local downloads and images work. External collections, video playback, and social links require an internet connection.

## What changed

- One-click logo ZIPs for all 16 brand kits and 214 individually downloadable files, hosted on this site.
- PNG/SVG/JPG and design-file filters, lightweight previews, direct file links, and quick access to guidelines.
- Native sharing where supported, with file sharing when supported and prepared; other browsers copy a shareable link. Source collections remain available as secondary links.
- Calmer dark and light themes, with the original white and full-color brand marks.
- Persistent section navigation, resource search, family/retailer filters, and responsive layouts.
- Accessible brand drawers with shareable links, native expandable file groups, and keyboard controls.
- Full-resolution video playback, downloadable local assets, and a filterable background gallery.
- One shared content source for both brand pages; gallery counts are derived automatically.
- Content remains accessible without JavaScript.

## Edit and rebuild

Update `source/content.json`, then run `python build.py`. This uses Python's standard library only. The generated HTML works without Python, a framework, a build server, or installed packages. Styling is in `styles.css`; interactions are in `app.js`.

All 16 original brand kits, 12 existing corporate videos, 9 video collections, 9 photography entries, 8 earlier social cards, and 20 background files are retained. The September 19 update adds the Sequent Platform Video and nine social reels. Four inaccessible collections remain visible as unavailable entries, with their source destinations preserved in the content file.

## Access notes — checked September 17, 2026

These collections redirected anonymous visitors to Bynder's no-access page, so their links are inactive in the redesign:

- OGO distributor assets.
- Ranch Road Brand Anthem.
- 2301 Industrial Drive photography.
- Customer Installs / UGC.

The general brand portal requires team sign-in and is labeled accordingly. Representative Sequent, Energize, and USE guideline previews were accessible anonymously. A Sequent PDF download timed out; not every third-party file download has been verified. External sharing settings remain controlled by their owners. Instagram may require sign-in.

Earlier social metrics remain in the source data for reference but are no longer displayed as current statistics. Existing refresh automations were not modified. Any future automation should update `source/content.json` and rebuild the pages.

## Site routes

The existing GitHub Pages routes are preserved: https://sequent-hq.github.io/sequent-resources/ is the full board, https://sequent-hq.github.io/sequent-resources/brands.html is the focused brand standards and logos page, and backgrounds.html is the background gallery. Brand kits keep their established assets and local download paths.

Checked: local resource paths, fragment targets, duplicate IDs, brand-page parity, search, filters, representative drawer groups, themes, keyboard shortcut, mobile overflow at 390px and 320px, and a script-free fallback.

## Logo files — September 17, 2026

The catalog contains 209 existing/source original files and five clearly labeled source-provided web renditions. Four blank white JPGs from the OGO source collection are excluded; their usable PNG/EPS variants remain. Filenames, formats, dimensions, and file sizes are shown in each kit. Per-brand ZIPs contain the same selectable files. Small or low-resolution source logos are retained at their real resolution; no logos were redrawn or upscaled. Downloads and previews are local. Source links still point to the original brand collections.

Add or update logo records under each brand's `logos` array and keep `logo_pack` ZIP contents in sync, then rebuild. The share button uses the device share menu when supported; the copy button always copies the direct local file URL. The library never sends files to a recipient automatically.

## Videos and social — September 19, 2026

The film library now starts with the featured Sequent Platform Video (5:49, 1080p), followed by 11 Kreate films and two Reinhart Foundation films. Related Kreate and foundation collections appear with their brand. All other product and brand collections remain available below.

Kreate Instagram (@kreate) and TikTok (@kreateusa) have direct links in the main navigation and social section. These profiles were verified through Kreate's own profile/Linktree. The social section features Dad Social's paid HDX Tote Stacker collaboration (July 29, 2026), then eight recent reels published August 28–September 9. The previous eight collaborations remain in an expandable group. Dates and collaboration identities were verified on the original Instagram posts; the featured Dad Social post is not labeled the newest post. Covers are local copies of the observed post thumbnails, and reel links open the originals on Instagram.


## Full-resolution film playback

The 14 film cards use stable GitHub release asset URLs for in-board playback at each source file's native dimensions: 1080p or 4K. Kreate Resin Facility is first in Kreate and uses its official source thumbnail, which also appears while its player loads. Play, Watch film, and video search results use the same player. Each film has a shareable board link; shared links open that film with native playback controls. Download video saves the hosted MP4, and Open collection retains the source destination.

Compatible H.264/AAC originals are retained without re-encoding where possible. Browser-incompatible originals and the oversized Eco Actions master receive high-quality H.264/AAC MP4 playback copies at the original dimensions and frame rate, with metadata at the start of the file for quick playback. The original master files remain available in Bynder. There is no lower-resolution automatic fallback and no expiring signed URL in the published content.

Large video files live in the `video-library-2026-09` GitHub release, separate from the static Pages repository. Their original source metadata and hosted-file checksums are recorded in the content source. To replace a film, publish and verify its new playback asset before changing the corresponding src and rebuilding. Keep original width/height and actual playback dimensions equal. Do not use Bynder's /mp4/ preview derivative as a full-resolution source.

## Sequent video replacement — September 25, 2026

The featured Sequent film now uses the September 21 version 6 supplied through Frame.io, at its native 1920×1080 resolution. The hosted playback file preserves the original audio and video streams, with fast-start metadata for immediate playback. Its poster is a frame from this version, and Open collection links to the supplied Frame.io share. The existing `#film-sequent-platform` sharing link is preserved.
