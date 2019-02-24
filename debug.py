import json
from jwt import JWT
from passlib.hash import bcrypt
from dex_api_client.client_test import make_client

client = make_client()

client.connect()

for method in client.grpc.api:
    method_name = method[0]
    method_obj  = method[1]
    print('Method: {}'.format(method_name))
    print(' Object: {}'.format(method_obj))
    print(' InputClass:')
    print(' > Type: {}'.format(method_obj.input.type))
    print(' > Handler: {}'.format(method_obj.input.handler))
    print(' InputFields: {}'.format(method_obj.input_fields()))
    print(' OutputClass: {}'.format(method_obj.output))
    print(' > Type: {}'.format(method_obj.output.type))
    print(' > Handler: {}'.format(method_obj.output.handler))
    print(' Stub: {}'.format(method_obj.stub))

# Parameters for a new client in 2.14.0, see: `Message Client` in protocol buffer definition
new_client_params = {
  'id': '1',
  'secret': 'mysecret',
  'redirect_uris': ['https://127.0.0.1', 'https://localhost'],
  'trusted_peers': ['host1.mydomain.com', 'host2.mydomain.com'],
  'public': False,
  'name': 'Bob',
  'logo_url': 'https://host1.domain.com/favicon.ico'
}

print('> CreateClient')
response = client.grpc.api.CreateClient(client=new_client_params)

print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> CreateClient: AlreadyExists')
response = client.grpc.api.CreateClient(client=new_client_params)

print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> UpdateClient')
response = client.grpc.api.UpdateClient(
    id='1',
    redirect_uris=['https://192.168.0.1', 'https://192.168.0.2'],
    trusted_peers=['host3.mydomain.com', 'host4.mydomain.com'],
    name='newclientname',
    logo_url='https://host3.domain.com/favicon.ico'
)

print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> UpdateClient: NotFound')
response = client.grpc.api.UpdateClient(
    id='2',
    redirect_uris=['https://192.168.0.1', 'https://192.168.0.2'],
    trusted_peers=['host3.mydomain.com', 'host4.mydomain.com'],
    name='newclientname',
    logo_url='https://host3.domain.com/favicon.ico'
)

print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> DeleteClient')
response = client.grpc.api.DeleteClient(id='1')

print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> DeleteClient: NotFound')
response = client.grpc.api.DeleteClient(id='1')

print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> CreatePassword')
response = client.grpc.api.CreatePassword(password={
    'email': 'user@domain.com',
    'hash': bcrypt.hash("password").encode(),
    'username': 'Test User',
    'user_id': 'testuser'
})
print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> UpdatePassword')
response = client.grpc.api.UpdatePassword(
    email='user@domain.com',
    new_hash=bcrypt.hash("password").encode(),
    new_username='Test User'
)
print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> ListPasswords')
response = client.grpc.api.ListPasswords()
print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))
passwords = json.loads(response.json)['passwords']

print('> ListRefresh')
response = client.grpc.api.ListRefresh()
print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

#for password in passwords:
#    user_id = password['userId']
#
#    jwt = JWT()
#    compact_jws = jwt.encode(user_id, 'mykey', 'RS256')
#
#    print('> ListRefresh: {0}'.format(user_id))
#    response = client.grpc.api.ListRefresh(user_id=compact_jws)
#    print('ResponseJSON: {}'.format(json.dumps(response.json)))
#    print('ResponseRaw: {}'.format(response.protobuf))

print('> DeletePassword')
response = client.grpc.api.DeletePassword(email='user@domain.com')
print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

print('> GetVersion')
response = client.grpc.api.GetVersion()
print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.protobuf))

client.grpc.disconnect()
