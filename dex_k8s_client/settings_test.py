import unittest
from importlib import import_module
from dex_k8s_client.settings import Dex_K8S_Settings
from dex_k8s_client.k8s.cluster import Dex_K8S_Cluster
from dex_k8s_client.k8s.connector import Dex_K8S_Connector

example_client_cert = 'docker_files/dex_tls/client.crt'
example_client_key = 'docker_files/dex_tls/client.key'
example_ca_cert = 'docker_files/dex_tls/ca.crt'

def make_settings():
    """
    Convenience method for generating a test client class.
    """

    cluster = Dex_K8S_Cluster('name', example_ca_cert, 'api_url')
    connector = Dex_K8S_Connector('localhost', '5557', '5556',
        example_client_cert, example_client_key, example_ca_cert, 'issuer_url',
        '2.14.0', oauth2_params={})

    return Dex_K8S_Settings(cluster, connector)

class Dex_K8S_Settings_Test(unittest.TestCase):
    """Tests for `settings.py`."""

    def test_create_client_settings(self):
        """ Test creating a new client settings object. """
        settings = make_settings()
        self.assertIsInstance(settings, Dex_K8S_Settings)
