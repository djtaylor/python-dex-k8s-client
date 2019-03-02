from passlib.hash import bcrypt

"""
Define test fields for making requests to the Dex server
during test runs. These fields should map to what is defined
in the proto definition for this API version.
"""

CreateClient = {
    'client': {
        'id': 'testclient',
        'secret': 'testsecret',
        'redirect_uris': ['http://one.com', 'http://two.com'],
        'trusted_peers': ['localhost', '127.0.0.1'],
        'public': True,
        'name': 'Test Client',
        'logo_url': ''
    }
}

DeleteClient = {
    'id': 'testclient'
}

UpdateClient = {
    'id': 'testclient',
    'redirect_uris': ['http://three.com', 'http://four.com'],
    'trusted_peers': ['updatedpeer1', 'updatedpeer2'],
    'name': 'Test Client 2',
}


CreatePassword = {
    'password': {
        'email': 'user@domain.com',
        'hash': bcrypt.hash("password").encode(),
        'username': 'Test Client 2',
        'user_id': 'testclient'
    }
}

UpdatePassword = {
    'email': 'user@domain.com',
    'new_hash': bcrypt.hash("password").encode(),
    'new_username': 'Test Client 2'
}

DeletePassword = {
    'email': 'user@domain.com'
}

ListPasswords = {}
GetVersion = {}

ListRefresh = {
    'user_id': 'testclient'
}

RevokeRefresh = {
    'user_id': 'testclient',
    'client_id': 'testclient'
}
