import unittest
from unittest import mock
from dex_k8s_client.settings_test import make_settings
from dex_k8s_client.oauth2.client import Dex_K8S_OAuth2_Client
from dex_k8s_client.client_test import make_client

example_token = {
    'access_token': 'bkhafadfvHJDAF',
    'token_type': 'bearer',
    'expires_in': 57248,
    'refresh_token': 'fgadw48ay5nkctnzksgnkzsd',
    'id_token': 'kycrkawgnctjsgtbkszc',
    'expires_at': 1551648182.857075
}

example_state = 'QTxEd0QoMKgIieANLl67i7iaSkjxw0'
example_auth_url = ''.join([
    'https://localhost:5556/auth?response_type=code&client_id=client',
    '&redirect_uri=https%3A%2F%2Flocalhost%3A5556%2Fcallback',
    '&scope=openid+groups+profile+email+offline_access',
    '&state={}&access_type=offline'.format(example_state),
    '&prompt=select_account',
])

example_callback_url = ''.join([
    '<a href="https://kubernetes:5556/callback?code=irgenlidu73igudeuobi3pd4d&',
    'amp;state=TpKCxqYwepp9tFzHjmqb40caATmE9C">See Other</a>.'
])

example_approval_location = '/approval?req=jgpebqvb6qv4tidmezzayckrt'
example_approval_url = 'https://localhost:5556{}'.format(example_approval_location)
example_login_url = 'https://localhost:5556/auth/ldap?req=jgpebqvb6qv4tidmezzayckrt'
example_auth_response_html = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <title>dex</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://localhost:5556/static/main.css" rel="stylesheet">
    <link href="https://localhost:5556/theme/styles.css" rel="stylesheet">
    <link rel="icon" href="https://localhost:5556/theme/favicon.png">
  </head>

  <body class="theme-body">
    <div class="theme-navbar">
      <div class="theme-navbar__logo-wrap">
        <img class="theme-navbar__logo" src="https://localhost:5556/theme/logo.png">
      </div>
    </div>

    <div class="dex-container">



<div class="theme-panel">
  <h2 class="theme-heading">Log in to dex </h2>
  <div>

      <div class="theme-form-row">
        <a href="/auth/local?req=jgpebqvb6qv4tidmezzayckrt" target="_self">
          <button class="dex-btn theme-btn-provider">
            <span class="dex-btn-icon dex-btn-icon--local"></span>
            <span class="dex-btn-text">Log in with Email</span>
          </button>
        </a>
      </div>

      <div class="theme-form-row">
        <a href="/auth/ldap?req=jgpebqvb6qv4tidmezzayckrt" target="_self">
          <button class="dex-btn theme-btn-provider">
            <span class="dex-btn-icon dex-btn-icon--ldap"></span>
            <span class="dex-btn-text">Log in with OpenLDAP</span>
          </button>
        </a>
      </div>

  </div>
</div>

    </div>
  </body>
</html>
"""

class Mock_OAuth2Session(object):
    """
    Mock OAuth2 session for testing.
    """
    class HTTP_Response(object):
        def __init__(self, status_code, text, headers={}):
            self.status_code = status_code
            self.text = text
            self.headers = headers

    def __init__(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        return True

    def fetch_token(self, *args, **kwargs):
        return example_token

    def authorization_url(self, *args, **kwargs):
        return example_auth_url, example_state

    def post(self, *args, **kwargs):

        if args[0] == example_login_url:
            return Mock_OAuth2Session.HTTP_Response(303, example_callback_url,
                headers={
                    'Location': example_approval_location,
                    'Date': 'Sat, 02 Mar 2019 21:46:07 GMT',
                    'Content-Length': '0'
                })

    def get(self, *args, **kwargs):

        if args[0] == example_auth_url:
            return Mock_OAuth2Session.HTTP_Response(200, example_auth_response_html)

        if args[0] == example_approval_url:
            return Mock_OAuth2Session.HTTP_Response(200, example_callback_url)


class Dex_K8S_OAuth2_Client_Test(unittest.TestCase):
    """Tests for `oauth2/client.py`."""

    def test_class_instance(self):
        """ Test creating a new instance of Dex_K8S_OAuth2_Client. """
        oauth2_client = Dex_K8S_OAuth2_Client(make_settings())
        self.assertIsInstance(oauth2_client, Dex_K8S_OAuth2_Client)

    @mock.patch('dex_k8s_client.oauth2.client.OAuth2Session', new=Mock_OAuth2Session)
    def test_get_token(self, *args, **kwargs):
        """ Test getting an OAuth2 token. """
        client = make_client()
        token = client.get_token('test', 'test', 'test@test.com', 'test')
        self.assertEqual(token, example_token)

    @mock.patch('dex_k8s_client.oauth2.client.OAuth2Session', new=Mock_OAuth2Session)
    def test_get_kubeconfig(self, *args, **kwargs):
        """ Test getting an OAuth2 token. """
        client = make_client()
        kubeconfig = client.get_kubeconfig('test', 'test', 'test@test.com', 'test')
