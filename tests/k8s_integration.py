import bcrypt
import unittest
from dex_k8s_client.client_test import make_client

client_params = {
    'id': 'test-client',
    'secret': 'test-client-secret',
    'redirect_uris': ['https://localhost:5556/dex/callback'],
    'trusted_peers': ['localhost'],
    'public': True,
    'name': 'Test Client'
}

password_params = {
    'email': 'person@domain.com',
    'username': 'Test Client',
    'user_id': 'test-client',
    'hash': bcrypt.hashpw(b'password', bcrypt.gensalt(14))
}

class IntegrationTests(unittest.TestCase):
    """
    Run integration tests.
    """

    def test_api_create_client(self):
        """ Test creating a new Dex client via the gRPC API """
        dex = make_client()
        dex.grpc_connect()

        response = dex.create_client(**client_params)
        dex.grpc.disconnect()
        self.assertEqual(response.json, {
            "client": {
                "id": "test-client",
                "secret": "test-client-secret",
                "redirectUris": [
                    "https://localhost:5556/dex/callback",
                ],
                "trustedPeers": [
                    "localhost"
                ],
                "public": True,
                "name": "Test Client"
            }
        })

    def test_authorize_client(self):
        dex = make_client()

        auth_url, state, session = dex.authorize_client('test-client')
        self.assertTrue(auth_url.startswith('https://127.0.0.1:5556/dex/auth'))

    def test_get_client_token(self):
        dex = make_client()

        response = dex.get_token('test-client', 'secret', 'user@domain.com', 'pass')
        self.assertEqual(response, None)

    def test_api_update_client(self):
        """ Test updating the client we just created """
        dex = make_client()
        dex.grpc_connect()

        response = dex.update_client(**{
            'id': 'test-client',
            'name': 'Renamed Test Client',
            'redirect_uris': ['https://localhost:4444']
        })
        dex.grpc.disconnect()
        self.assertEqual(response.json, {})

    def test_api_update_client_notfound(self):
        """ Test attempting to update a non-existant client """
        dex = make_client()
        dex.grpc_connect()

        response = dex.update_client(**{
            'id': 'notreal-client',
            'name': 'Not Real Client',
            'redirect_uris': ['https://localhost:4444']
        })
        dex.grpc.disconnect()
        self.assertEqual(response.json, {'notFound': True})

    def test_api_create_client_already_exists(self):
        """ Test trying to create an already existing client """
        dex = make_client()
        dex.grpc_connect()

        response = dex.create_client(**client_params)
        dex.grpc.disconnect()
        self.assertEqual(response.json, {'alreadyExists': True})

    def test_api_create_password(self):
        """ Test creating a password """
        dex = make_client()
        dex.grpc_connect()

        response = dex.create_password(**password_params)
        dex.grpc.disconnect()
        self.assertEqual(response.json, {})

    def test_api_update_password(self):
        """ Test updating a password """
        dex = make_client()
        dex.grpc_connect()

        response = dex.update_password(**{
            'email': 'person@domain.com',
            'new_hash': bcrypt.hashpw(b'secret', bcrypt.gensalt(14)),
            'new_username': 'New Username'
        })
        dex.grpc.disconnect()
        self.assertEqual(response.json, {})

    def test_api_list_passwords(self):
        """ Test listing passwords """
        dex = make_client()
        dex.grpc_connect()

        response = dex.list_passwords()
        dex.grpc.disconnect()
        self.assertEqual(response.json, {
            'passwords': [
                {
                    'email': 'person@domain.com',
                    'username': 'New Username',
                    'userId': 'test-client'
                }
            ]
        })

    def test_api_delete_password(self):
        """ Testing deleting a password """
        dex = make_client()
        dex.grpc_connect()

        response = dex.delete_password('person@domain.com')
        dex.grpc.disconnect()
        self.assertEqual(response.json, {})

    def test_api_delete_client(self):
        """ Testing deleting a client via the gRPC API """
        dex = make_client()
        dex.grpc_connect()

        response = dex.delete_client('test-client')
        dex.grpc.disconnect()
        self.assertEqual(response.json, {})

    def test_api_delete_client_notfound(self):
        """ Test attempting to delete a non-existant client """
        dex = make_client()
        dex.grpc_connect()

        response = dex.delete_client('not-found')
        dex.grpc.disconnect()
        self.assertEqual(response.json, {'notFound': True})

if __name__ == '__main__':
    unittest.main()
