# Nazrul & Brothers — Domain-free Staging & Firebase Setup

The site currently uses static HTML + CSS + JS. There is no Node.js runtime or server-side build requirement. No GitHub Actions, cron jobs or active monitoring workflows are needed.

## 1. Hostinger before domain purchase
1. Go to Hostinger hPanel → Websites → Create site.
2. Choose **Custom PHP/HTML** and the **correct hosting plan** (not Website Builder).
3. Choose **Use temporary domain**. Hostinger will assign an address ending in `.hostingersite.com`.
4. In the new, *dedicated* site's dashboard go to **Advanced → Git** (or Websites → Import site → Deploy from GitHub).
5. Connect GitHub using official OAuth, allow access to `creatifybd/nazrul-brothers`, choose `main` and deploy to this new site's own document root, usually `public_html`.
6. Check home, about, products, individual detail pages, contact and `/admin/` over HTTPS.
7. IMPORTANT: Git deployment can overwrite content at the selected destination. Never target another company's website folder. For staging you may temporarily disable automatic deployment and redeploy manually after review.

Hostinger official guides:
- https://www.hostinger.com/support/1583214-how-to-add-a-website-in-hostinger/
- https://www.hostinger.com/support/1583302-how-to-deploy-a-git-repository-in-hostinger/

## 2. Firebase, separate from Joytun and Orbit
1. Create a dedicated Nazrul & Brothers Firebase project using an authorized company-owned Google account. Avoid editing any existing company's Firebase resources.
2. Add a **Web app** in Project Settings, and copy ONLY the public Web SDK config: `apiKey`, `authDomain`, `projectId`, `appId`, optional `measurementId`, into `assets/js/firebase-config.js`. These client values are not service-account secrets. Never paste or commit a Firebase Admin SDK JSON/private key.
3. Enable **Authentication → Google sign-in**.
4. In **Authentication → Settings → Authorized domains**, add the exact temporary Hostinger hostname (without scheme/path). After domain purchase, add the official hostname too.
5. Create **Cloud Firestore** (production rules, not public test rules). Deploy `firebase/firestore.rules` with the Firebase CLI or paste/publish in the Firebase console. Test rules before going live.
6. Go to `https://YOUR-TEMPORARY-HOST/admin/`. Sign in. At first you will see an unauthorized message with your Google Firebase Auth UID.
7. After confirming the UID belongs to an approved administrator, create Firestore document `adminUsers/THAT_UID` using Firebase Console with `active` field of **Boolean true**. Browser users cannot create admin records.
8. Reload admin page, sign in again, edit content. Leave as Draft until company approval; publish only verified text. Firestore read is limited to published documents for the public site.
9. Product images will be linked from supplied originals; Firebase Cloud Storage is intentionally NOT enabled because Cloud Storage requires the Blaze billing plan as of February 3, 2026. Firebase Auth + Firestore can be started without Storage.
10. Do not enable general open rules or use an email string alone as an admin permission check.

## 3. Saturday: custom domain
1. Buy an approved corporate domain and select **Connect domain** for this *same temporary Nazrul & Brothers website*, not another website.
2. Set DNS/nameservers as instructed by Hostinger, check HTTPS / SSL; propagation can take up to 24 hours.
3. Add the official domain to Firebase Authentication authorized domains and test Google login.
4. Only after approval of official product photography, content and contact details: add canonical URLs, OG image, sitemap, JSON-LD, Search Console, and change `robots.txt` and HTML `noindex` meta to permit indexing.
5. Dynamic Firestore content alone is not a substitute for crawlable static product-page copy. Reflect approved product copy in HTML before SEO launch.
6. GA4/analytics is pending company approval and a real measurement ID. No tracking has been claimed active.

## Safety
- No hosting or Firebase credentials should be sent in chat.
- The temporary site is a staging preview, not an approved official public launch.
- Only original unmodified product imagery should be published.
