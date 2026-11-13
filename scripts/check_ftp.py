#!/usr/bin/env python3
"""Read-only FTP path check. No upload, delete, or site modification."""
import ftplib
import os
import ssl

def required(name):
    value=os.getenv(name,"").strip()
    if not value:
        raise RuntimeError(f"Missing GitHub secret: {name}")
    return value

def run():
    if required("HOSTINGER_FTP_PASSWORD_ROTATED") != "true":
        raise RuntimeError("Rotate the exposed password and update GitHub before authenticating.")
    host=required("FTP_SERVER")
    username=required("FTP_USERNAME")
    password=required("FTP_PASSWORD")
    if host != "ftp.coral-oyster-225966.hostingersite.com":
        raise RuntimeError("FTP_SERVER does not match the configured Nazrul hostname.")
    if username != "u104160495.nazruldeploy":
        raise RuntimeError("FTP_USERNAME does not match the dedicated Nazrul account.")
    ftp = ftplib.FTP_TLS(timeout=20, context=ssl.create_default_context())
    try:
        ftp.connect(host,21)
        ftp.auth()
        print("FTPS certificate and hostname verified.")
        ftp.login(username, password)
        ftp.prot_p()
        ftp.set_pasv(True)
        pwd=ftp.pwd()
        print(f"FTP login succeeded. Reported initial working directory: {pwd}")
        for candidate in (
            "/home/u104160495/domains/coral-oyster-225966.hostingersite.com/public_html",
            "/public_html",
            "/",
        ):
            try:
                ftp.cwd(candidate)
                print(f"Accessible candidate {candidate}: PWD {ftp.pwd()}")
            except ftplib.error_perm:
                print(f"Unavailable candidate {candidate}")
    finally:
        try:ftp.quit()
        except Exception:ftp.close()

if __name__=="__main__":
    try:run()
    except Exception as ex:
        raise SystemExit("FTP check failed: "+str(ex)) from None
