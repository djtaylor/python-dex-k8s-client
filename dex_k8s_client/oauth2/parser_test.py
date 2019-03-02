import unittest
from dex_k8s_client.oauth2.parser import Dex_K8S_OAuth2_Parser as parser
from dex_k8s_client.settings_test import make_settings
from dex_k8s_client.oauth2.client_test import example_auth_response_html, \
    example_login_url

class Dex_K8S_OAuth2_Parser_Test(unittest.TestCase):
    """Tests for `oauth2/parser.py`."""

    def test_parse_ldap_auth_uri(self):
        """ Test parsing LDAP URI from auth page """
        auth_uri = parser.get_ldap_authentication_uri(example_auth_response_html, make_settings())
        self.assertEqual(auth_uri, example_login_url)
