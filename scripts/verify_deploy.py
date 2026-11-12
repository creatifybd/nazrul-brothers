#!/usr/bin/env python3
"""Verify Hostinger serves this exact GitHub Actions commit after FTP upload."""
import json, os, time
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

url = os.getenv("SITE_URL", "https://coral-oyster-225966.hostingersite.com").rstrip("/")
sha = os.getenv("GITHUB_SHA", "").strip()
if urlsplit(url).scheme != "https" or not urlsplit(url).hostname or not sha:
    raise SystemExit("SITE_URL must use HTTPS and GITHUB_SHA must exist.")

def fetch(path):
    req = Request(url+path, headers={"Cache-Control":"no-cache","User-Agent":"NazrulBrothersDeploymentVerifier/1.0"})
    with urlopen(req, timeout=18) as response:
        return response.read(180_000).decode("utf-8", errors="replace")

for attempt in range(1, 4):
    try:
        marker = json.loads(fetch("/deployment.json?commit="+sha))
        if marker.get("project") != "nazrul-brothers" or marker.get("commit") != sha:
            raise ValueError("The live deployment.json does not match this commit.")
        for route, expected in [
          ("/", "Nazrul"),
          ("/admin/", "Content Admin"),
          ("/products/urojahaj-alkatra/", "Urojahaj Alkatra")
        ]:
            if expected not in fetch(route):
                raise ValueError("Incorrect live HTML at "+route)
        print("Verified live Nazrul & Brothers deployment:", sha, "at", url)
        raise SystemExit(0)
    except Exception as err:
        print(f"Verification {attempt}/3 failed: {err}")
        if attempt < 3:
            time.sleep(5)
raise SystemExit("Deployment verification FAILED: check FTP_SERVER_DIR and Hostinger Coming Soon settings.")
