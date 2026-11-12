#!/usr/bin/env python3
"""Deploy public files using the isolated Nazrul & Brothers FTP account only.

FTPS first. Plain FTP only if explicitly selected; no automatic downgrade.
No server-side delete and no guessing of multi-site document roots.
"""
import ftplib, os, posixpath, re, ssl
from pathlib import Path

DIST = Path(__file__).resolve().parents[1] / "dist"

def required(key):
    result = os.getenv(key, "").strip()
    if not result:
        raise RuntimeError("Missing GitHub secret/variable: " + key)
    return result

def destination_path(value):
    if not value.startswith("/") or "\\" in value or "//" in value:
        raise RuntimeError("FTP_SERVER_DIR must be an absolute FTP path.")
    segments = [x for x in value.split("/") if x]
    if any(x in (".", "..") for x in segments):
        raise RuntimeError("Unsafe FTP_SERVER_DIR segments.")
    if any(s in value.lower() for s in ("joytun", "orbit-lubricants", "creatifybd")):
        raise RuntimeError("Refusing a directory associated with another company.")
    return "/" + "/".join(segments) if segments else "/"

def remote_guard(ftp):
    names = {posixpath.basename(p.rstrip("/")) for p in ftp.nlst()}
    if "wp-config.php" in names or "wp-content" in names:
        raise RuntimeError("Wrong destination: WordPress detected.")
    if "index.html" in names:
        data = bytearray()
        def collect(chunk):
            if len(data) < 100_000:
                data.extend(chunk[:100_000-len(data)])
        ftp.retrbinary("RETR index.html", collect)
        body = data.decode("utf-8", errors="replace").lower()
        if not (("nazrul" in body and "brothers" in body) or "coming soon" in body):
            raise RuntimeError("Unexpected remote index.html: possible unrelated site.")

def publish(ftp, root, local, run_id):
    relative = local.relative_to(DIST).as_posix()
    folder, name = posixpath.split(relative)
    ftp.cwd(root)
    if folder:
        for part in folder.split("/"):
            try:
                ftp.cwd(part)
            except ftplib.error_perm as exc:
                if not str(exc).startswith("550"):
                    raise
                ftp.mkd(part)
                ftp.cwd(part)
    temporary = name + ".upload-" + run_id
    with local.open("rb") as src:
        ftp.storbinary("STOR " + temporary, src, blocksize=65536)
    try:
        size = ftp.size(temporary)
    except ftplib.error_perm as exc:
        if not str(exc).startswith(("500", "502", "504")):
            raise
        size = None
    if size is not None and size != local.stat().st_size:
        raise RuntimeError("Remote upload-size mismatch: " + relative)
    ftp.rename(temporary, name)
    print("Published", relative)

def main():
    if required("HOSTINGER_FTP_SCOPED") != "true":
        raise RuntimeError("Confirm a dedicated FTP account limited to this site's directory before enabling.")
    host, user, password = required("FTP_SERVER"), required("FTP_USERNAME"), required("FTP_PASSWORD")
    path = destination_path(required("FTP_SERVER_DIR"))
    secure = os.getenv("FTP_SECURE", "true").lower()
    if secure not in ("true", "false"):
        raise RuntimeError("FTP_SECURE must be true or false.")
    if secure == "true":
        ftp = ftplib.FTP_TLS(timeout=45, context=ssl.create_default_context())
    else:
        print("Warning: FTP_SECURE=false transmits FTP credentials without transport encryption.")
        ftp = ftplib.FTP(timeout=45)
    try:
        ftp.connect(host, 21)
        ftp.login(user, password)
        if secure == "true":
            ftp.prot_p()
        ftp.set_pasv(True)
        ftp.cwd(path)  # Must exist. Never invent a fallback.
        root = ftp.pwd()
        print("Publishing only into confirmed destination:", root)
        remote_guard(ftp)
        files = [p for p in DIST.rglob("*") if p.is_file()]
        def order(p):
            name = p.relative_to(DIST).as_posix()
            return (4 if name == "deployment.json" else 3 if name == "index.html" else
                    2 if name.endswith(".html") else 1 if name == ".htaccess" else 0, name)
        files.sort(key=order)
        run_id = re.sub(r"[^a-zA-Z0-9]", "", os.getenv("GITHUB_RUN_ID", "release"))[:16]
        for file in files:
            publish(ftp, root, file, run_id)
        print(f"Uploaded {len(files)} files without remote deletions.")
    finally:
        try:
            ftp.quit()
        except Exception:
            ftp.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        raise SystemExit("Safe deployment stopped: " + str(err)) from None
