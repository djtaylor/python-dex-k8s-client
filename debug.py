import json
from os.path import expanduser
from dex_k8s_client.client import Dex_K8S_Client
from dex_k8s_client.k8s.cluster import Dex_K8S_Cluster
from dex_k8s_client.k8s.connector import Dex_K8S_Connector

cluster_name = 'minikube'
cluster_ca_cert = expanduser('~/.minikube/ca.crt')
cluster_api_url = 'https://kubernetes:8443'

# Define the cluster you will be connecting to
cluster = Dex_K8S_Cluster(
    name    = cluster_name,
    ca_cert = cluster_ca_cert,
    api_url = cluster_api_url
)

# Define the Dex connector attributes
connector = Dex_K8S_Connector(
    host = 'kubernetes',
    grpc_port = '30557',
    https_port = '30556',
    client_cert = expanduser('~/git/minikube-cluster/tls/certs/dex-grpc-client-tls.pem'),
    client_key = expanduser('~/git/minikube-cluster/tls/keys/dex-grpc-client-tls.pem'),
    ca_cert = expanduser('~/git/minikube-cluster/tls/certs/ca.pem'),
    issuer_url = 'https://kubernetes:30556',
    version = '2.14.0'
)

# Create the Dex client for this cluster
dex = Dex_K8S_Client(cluster, connector)

client_id = 'minikube'
client_secret = 'somereallysecuresecretfortesting'

kubeconfig_yaml = dex.get_kubeconfig(client_id, client_secret, 'jane.doe@minikube.local', 'password')

print(json.dumps(kubeconfig_yaml, indent=2))
