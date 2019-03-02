import unittest
from base64 import b64encode
from dex_k8s_client.k8s.kubeconfig import Dex_K8S_KubeConfig

class Dex_K8S_KubeConfig_Test(unittest.TestCase):
    """Tests for `k8s/kubeconfig.py`."""

    def test_create_kubeconfig_from_template(self):
        """ Test creating a new kubeconfig from template string """
        kubeconfig = Dex_K8S_KubeConfig.from_template(**{
            'cluster_name': 'cluster_name',
            'cluster_ca': b64encode(b'cluster_ca').decode(),
            'client_id': 'client_id',
            'client_secret': 'client_secret',
            'email': 'user_email',
            'api_url': 'api_url',
            'issuer_url': 'issuer_url',
            'refresh_token': 'refresh_token',
            'id_token': 'id_token'
        })

        self.assertIsInstance(kubeconfig, dict)
