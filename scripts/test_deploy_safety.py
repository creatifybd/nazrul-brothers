"""Security regression tests: refused configurations must never open a connection."""
import os
import unittest
from unittest.mock import patch
import deploy_ftp

class DeploymentSafety(unittest.TestCase):
    def test_only_approved_roots(self):
        for value in ('/', '/public_html', deploy_ftp.SITE_ROOT):
            self.assertEqual(deploy_ftp.destination_path(value), value)
        for value in ('/home/u104160495', '/domains', '/other/public_html',
                      '/public_html/../', '/public_html//', 'public_html',
                      '/home/u104160495/domains/joytunchemicals.com/public_html'):
            with self.subTest(path=value), self.assertRaises(RuntimeError):
                deploy_ftp.destination_path(value)

    def test_unsafe_configuration_never_connects(self):
        base = {'HOSTINGER_FTP_SCOPED':'true','HOSTINGER_FTP_PASSWORD_ROTATED':'true',
                'FTP_SERVER':'ftp.coral-oyster-225966.hostingersite.com',
                'FTP_USERNAME':deploy_ftp.EXPECTED_USER,'FTP_PASSWORD':'test-only',
                'FTP_SERVER_DIR':'/','FTP_SECURE':'true'}
        for override in ({'FTP_SECURE':'false'}, {'FTP_USERNAME':'shared-account'},
                         {'HOSTINGER_FTP_PASSWORD_ROTATED':'false'},
                         {'HOSTINGER_FTP_SCOPED':'false'}, {'FTP_SERVER_DIR':'/other'}):
            with self.subTest(override=override), patch.dict(os.environ, base | override, clear=True), \
                 patch('deploy_ftp.ftplib.FTP_TLS') as tls, patch('deploy_ftp.ftplib.FTP') as plain:
                with self.assertRaises(RuntimeError): deploy_ftp.main()
                tls.assert_not_called()
                plain.assert_not_called()

if __name__ == '__main__': unittest.main()
