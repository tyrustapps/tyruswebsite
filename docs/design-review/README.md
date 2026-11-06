# Tyrus coastal redesign — TYRUS-DESIGN-002

Review implementation; no merge or production deployment. The current upstream baseline was verified as `e2ddf64ada0bd10403c12ce45488ebf54937f7c5` on November 5, 2026 (America/Los_Angeles).

## What changed

The geometric illustration is replaced with the supplied coastal photograph spanning the hero and navigation. Libre Caslon Display headlines, DM Sans body text, restrained glass navigation and a localized dark overlay connect the visual treatment to Catalyst. The hero preserves the open ocean and sunset on the right at desktop sizes. Mobile allows natural vertical flow.

The seven-section page retains all six service offerings and four methodology stages. About and Leadership use the brief's approved copy; the 35-year claim describes Jay Clem's professional experience. The persistent navigation gains a dark surface after scrolling and maintains mobile-menu behavior. A focusable main target fixes skip-link keyboard focus. Existing canonical/title/description, five email links, sitemap, robots, favicon and security configuration are retained. Open Graph photography is added. No framework, backend, form, theme switcher or paid service was added.

## Design provenance and adaptation

- Brief: supplied TYRUS-DESIGN-002, November 5, 2026.
- [Catalyst HIG](https://docs.google.com/document/d/16XJq_smv-uFBwco1tQnnd5py8pbjp5suUTz3LFiQZWc/edit), retrieved in this chat. The source remains labeled Draft.
- Approved reference: `tyrustapps/pcip`, commit `4e7791e`, `apps/workspace-web/src/experience/coastal-light.css` and `moonlight-night.css`; inspected with `git show` in the local Catalyst checkout. Also inspected the CAT-UX-006A corrected-night screenshot.
- Directly reused semantic values: paper `#f8faf7`, ink `#103b49`, text `#152b35`, muted `#53656b`, sea glass `#eaf5f3`, bronze text `#8b5428`; night `#102b38`, ivory `#f1f4f0`, night muted `#c4d5d6`, sand `#d9c19a`, action `#c2e5df`.
- Local font binaries and OFL notices copied from the Catalyst reference. All assets are served from the same origin, preserving the existing CSP.
- Tyrus deliberately remains a scrolling marketing site per the brief; Catalyst's application shell, viewport-only scrolling, rails and module controls are not imported. These changes do not claim Figma pixel parity or constitute approval of the draft HIG. Catalyst files are unchanged.

## Review artifacts

- [Desktop hero](desktop-hero.png) / [full page](desktop-full.png), 1440 × 900 viewport.
- [Mobile hero](mobile-hero.png) / [full page](mobile-full.png), 390 × 844 viewport.
- [Browser results](browser-results.json).
- [Photographic contrast measurements](photo-contrast.json).
- [Asset provenance](assets.json).

## Verification

`npm run build` and `npm test` pass 95 checks covering local assets and responsive image references, anchors, mail links, heading structure, metadata, semantic color pairings, security headers and payload budgets. JavaScript syntax validation passes. `git diff --check` passes.

Chromium verification covers 1920×1080, 1440×900, 1280×800, 1024×768, 768×1024, 390×844 and 320×740, plus 720×450 (the CSS viewport equivalent of a 1440×900 display at 200% zoom). This last test verifies reflow, not native browser zoom UI or assistive technology. All runs use DPR 1. No horizontal overflow, missing fonts, broken images, page errors or failed HTTP resources were observed. Measured CLS is 0 at all tested sizes. Six services and all five email destinations are verified.

Keyboard checks cover the skip link moving focus to main, mobile Menu expansion, Escape closing and restoring focus, and section selection closing the menu. Scrolled header styling and section-target clearance are checked. Reduced-motion mode disables smooth scrolling. Axe WCAG 2 A/AA, 2.1 AA and 2.2 AA scans report no violations in the tested default layouts. Photo contrast remains marked incomplete by axe, so it was assessed separately: sampled pixels under 95 text rectangles at four representative viewports met the applicable 3:1 large-text or 4.5:1 normal-text threshold. Sampling is conservative across entire rectangles, not only glyph positions. These checks are not a full WCAG certification or a screen-reader audit.

Performance figures are local observations, not a network-throttled Lighthouse score: code/metadata ~24 KB, fonts ~74 KB, hero WebP 75 KB / 156 KB / 256 KB. At DPR 1, observed resource bodies were approximately 162 KB on narrow screens, 243 KB at 1024px and 343 KB on desktop, excluding the HTML response. The full distribution is approximately 1.094 MB and contains mutually exclusive image sizes, JPEG fallback, social image and font licenses; browsers do not download all variants. Higher-density screens can select larger variants. WebP is paired with a JPEG fallback; AVIF was unnecessary for this small source asset.

## Explicit performance budget change

The former 100 KB total validation counted only root-level files. The revised validator recursively counts all distribution files and retains a 100 KB ceiling for code and metadata. Additional limits: all fonts <120 KB, complete distribution <1.4 MB; 768/1200/1672 WebP <100/180/300 KB respectively, JPEG fallback <350 KB, social JPEG <220 KB. The original PNG stays outside `dist` and is never shipped by the Azure workflow.

## Reproduction

Production build remains dependency-free: `npm run build`. To regenerate images, install Pillow in a temporary virtual environment and run `scripts/optimize-images.py` with that interpreter. To reproduce browser QA, install Playwright with Chromium and axe-core in a separate authoring environment, run a local server on port 4175, then run:

```sh
PLAYWRIGHT_MODULE=/absolute/path/to/playwright AXE_MODULE=/absolute/path/to/axe-core node scripts/browser-review.cjs
```

The review script writes screenshots and JSON results into this folder. No browser-testing libraries are required by the delivered website or CI build.

## Release decision

The design is ready for Product Owner visual review. Merge and production deployment remain separate approval steps. No domain, DNS, Azure resource, deployment workflow or security-header changes were made. The existing Azure workflow deploys only on `main` pushes or manual dispatch; this review branch does not trigger production deployment.
