[![Build Status](https://api.travis-ci.org/djtaylor/python-dex-api-client.png)](https://api.travis-ci.org/djtaylor/python-dex-api-client)

# Dex API Client
This module is designed to interact with a [Dex](https://github.com/dexidp/dex) server via gRPC API. This was inspired by a need to interact with [Dex running on Kubernetes](https://github.com/helm/charts/tree/master/stable/dex), and as such, initial functionality is targeted at that type of architecture.

# Dex Versions
This module comes with precompiled protocol buffer bindings for targeted Dex API versions. As of the creation of this repository, the latest version is `2.14.0`. See the [protocol file](proto/dex_api_client/dexidp/dex/api/v2_14_0.proto) for available API methods.

# Installation
To install the module with the precompiled protocol buffer bindings:

```sh
python3 setup.py install
```

# Basic Usage
The following shows some basic examples of interacting with a Dex API server. Request methods and parameters are generated automatically. To understand how to construct a request, please refer to the protocul buffer file for whichever version of Dex you are interacting with.

```python3
import json
from dex_api_client.client import Dex_API_Client

dex_args = ['127.0.0.1', '5557']
dex_kwargs = {
  'ca_cert': '/my/ca.crt',
  'client_cert': '/my/client.crt',
  'client_key': '/my/client.key'
}

# Make a new client for the latest compiled version of Dex (2.14.0)
client_latest = Dex_API_Client(*dex_args, **dex_kwargs)
print('API Version: {}'.format(client_latest.bindings.version))

# Show available methods
for method in client_latest.grpc.api:
  method_name = method[0]
  method_obj  = method[1]
  print('Method: {}, {}'.format(method_name, method_obj))

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

response = client_latest.grpc.api.CreateClient(client=new_client_params)

print('ResponseJSON: {}'.format(json.dumps(response.json)))
print('ResponseRaw: {}'.format(response.proto))

# Make a new client for a different version of Dex
dex_kwargs['dex_version'] = '2.13.0'
client_2_13_0 = Dex_API_Client(*dex_args, **dex_kwargs)

print('API Version: {}'.format(client_2_13_0.bindings.version))

# Close the connections
client_latest.grpc.close()
client_2_13_0.grpc.close()

```
