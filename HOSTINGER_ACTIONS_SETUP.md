# Nazrul & Brothers — GitHub Actions → Hostinger

The workflow at `.github/workflows/deploy-hostinger.yml` automatically validates relevant changes to `main`. It deploys to Hostinger only after the one-time safety configuration below is complete. No manual ZIP upload or Hostinger Git integration is needed.

## One-time Hostinger setup

1. Go to Hostinger hPanel → Websites → **coral-oyster-225966.hostingersite.com** → Manage site → **Files → FTP Accounts**.
2. Create an **additional FTP account restricted to Nazrul & Brothers' website folder only**. This matters because the same hosting account contains other websites. Confirm its FTP IP and the exact allowed remote path from the FTP Accounts screen.
3. If you cannot restrict the FTP account to this site, **do not enable deployment**. Check the directory mapping first to protect Joytun, Orbit, and other hosted sites.

## GitHub configuration

Go to https://github.com/creatifybd/nazrul-brothers/settings/secrets/actions

Under **Repository secrets**, add:

| Secret | Value |
| --- | --- |
| `FTP_SERVER` | Hostinger FTP server IP / hostname from FTP Accounts |
| `FTP_USERNAME` | New Nazrul-only FTP username |
| `FTP_PASSWORD` | New Nazrul-only FTP password |

**Never send the password or private keys in chat or commit them to GitHub source.**

Under **Repository variables**, add:

| Variable | Value |
| --- | --- |
| `FTP_SERVER_DIR` | Exact Hostinger FTP path to this site's document root, e.g. the scoped account's `/public_html` or `/`, **not an assumed shared path** |
| `HOSTINGER_FTP_SCOPED` | `true` only after verifying the FTP account is limited to Nazrul's folder |
| `FTP_SECURE` | `true` only. Plaintext FTP is rejected. |
| `HOSTINGER_FTP_PASSWORD_ROTATED` | `true` only after the previously exposed dedicated FTP password is rotated and `FTP_PASSWORD` is updated. |
| `SITE_URL` | `https://coral-oyster-225966.hostingersite.com` |
| `HOSTINGER_DEPLOY_ENABLED` | `true` **LAST**, after all values and permissions are verified |

GitHub → Actions → **Deploy Nazrul & Brothers to Hostinger** → Run workflow for the first deployment. After a successful run, further changes to the site on `main` deploy automatically.

## What happens on each deployment?

1. Validate the site's pages, asset paths and staging indexing protection.
2. Copy only site files to `dist/`. Admin SDK service-account files, Firestore rules, developer notes and Git metadata are NEVER uploaded.
3. Upload via FTP/FTPS to the *existing confirmed destination*, assets first and HTML last. The workflow does not delete any remote files or search fallback directories.
4. Check that `https://coral-oyster-225966.hostingersite.com/deployment.json` serves the exact current Git SHA, then verify the homepage, Admin Panel and product page.
5. If the upload directory is wrong, the site still shows Coming Soon, or the verification fails, the deployment run is marked FAILED. A validation-only success is **not** proof of hosting success.

## Security notes

- Read-only GitHub permissions; checkout is pinned to a vetted commit SHA.
- No `schedule` or `pull_request_target`; only relevant main-branch pushes or an authorized manual dispatch.
- Each deployment waits for the previous run rather than canceling an upload.
- Separate Hostinger FTP account with limited folder access is essential.
- Certificate-verified FTPS is mandatory. SFTP requires a separately reviewed account scope and a trusted Hostinger host-key fingerprint.
- No bulk cleanup / dangerous-clean-slate or remote file deletion.
- Staging website stays `noindex` until the company approves the official logo, product images and content.
- When Saturday's custom domain is connected, update the `SITE_URL` variable and Firebase Authorized Domains; do not change the confirmed FTP target unless Hostinger's actual directory changes.

Official Hostinger FTP account instructions: https://www.hostinger.com/support/1583246-how-to-create-additional-ftp-accounts-in-hostinger/

## FTPS certificate mismatch diagnosed on 12 November 2026

A read-only diagnostic run confirmed `CERTIFICATE_VERIFY_FAILED: IP address mismatch` when `FTP_SERVER=195.35.15.205` because the presented TLS certificate covers `*.hstgr.io` and `hstgr.io` rather than the bare IP. This is **not** proof of bad FTP credentials. Do not disable TLS certificate verification.

In Hostinger hPanel → **Hosting plan → Plan Details → Server Details → Server Name**, identify the precise `*.hstgr.io` hostname for the hosting plan containing the Nazrul & Brothers website. Do **not** reuse a hostname from Joytun or Orbit without checking. Replace GitHub's **FTP_SERVER secret** with that exact hostname. Our test and deploy scripts require DNS for the new hostname to resolve to the known FTP IP `195.35.15.205`; otherwise they stop without sending credentials. Retest **Inspect Hostinger FTP (read-only)**. Leave `HOSTINGER_DEPLOY_ENABLED` unset until FTP login and document-root isolation have been confirmed.

## Verified follow-up: 13 November 2026

hPanel shows Business Web Hosting, server name `server1221`, FTP IP `195.35.15.205`, and dedicated account `u104160495.nazruldeploy` restricted to `/home/u104160495/domains/coral-oyster-225966.hostingersite.com/public_html`.

The account's displayed active hostname `ftp.coral-oyster-225966.hostingersite.com` resolves to `free.cdn.hstgr.net` and CDN addresses `147.79.69.55` / `88.222.243.128`, not the FTP server. A no-credential FTPS connection timed out. The most recent diagnostic run failed to obtain a certificate before the login step. Do not treat this as a password failure.

SSH is inactive. hPanel lists port `65002` and hosting-account username `u104160495`, not the dedicated site FTP username. Do not enable account-wide SSH deployment as a substitute for verifying site isolation. Obtain a certificate-matching endpoint from Hostinger or an explicitly approved isolated SFTP arrangement. No TLS/SSH verification bypass is acceptable.

The diagnostic workflow is manual-only. Before authenticating it now requires the password-rotation gate. If Hostinger supplies a different verified FTPS hostname, update the diagnostic's explicit hostname guard after verifying its certificate and address; do not blindly retry the current CDN endpoint.
