#!/usr/bin/env python3
"""Read-only FTP path check. No upload, delete, or site modification."""
import ftplib
import os
import ssl
import socket
import ipaddress
import socket

def required(name):
    value=os.getenv(name,"").strip()
    if not value:
        raise RuntimeError(f"Missing GitHub secret: {name}")
    return value

def run():
    host=required("FTP_SERVER")
    username=required("FTP_USERNAME")
    password=required("FTP_PASSWORD")
    secure=os.getenv("FTP_SECURE","true").lower()
    # Hostinger's Plan Details screenshot identifies the server as 'server1221'.
    # The FTPS certificate issued by the endpoint is valid for *.hstgr.io.
    # Do not send credentials unless that name resolves to the SAME verified FTP IP.
    if secure == "true":
        verified_ip="195.35.15.205"
        verified_name="server1221.hstgr.io"
        if host == verified_ip:
            addresses={item[4][0] for item in socket.getaddrinfo(verified_name, 21, type=socket.SOCK_STREAM)}
            print("Checked Hostinger server hostname", verified_name, "resolves to", sorted(addresses))
            if verified_ip not in addresses:
                raise RuntimeError("Verified server hostname does not resolve to the FTP IP shown in Hostinger; stop before login.")
            host=verified_name
        elif host != verified_name:
            raise RuntimeError("FTP_SERVER must be the verified IP or server1221.hstgr.io; stop before login.")
        else:
            addresses={item[4][0] for item in socket.getaddrinfo(host, 21, type=socket.SOCK_STREAM)}
            if verified_ip not in addresses:
                raise RuntimeError("FTPS hostname does not match the expected Hostinger FTP IP; stop before login.")
    if secure not in ("true","false"):
        raise RuntimeError("FTP_SECURE must be 'true' or 'false'")
    if secure=="true":
        try:
            ipaddress.ip_address(host)
        except ValueError:
            resolved={x[4][0] for x in socket.getaddrinfo(host, 21, type=socket.SOCK_STREAM)}
            if "195.35.15.205" not in resolved:
                raise RuntimeError("FTP_SERVER hostname does not resolve to the expected Hostinger FTP server IP (195.35.15.205). Check Hosting Plan Details.")
        else:
            raise RuntimeError("Hostinger FTPS certificate covers *.hstgr.io, not the IP address. Use the exact Server Name shown in Hosting Plan Details as FTP_SERVER.")
    ftp=ftplib.FTP_TLS(timeout=30,context=ssl.create_default_context()) if secure=="true" else ftplib.FTP(timeout=30)
    try:
        ftp.connect(host,21)
        ftp.login(username,password)
        if secure=="true":
            ftp.prot_p()
        ftp.set_pasv(True)
        pwd=ftp.pwd()
        print(f"FTP login succeeded. Reported initial working directory: {pwd}")
        # Probe paths without listing unrelated hosted websites.
        for candidate in ["/public_html","/"]:
            try:
                ftp.cwd(candidate)
                current=ftp.pwd()
                try:
                    names={x.rsplit("/",1)[-1].rstrip("/") for x in ftp.nlst()}
                except ftplib.all_errors:
                    names=set()
                print(f"Available candidate {candidate}: actual PWD {current}. Contains index.html: {'index.html' in names}, default.php: {'default.php' in names}, public_html subfolder: {'public_html' in names}")
            except ftplib.all_errors:
                print(f"Unavailable candidate {candidate}")
        print("This is READ-ONLY. Verify the account is limited to Nazrul & Brothers before enabling deployment.")
    finally:
        try:ftp.quit()
        except Exception:ftp.close()

if __name__=="__main__":
    try:run()
    except Exception as ex:
        raise SystemExit("FTP check failed: "+str(ex)) from None
