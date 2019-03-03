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

test_client_id = 'auth-app'
test_client_secret = 'ZXhhbXBsZS1hcHAtc2VjcmV0'

test_user_email = 'janedoe@example.org'
test_user_password = 'foo'

test_http_args = [
    test_client_id,
    test_client_secret,
    test_user_email,
    test_user_password
]

tester = unittest.TestCase('__init__')

def test_http_authorize_client():
    """ Test getting an OAuth2 authorization URL via HTTP """
    dex = make_client(connect_grpc=False)

    auth_url, state, session = dex.authorize_client(test_client_id)
    print(auth_url)
    tester.assertTrue(auth_url.startswith('https://localhost:5556/auth'))

def test_http_client_token():
    """ Test getting OAuth2 token via HTTP """
    dex = make_client(connect_grpc=False)

    response = dex.get_token(*test_http_args)
    tester.assertIsInstance(response, dict)

def test_grpc_create_client():
    """ Test creating a new Dex client via the gRPC API """
    dex = make_client()

    response = dex.create_client(**client_params)
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {
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

def test_grpc_update_client():
    """ Test updating the client we just created """
    dex = make_client()

    response = dex.update_client(**{
        'id': 'test-client',
        'name': 'Renamed Test Client',
        'redirect_uris': ['https://localhost:4444']
    })
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {})

def test_grpc_update_client_notfound():
    """ Test attempting to update a non-existant client """
    dex = make_client()

    response = dex.update_client(**{
        'id': 'notreal-client',
        'name': 'Not Real Client',
        'redirect_uris': ['https://localhost:4444']
    })
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {'notFound': True})

def test_grpc_create_client_already_exists():
    """ Test trying to create an already existing client """
    dex = make_client()

    response = dex.create_client(**client_params)
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {'alreadyExists': True})

def test_grpc_create_password():
    """ Test creating a password """
    dex = make_client()

    response = dex.create_password(**password_params)
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {})

def test_grpc_update_password():
    """ Test updating a password """
    dex = make_client()

    response = dex.update_password(**{
        'email': 'person@domain.com',
        'new_hash': bcrypt.hashpw(b'secret', bcrypt.gensalt(14)),
        'new_username': 'New Username'
    })
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {})

def test_grpc_list_passwords():
    """ Test listing passwords """
    dex = make_client()

    response = dex.list_passwords()
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {
        'passwords': [
            {
                'email': 'person@domain.com',
                'username': 'New Username',
                'userId': 'test-client'
            }
        ]
    })

def test_grpc_delete_password():
    """ Testing deleting a password """
    dex = make_client()

    response = dex.delete_password('person@domain.com')
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {})

def test_grpc_delete_client():
    """ Testing deleting a client via the gRPC API """
    dex = make_client()

    response = dex.delete_client('test-client')
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {})

def test_grpc_delete_client_notfound():
    """ Test attempting to delete a non-existant client """
    dex = make_client()

    response = dex.delete_client('not-found')
    dex.grpc_disconnect()
    tester.assertEqual(response.json, {'notFound': True})