import unittest
from dex_k8s_client.k8s.connector import Dex_K8S_Connector

class Dex_K8S_Connector_Test(unittest.TestCase):
    """Tests for `k8s/connector.py`."""

    def test_create_connector_instance(self):
        """ Test creating a new Dex_K8S_Connector instance """
        connector = Dex_K8S_Connector('host', 'grpc_port', 'https_port',
            'client_cert', 'client_key', 'ca_cert', 'issuer_url',
            'version', oauth2_params={})

        self.assertIsInstance(connector, Dex_K8S_Connector)
