# Production deployment runbook

## Current readiness

Implementation and local validation are complete. The production Azure subscription must be selected before resource creation. Existing accessible static apps belong to other projects; none were changed. GoDaddy currently holds the domain. On 2026-11-05, `www.tyrus.com` did not resolve; `tyrus.com` resolved to `3.33.130.190` and returned an HTTPS 200 response for a small parked page. This is not the new website.

## Provision a dedicated free resource

Use the intended subscription explicitly, without changing the CLI's global default:

```sh
az group create --subscription <approved-subscription-id> --name rg-tyrus-website --location eastus2
az staticwebapp create --subscription <approved-subscription-id> --resource-group rg-tyrus-website --name tyrus-website --location eastus2 --sku Free
az staticwebapp show --subscription <approved-subscription-id> --resource-group rg-tyrus-website --name tyrus-website --query defaultHostname -o tsv
```

Confirm the resource name is available and the SKU remains Free. Capture the returned Azure hostname; do not guess it.

In Azure, obtain the dedicated app's deployment token and store it as `AZURE_STATIC_WEB_APPS_API_TOKEN` in the GitHub repository's **production environment secret**. Use a protected stdin pipeline or the portal; do not print tokens in logs or store them in files. Set repository variable `AZURE_DEPLOY_ENABLED=true`, then run the deployment workflow on `main`. Verify the Azure hostname serves the Tyrus website before changing DNS.

## GoDaddy DNS and custom domains

Keep the registration at GoDaddy. No nameserver change or registrar transfer is required.

1. In the Azure app's Custom domains page, add `www.tyrus.com` and use its generated verification instructions. At GoDaddy, set `www` CNAME to the **actual Azure defaultHostname**; use TTL 600 if available. Add a validation TXT record only with the exact name and value supplied by Azure.
2. Add `tyrus.com` as the second custom domain. Use Azure's apex-domain TXT validation and follow the supported apex DNS instructions for this exact app. A CNAME cannot be used at the zone apex alongside existing MX records. If GoDaddy cannot support the required alias mechanism, use its HTTPS-capable permanent forwarding to `https://www.tyrus.com/`, preserving paths and queries where supported; verify HTTPS at the apex before accepting this route.
3. Once both are verified, set `www.tyrus.com` as the Azure app's default domain to redirect other bound domains to it. Use Azure's custom-domain/default-domain feature, not a blanket path redirect in the website configuration (which would loop).
4. Preserve all mail-related MX/TXT records, SPF/DKIM/DMARC, unrelated subdomains, and other applications. Replace only website records that conflict with the new binding after the preview has been verified.
5. Wait for Azure's free managed certificates to be issued. Test HTTPS and the canonical redirect from multiple networks after propagation.

## Release verification

```sh
curl -I https://www.tyrus.com/
curl -I https://tyrus.com/
curl -fsS https://www.tyrus.com/sitemap.xml
```

Verify www returns 200 with valid TLS; apex redirects to www without a loop; security headers are present; the exact approved content is live; all five email links target jay@tyrus.com; CSS/JS/favicon load; mobile navigation works. DNS propagation and certificate issuance may take time. Do not report production complete before these checks pass.

## Rollback

Revert the deployment commit on `main` to trigger redeployment of the prior approved source. For the initial domain cutover, retain the prior GoDaddy website record values and restore only those records if needed. Do not change mail records. Keep deployment disabled until the target resource and secret are configured.

## Cost and reference documentation

- [Azure Static Web Apps pricing](https://azure.microsoft.com/en-us/pricing/details/app-service/static/): Free tier $0 within included limits; custom domains and TLS included. No SLA on Free.
- [Hosting plans](https://learn.microsoft.com/en-us/azure/static-web-apps/plans)
- [Custom domains](https://learn.microsoft.com/en-us/azure/static-web-apps/custom-domain)
- [Configuration and headers](https://learn.microsoft.com/en-us/azure/static-web-apps/configuration)
- [Build configuration](https://learn.microsoft.com/en-us/azure/static-web-apps/build-configuration)

GoDaddy registration/renewal remains an existing separate expense. No paid Azure service is required for this implementation.
