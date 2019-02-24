from os import getenv
from grpc_api_client.client import gRPC_API_Client

from dex_api_client.settings import Dex_API_Settings
from dex_api_client.bindings import Dex_API_Bindings

DEX_VERSION=getenv('PYTHON_DEX_API_VERSION', '2.14.0')

class Dex_API_Client(object):
    """
    Client class for interacting with a Dex API server.
    """
    def __init__(self, host, port,
        ca_cert=None,
        client_cert=None,
        client_key=None,
        dex_version=DEX_VERSION):

        # Store connection settings
        self.settings = Dex_API_Settings(host, port,
            ca_cert=ca_cert,
            client_cert=client_cert,
            client_key=client_key,
            dex_version=dex_version
        )

        # Create a new bindings instance
        self.bindings = Dex_API_Bindings(self.settings)

        # Create a new gRPC client
        self.grpc = gRPC_API_Client(
            self.bindings.modules.proto,
            self.bindings.modules.grpc
        )

    def connect(self):
        """
        Open the connection to the Dex API server.
        """
        self.grpc.connect(self.settings.host, self.settings.port,
            ca_cert     = self.settings.ca_cert,
            client_cert = self.settings.client_cert,
            client_key  = self.settings.client_key
        )

        # Get the server version
        #print(self.grpc.api.GetVersion())
