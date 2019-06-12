[![Build Status](https://api.travis-ci.org/djtaylor/python-dex-k8s-client.png)](https://api.travis-ci.org/djtaylor/python-dex-k8s-client)

# Dex K8S Client
This module is designed to interact with a [Dex](https://github.com/dexidp/dex) server running on Kubernetes using both gRPC and HTTP calls to handle user authorization and authentication programmatically.

# Dex Versions
This module comes with precompiled protocol buffer bindings for targeted Dex gRPC API versions. As of the creation of this repository, the latest version is `2.14.0`. See the [protocol file](proto/dex_api_client/dexidp/dex/api/v2_14_0.proto) for available API methods.

# Basic Usage
The following shows same basic use cases for this module:

```python3
import json
from io import BytesIO
from dex_k8s_client.k8s.cluster import Dex_K8S_Cluster
from dex_k8s_client.k8s.connector import Dex_K8S_Connector
from dex_k8s_client.client import Dex_K8S_Client

# Cluster CA certificate
cluster_ca_cert = None
with open('/my/cluster/ca.crt', 'rb') as f:
  cluster_ca_cert = BytesIO(f.read())

# Dex certificates
dex_client_cert = None
dex_client_key = None
dex_ca_cert = None

with open('/my/dex/client.crt', 'rb') as f:
  dex_client_cert = f.read()

with open('/my/dex/client.key', 'rb') as f:
  dex_client_key = f.read()

with open('/my/dex/ca.crt', 'rb') as f:
  dex_ca_cert = f.read()

# Define your cluster
cluster = Dex_K8S_Cluster('my-cluster-name',
  ca_cert    = cluster_ca_cert,
  api_url    = 'https://mycluster:8443/api/url',
  issuer_url = 'https://mycluster-dex-issuer:5556')

# Define your Dex connection (optional)
dex_connector = Dex_K8S_Connector(
  host = 'mycluster',
  grpc_port = '5557',
  https_port = '5556',
  client_cert = dex_client_cert,
  client_key = dex_client_key,
  ca_cert = dex_ca_cert,
  issuer_url = 'https://mycluster-dex-issuer:5556',
  version = '2.14.0'
)

# Create the client
dex = Dex_K8S_Client(cluster, oauth2=dex_oauth2, grpc=dex_grpc)

# Get a token for a user
token = dex.get_token('client-id', 'client-secret', 'user@domain.com', 'password')

# Get the token JSON
print(json.dumps(token.json()))

# Decode the token to inspect the payload
print(json.dumps(token.decode()))

# Get a kubeconfig for a user
kubeconfig = dex.get_kubeconfig('client-id', 'client-secret', 'user2@domain.com', 'password')

```

# Installation
To install the module with the precompiled protocol buffer bindings:

```sh
python3 setup.py install
```
