import unittest
from importlib import import_module
from dex_api_client.settings import Dex_API_Settings

def make_settings():
    """
    Convenience method for generating a test client class.
    """
    return Dex_API_Settings(*['127.0.0.1', '35556'], **{
        'ca_cert': 'docker_files/grpc_tls/ca.crt',
        'client_cert': 'docker_files/grpc_tls/client.crt',
        'client_key': 'docker_files/grpc_tls/client.key',
        'dex_version': '2.14.0'
    })

class Dex_API_Settings_Test(unittest.TestCase):
    """Tests for `settings.py`."""

    def test_create_client_settings(self):
        """ Test creating a new client settings object. """
        settings = make_settings()
        self.assertIsInstance(settings, Dex_API_Settings)
