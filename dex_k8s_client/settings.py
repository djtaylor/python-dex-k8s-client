from dex_k8s_client.k8s.cluster import Dex_K8S_Cluster
from dex_k8s_client.k8s.connector import Dex_K8S_Connector

class Dex_K8S_Settings(object):
    """
    Class object for storing client settings.
    """
    def __init__(self, cluster, connector):

        # Enforce class instance requirements
        if not isinstance(cluster, Dex_K8S_Cluster):
            raise Exception('`cluster` argument must be an instance of Dex_K8S_Cluster')
        if not isinstance(connector, Dex_K8S_Connector):
            raise Exception('`cluster` argument must be an instance of Dex_K8S_Connector')

        self.cluster = cluster
        self.dex     = connector
