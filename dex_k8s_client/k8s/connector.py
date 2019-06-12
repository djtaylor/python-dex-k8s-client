from dex_k8s_client.dexidp.dex import DEX_VERSION

class _Dex_K8S_OAuth2_Settings(object):
    """
    Store parameters for making OAuth2 requests.
    """
    def __init__(self, redirect_uri, response_type, scope, access_type, prompt):

        self.redirect_uri = redirect_uri
        self.response_type = response_type
        self.scope = scope
        self.access_type = access_type
        self.prompt = prompt

class Dex_K8S_Connector(object):
    """
    Class object for storing connection attributes for an instance
    of Dex running on Kubernetes.
    """
    def __init__(self, host, grpc_port, https_port, client_cert, client_key,
        ca_cert, issuer_url, version=DEX_VERSION, oauth2_params={}):

        self.base_url = 'https://{}:{}'.format(host, https_port)

        # Dex parameters
        self.host = host
        self.grpc_port = grpc_port
        self.https_port = https_port
        self.client_cert = client_cert
        self.client_key = client_key
        self.ca_cert = ca_cert
        self.issuer_url = issuer_url
        self.version = version
        self.auth_url = '{}/auth'.format(self.base_url)
        self.token_url = '{}/token'.format(self.base_url)
        self.keys_url = '{}/keys'.format(self.base_url)


        # Set the redirect URI
        redirect_uri = oauth2_params.get('redirect_uri', \
            'https://{0}:{1}/callback'.format(self.host, self.https_port))

        # OAuth2 parameters
        self.oauth2 = _Dex_K8S_OAuth2_Settings(
            redirect_uri=redirect_uri,
            response_type=oauth2_params.get('response_type', 'code'),
            scope=oauth2_params.get('scope', 'openid groups profile email offline_access'),
            access_type=oauth2_params.get('access_type', 'offline'),
            prompt=oauth2_params.get('prompt', 'select_account')
        )
