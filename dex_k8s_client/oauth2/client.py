import re
from base64 import b64encode
from requests_oauthlib import OAuth2Session
from dex_k8s_client.oauth2.parser import Dex_K8S_OAuth2_Parser
from dex_k8s_client.k8s.kubeconfig import Dex_K8S_KubeConfig
from dex_k8s_client.oauth2.token import Dex_K8S_OAuth2_Token

class Dex_K8S_OAuth2_Client(object):
    """
    Client for making requests to Dex OAuth2 authorization URLs.
    """
    def __init__(self, settings):
        self.settings = settings

        # HTML parser
        self.parser = Dex_K8S_OAuth2_Parser

        # SSL verification
        self.verify_ssl = getattr(self.settings.dex, 'ca_cert', True)

    def _session(self, client_id):
        """
        Initiate an OAuth2 session, get an auth_url and state.
        """
        session = OAuth2Session(client_id,
            redirect_uri=self.settings.dex.oauth2.redirect_uri,
            scope=self.settings.dex.oauth2.scope)

        # Get an authorization URL and state
        auth_url, state = session.authorization_url(self.settings.dex.auth_url,
            access_type=self.settings.dex.oauth2.access_type,
            prompt=self.settings.dex.oauth2.prompt)
        return auth_url, state, session

    def _authorize(self, client_id):
        """
        Make an authorization request.
        """
        return self._session(client_id)

    def _get_ldap_authentication_uri(self, auth_url, session):
        """
        Get the URL for making POST authentication requests.
        """
        response = session.get(auth_url, verify=self.verify_ssl)

        if not response.status_code == 200:
            raise Exception('Failed to get authentication URL: auth_url="{}", http_error="{}"'.format(
                auth_url, response.text
            ))

        # Get the URL for making POST requests for LDAP auth
        return self.parser.get_ldap_authentication_uri(
            response.text, self.settings)

    def _login(self, ldap_uri, user_email, user_password, session):
        """
        Login a user.
        """

        response = session.post(ldap_uri, data={
            'login': user_email,
            'password': user_password
        }, verify=self.verify_ssl, allow_redirects=False)

        if not response.status_code == 303:
            raise Exception('Failed to login: {}'.format(response.text))

        # Get the auth code from the approval endpoint
        approval_endpoint = '{}{}'.format(self.settings.dex.base_url, response.headers['Location'])
        response = session.get(approval_endpoint, allow_redirects=False, verify=self.verify_ssl)

        return re.search(r"[/]callback[?]code=(\w+)", response.text).group(1)

    def get_token(self, client_id, client_secret, user_email, user_password):
        """
        Get an OAuth2 token for a particular client/user.
        """
        auth_url, state, session = self._authorize(client_id)

        # Get the URL for making POST requests for the LDAP connector
        ldap_uri = self._get_ldap_authentication_uri(auth_url, session)

        # Log the user in and get an auth_code
        auth_code = self._login(
            ldap_uri, user_email, user_password, session)

        # Get and return the token
        token = session.fetch_token(self.settings.dex.token_url,
                                    code=auth_code,
                                    client_secret=client_secret,
                                    verify=self.verify_ssl)

        return Dex_K8S_OAuth2_Token(token, client_id, session, self.settings)

    def get_kubeconfig(self, client_id, client_secret, user_email, user_password):
        """
        Retrieve a user's kubectl config file.
        """
        token = self.get_token(client_id, client_secret, user_email, user_password).json()

        # CA certificate
        cluster_ca = None
        with open(self.settings.cluster.ca_cert, 'rb') as f:
            cluster_ca = f.read()

        return Dex_K8S_KubeConfig.from_template(**{
            'cluster_name': self.settings.cluster.name,
            'cluster_ca': b64encode(cluster_ca).decode(),
            'client_id': client_id,
            'client_secret': client_secret,
            'email': user_email,
            'api_url': self.settings.cluster.api_url,
            'issuer_url': self.settings.dex.issuer_url,
            'refresh_token': token['refresh_token'],
            'id_token': token['id_token']
        })
