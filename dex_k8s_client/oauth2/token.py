import jwt
import json

class Dex_K8S_OAuth2_Token(object):
    """
    Class for managing tokens retrieved from Dex.
    """
    def __init__(self, token, client_id, session, settings):
        self._token     = token
        self._client_id = client_id
        self._session   = session
        self._settings  = settings
        self._verify    = getattr(settings, 'ca_cert', True)

    def _get_jwt_pubkey(self):
        """
        Get the JWT public key from the server.
        """
        pubkey_response = self._session.get(self._settings.dex.keys_url, verify=self._verify)
        pubkey_json = pubkey_response.json()['keys'][0]

        return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(pubkey_json))

    def decode(self):
        """
        Decode the `id_token` key of an OAuth2 token.
        """
        pubkey = self._get_jwt_pubkey()

        # Decode it
        return jwt.decode(self._token['id_token'], pubkey, audience=self._client_id, algorithm='RS256')

    def json(self):
        """
        Return the JSON object for the full token.
        """
        return self._token
