# Tyrus LLC — Corporate Website

Build 01 is a responsive, dependency-free, single-page website for executive technology consulting. All approved sections are included: hero, about, six expertise areas, four-stage approach, leadership, contact, and footer.

## Local development and build

Requires Node.js 22+ and Python 3. No package installation is needed.

```sh
npm run dev
# Open http://127.0.0.1:4173
npm run build
```

`dist/` is the complete deployable website. The build command validates the ready-to-serve static files and JavaScript syntax; no compilation or bundling is necessary. `npm test` runs the same release gate.

## Validation

The automated gate checks links, anchor destinations, all five email links, required metadata, heading order, document language, accessible relationships, local assets, text palette contrast, reduced-motion/focus styles, sitemap, security-header configuration, and a 100 KB payload budget. These baseline accessibility checks are not a full WCAG audit.

Browser review covered 320, 390, 768, and 1440 pixel viewports without horizontal overflow. Mobile menu opening, anchor selection, closing, Escape dismissal, and direct email destinations were verified. The browser reported no warnings or errors. See `docs/screenshots/` for desktop/mobile captures.

## Hosting and deployment

Configured production host: **Azure Static Web Apps Free**, in Recoup AR - Nonproduction. Live Azure URL: https://wonderful-glacier-0e9abc00f.6.azurestaticapps.net/. Custom-domain activation awaits GoDaddy DNS changes. Expected hosting cost is $0/month within the free tier's limits; domain registration remains separately billed by GoDaddy. No database, backend, paid API, or tracking service is used. Free hosting has no production SLA; assess Standard separately if an SLA is required.

The GitHub validation workflow runs on pushes and pull requests. The Azure deployment workflow runs on `main` pushes or manual dispatch only after repository variable `AZURE_DEPLOY_ENABLED` is set to `true`. It validates before publishing and reads `AZURE_STATIC_WEB_APPS_API_TOKEN` from the `production` environment's secrets. Never commit this token.

The source can also be served through a private Sites review preview. `.openai/hosting.json` identifies that review site; it is not Azure production configuration. The Azure security headers in `dist/staticwebapp.config.json` take effect on Azure, not the local Python server or necessarily the review host.

See [deployment runbook](docs/deployment.md) for provisioning, DNS, HTTPS, activation, and rollback.

## Structure

- `dist/index.html`: approved content and SEO/social metadata
- `dist/styles.css`: responsive styling, geometric illustration, and reduced-motion support
- `dist/script.js`: accessible mobile menu and copyright year
- `dist/favicon.svg`: single-color T mark
- `dist/sitemap.xml`, `dist/robots.txt`: search discovery
- `dist/staticwebapp.config.json`: Azure security headers and index redirect
- `scripts/validate.py`: dependency-free release checks
- `.github/workflows/`: validation and conditional Azure deployment

All contact links use `mailto:jay@tyrus.com`. The TYRUS wordmark uses one color. No client names, endorsements, metrics, credentials, or biography beyond the approved brief are included.
