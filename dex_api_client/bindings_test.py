import unittest
from dex_api_client.bindings import Dex_API_Bindings
from dex_api_client.settings_test import make_settings

class Dex_API_Bindings_Test(unittest.TestCase):
    """Tests for `bindings.py`."""

    def test_create_bindings(self):
        """ Test creating a new API bindings object. """
        bindings = Dex_API_Bindings(make_settings())
        self.assertIsInstance(bindings, Dex_API_Bindings)
