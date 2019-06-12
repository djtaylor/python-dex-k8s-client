from grpc_api_client.client import gRPC_API_Client

from dex_k8s_client.settings import Dex_K8S_Settings
from dex_k8s_client.bindings import Dex_K8S_Bindings
from dex_k8s_client.oauth2.client import Dex_K8S_OAuth2_Client
from dex_k8s_client.dexidp.dex import DEX_VERSION

class Dex_K8S_Client(object):
    """
    Client class for interacting with a Dex API server.
    """
    def __init__(self, cluster, connector):

        # Store connection settings
        self.settings = Dex_K8S_Settings(cluster, connector)

        # Create a new bindings instance
        self.bindings = Dex_K8S_Bindings(self.settings)

        # Create a new gRPC/OAuth2 client
        self.grpc     = gRPC_API_Client(
            self.bindings.modules.proto,
            self.bindings.modules.grpc
        )
        self.oauth2   = Dex_K8S_OAuth2_Client(self.settings)

    def grpc_connect(self):
        """ Open the connection to the Dex gRPC API server. """
        self.grpc.connect(self.settings.dex.host, self.settings.dex.grpc_port,
            ca_cert     = self.settings.dex.ca_cert,
            client_cert = self.settings.dex.client_cert,
            client_key  = self.settings.dex.client_key
        )

    def grpc_disconnect(self):
        """ Close connection to gRPC server """
        self.grpc.disconnect()

    def server_version(self):
        """
        Return the Dex server version for the client to inspect.
        """
        return self.grpc.api.GetVersion()

    def get_kubeconfig(self, client_id, client_secret, user_email, user_password):
        """
        Get the kubeconfig for a particular cluster for a user.
        """
        return self.oauth2.get_kubeconfig(
            client_id, client_secret, user_email, user_password)

    def get_token(self, client_id, client_secret, user_email, user_password):
        """
        Get a OAuth2 token for a user.
        """
        return self.oauth2.get_token(
            client_id, client_secret, user_email, user_password)

    def authorize_client(self, client_id):
        """
        Make an authorization request on behalf of a client.
        """
        return self.oauth2._authorize(client_id)

    def delete_client(self, client_id):
        """
        Delete an existing client.
        """
        return self.grpc.api.DeleteClient(id=client_id)

    def create_client(self, **kwargs):
        """
        Create a new client.
        """
        return self.grpc.api.CreateClient(client={
            'id': kwargs.get('id'),
            'secret': kwargs.get('secret'),
            'redirect_uris': kwargs.get('redirect_uris'),
            'trusted_peers': kwargs.get('trusted_peers'),
            'public': kwargs.get('public'),
            'name': kwargs.get('name'),
            'logo_url': kwargs.get('logo_url', None)
        })

    def update_client(self, **kwargs):
        """
        Update an existing client.
        """
        return self.grpc.api.UpdateClient(**kwargs)

    def create_password(self, **kwargs):
        """
        Create a new password.
        """
        return self.grpc.api.CreatePassword(password=kwargs)

    def delete_password(self, email):
        """
        Delete a password.
        """
        return self.grpc.api.DeletePassword(email=email)

    def update_password(self, **kwargs):
        """
        Update an existing password.
        """
        return self.grpc.api.UpdatePassword(**kwargs)

    def list_passwords(self):
        """
        Return a list of passwords.
        """
        return self.grpc.api.ListPasswords()

    def list_refresh(self, client_id, client_secret, user_email, user_password):
        """
        List refresh tokens for a user.
        """

        # Get the user's token first
        user_token = self.get_token(
            client_id, client_secret, user_email, user_password)

        return self.grpc.api.ListRefresh(user_id=user_token.decode()['sub'])

    def revoke_refresh(self, client_id, client_secret, user_email, user_password):
        """
        Revoke a refresh token for a user.
        """

        # Get the user's token first
        user_token = self.get_token(
            client_id, client_secret, user_email, user_password)

        return self.grpc.api.RevokeRefresh(user_id=user_token.decode()['sub'], client_id=client_id)
