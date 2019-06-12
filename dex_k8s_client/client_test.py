import unittest
from unittest import mock
from importlib import import_module
from parameterized import parameterized
from grpc_api_client.client import gRPC_API_Client
from grpc_api_client.grpc.api import gRPC_API_Path, gRPC_API_Response
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

def make_client(connect_grpc=True):
    """
    Convenience method for generating a test client class.
    """
    settings = make_settings()
    client_object = Dex_K8S_Client(settings.cluster, settings.dex)
    if connect_grpc:
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

class Mock_gRPC_API_Path(gRPC_API_Path):
    """
    Class for mocking a gRPC API path.
    """
    def __call__(self, **kwargs):
        import dex_k8s_client.dexidp.dex.api.v2_14_0_pb2 as dex_pb2

        response = {
            'CreateClient': dex_pb2.CreateClientResp(),
            'UpdateClient': dex_pb2.UpdateClientResp(),
            'DeleteClient': dex_pb2.CreateClientResp(),
            'CreatePassword': dex_pb2.CreatePasswordResp(),
            'UpdatePassword': dex_pb2.UpdatePasswordResp(),
            'DeletePassword': dex_pb2.DeletePasswordResp(),
            'GetVersion': dex_pb2.VersionResp(),
            'ListRefresh': dex_pb2.ListRefreshResp(),
            'RevokeRefresh': dex_pb2.RevokeRefreshResp(),
            'ListPasswords': dex_pb2.ListPasswordResp()
        }.get(self.name)

        return gRPC_API_Response(response, self.output.handler, self.input_fields())

@mock.patch('grpc_api_client.grpc.api.gRPC_API_Path', new=Mock_gRPC_API_Path)
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
