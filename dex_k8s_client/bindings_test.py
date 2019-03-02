import unittest
from dex_k8s_client.bindings import Dex_K8S_Bindings
from dex_k8s_client.settings_test import make_settings

class Dex_K8S_Bindings_Test(unittest.TestCase):
    """Tests for `bindings.py`."""

    def test_create_bindings(self):
        """ Test creating a new gRPC API bindings object. """
        bindings = Dex_K8S_Bindings(make_settings())
        self.assertIsInstance(bindings, Dex_K8S_Bindings)
