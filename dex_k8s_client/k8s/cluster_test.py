import unittest
from dex_k8s_client.k8s.cluster import Dex_K8S_Cluster

class Dex_K8S_Cluster_Test(unittest.TestCase):
    """Tests for `k8s/cluster.py`."""

    def test_create_cluster_instance(self):
        """ Test creating a new Dex_K8S_Cluster instance """
        cluster = Dex_K8S_Cluster('name', 'ca_cert', 'api_url')
        self.assertIsInstance(cluster, Dex_K8S_Cluster)
