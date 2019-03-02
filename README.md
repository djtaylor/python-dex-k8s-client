[![Build Status](https://api.travis-ci.org/djtaylor/python-dex-k8s-client.png)](https://api.travis-ci.org/djtaylor/python-dex-k8s-client)

# Dex K8S Client
This module is designed to interact with a [Dex](https://github.com/dexidp/dex) server running on Kubernetes using both gRPC and HTTP calls to handle user authorization and authentication programmatically.

# Dex Versions
This module comes with precompiled protocol buffer bindings for targeted Dex gRPC API versions. As of the creation of this repository, the latest version is `2.14.0`. See the [protocol file](proto/dex_api_client/dexidp/dex/api/v2_14_0.proto) for available API methods.

# Basic Usage
The following shows same basic use cases for this module:

```python3
from dex_k8s_client.k8s.cluster import Dex_K8S_Cluster
from dex_k8s_client.k8s.connector import Dex_K8S_Connector
from dex_k8s_client.client import Dex_K8S_Client

# Define your cluster
cluster = Dex_K8S_Cluster('my-cluster-name', '/my/cluster/ca.crt', 'https://mycluster:8443/api/url')

# Define your Dex connection
dex_connector = Dex_K8S_Connector(
  host = 'mycluster',
  grpc_port = '5557',
  https_port = '5556',
  client_cert = '/my/dex/client.crt',
  client_key = '/my/dex/client.key',
  ca_cert = '/my/dex/ca.crt',
  issuer_url = 'https://mycluster-dex-issuer:5556',
  version = '2.14.0'
)

# Create the client
dex = Dex_K8S_Client(cluster, connector)

# Get a token for a user
token = dex.get_token('client-id', 'client-secret', 'user@domain.com', 'password')

# Get a kubeconfig for a user
kubeconfig = dex.get_kubeconfig('client-id', 'client-secret', 'user2@domain.com', 'password')

```

# Installation
To install the module with the precompiled protocol buffer bindings:

```sh
python3 setup.py install
```
