#!/usr/bin/env python3
"""Build a public-only static deployment package; verify navigation and staging SEO."""
import json, os, re, shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "dist"
PAGES = [
  "index.html", "404.html", "admin/index.html", "about/index.html",
  "contact/index.html", "products/index.html",
  "products/aeroplane-alkatra/index.html",
  "products/urojahaj-alkatra/index.html",
  "products/orbit-steel-care/index.html"
]
FILES = PAGES + ["robots.txt", "favicon.svg"] + sorted(
  p.relative_to(ROOT).as_posix() for p in (ROOT / "assets").rglob("*")
  if p.is_file() and p.suffix.lower() in {".css", ".js", ".svg", ".png", ".jpg", ".jpeg", ".webp", ".avif"}
)
def main():
    for file in FILES:
        if not (ROOT / file).is_file():
            raise SystemExit("Missing deployment file: " + file)
    referenced = set()
    for page in PAGES:
        html = (ROOT / page).read_text(encoding="utf-8")
        if '<title>' not in html or 'noindex,nofollow,noarchive' not in html:
            raise SystemExit("Invalid title / staging protection: " + page)
        for uri in re.findall(r'\b(?:href|src)="(/[^"#?]*)', html):
            referenced.add("index.html" if uri == "/" else uri.lstrip("/") +
                           ("index.html" if uri.endswith("/") else ""))
    unknown = referenced - set(FILES)
    if unknown:
        raise SystemExit("Broken local links: " + str(sorted(unknown)))
    if "Disallow: /" not in (ROOT / "robots.txt").read_text(encoding="utf-8"):
        raise SystemExit("Staging robots.txt no longer blocks indexing.")
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir()
    for path in FILES:
        output = DEST / path
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / path, output)
    marker = {
      "project": "nazrul-brothers",
      "commit": os.getenv("GITHUB_SHA", "local"),
      "run": os.getenv("GITHUB_RUN_ID", "local"),
      "deployedBuildAt": datetime.now(timezone.utc).isoformat()
    }
    (DEST / "deployment.json").write_text(json.dumps(marker) + "\n", encoding="utf-8")
    (DEST / ".htaccess").write_text("DirectoryIndex index.html index.php default.php\nOptions -Indexes\n", encoding="utf-8")
    print("Validated static site and staged", len(FILES)+2, "public files.")

if __name__ == "__main__":
    main()
