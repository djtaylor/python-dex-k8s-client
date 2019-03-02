import unittest
from importlib import import_module
from parameterized import parameterized
from grpc_api_client.client import gRPC_API_Client
from dex_k8s_client.client import Dex_K8S_Client
from dex_k8s_client.settings_test import make_settings

def make_fields(method):
    """
    Generate test fields for a Dex gRPC method.
    """
    settings = make_settings()
    test_fields = import_module('dex_k8s_client.dexidp.dex.api.v{0}_pb2_test_fields'.format(
        settings.dex.version.replace('.', '_')
    ))
    return getattr(test_fields, method.name)

def make_client(connect=True):
    """
    Convenience method for generating a test client class.
    """
    settings = make_settings()
    client_object = Dex_K8S_Client(settings.cluster, settings.dex)
    if connect:
        client_object.grpc_connect()
    return client_object

def generate_grpc_methods():
    """
    Generate an argument to pass to parameterized gRPC method tests
    """

    # Generate a mock client
    client = make_client()

    # Get all API methods and return a list of names
    method_tests = []
    for name, method in client.grpc.api:
        method_tests.append([name, method])
    return method_tests

class Dex_K8S_Client_Test(unittest.TestCase):
    """Tests for `client.py`."""

    def test_create_client(self):
        """ Test creating a new client interface. """
        client = make_client()
        self.assertIsInstance(client, Dex_K8S_Client)

    def test_client_connect(self):
        """ Test creating a new client interface and connecting. """
        client = make_client()
        client.grpc_connect()
        self.assertIsInstance(client.grpc, gRPC_API_Client)

    @parameterized.expand(generate_grpc_methods())
    def test_grpc_method(self, name, method):
        client = make_client()
        output_class = getattr(client.grpc.api, name).output.handler
        response = getattr(client.grpc.api, name)(**make_fields(method))
        self.assertIsInstance(response.protobuf, output_class)
