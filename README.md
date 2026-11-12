# Nazrul & Brothers — Corporate Website

A dependency-free, responsive corporate website staging build featuring a typography-led **50 Years of Proud Legacy** hero, company background, and three signature product pages.

## Pages
- `/` — heritage hero, signature range, legacy and company location
- `/about/` — company story
- `/products/` — signature catalogue
- `/products/aeroplane-alkatra/`
- `/products/urojahaj-alkatra/`
- `/products/orbit-steel-care/`
- `/contact/` — location and enquiry placeholder

## Development only: DO NOT PUBLIC-LAUNCH YET
- Product packaging images and official company logo are pending. The temporary **NB** monogram is not the official logo; no fictitious product images are used.
- No technical product specification, application, safety claim, specific founding year, contact number, email, or address beyond the supplied location has been invented.
- Confirm branding, product ownership and copy with Nazrul & Brothers management.
- Every HTML page has `noindex,nofollow,noarchive`; `robots.txt` blocks crawlers. Keep this restriction until contents and production domain are approved.
- After domain purchase: set full domain-specific canonical URLs, OG image, sitemap.xml, production robots.txt; then remove `noindex`, verify in Search Console and connect analytics after consent/privacy review.
- The product page content is a placeholder pending company-original photography and authoritative pack/TDS details.
- This is a static site for deployment to the *correct* Hostinger website document root; do not overwrite other sites hosted on the account.
- GitHub Actions / scheduled workflows are intentionally not included, to avoid unnecessary automated runs.
- Never commit hosting passwords, GitHub tokens, personal details, or private files.

## Local development
Serve from the project root (root-relative URLs are used):
```bash
python -m http.server 8000
```
Then open http://localhost:8000/.

## Production QA checklist
1. Obtain and approve original Nazrul & Brothers logo and each of the three product image sets.
2. Verify company history wording, product descriptions, current available variants and contact details.
3. Check responsive design on real Android/iOS devices and desktop browsers; test keyboard navigation.
4. Confirm HTTPS and Hostinger directory mapping for the newly purchased domain.
5. Enable canonical, sitemap, indexing and analytics only after approval.

## Domain-free staging and Firebase

Read [DEPLOYMENT.md](./DEPLOYMENT.md). The secure admin scaffold is available at `/admin/` once deployed, but Firebase requires a dedicated project, its public web config, authorized Hostinger hostname, deployed Firestore rules and manually approved admin UID. Hosting and Firebase are not yet connected.
