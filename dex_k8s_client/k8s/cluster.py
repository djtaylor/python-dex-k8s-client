class Dex_K8S_Cluster(object):
    """
    Class object for passing to the client class for defining
    and storing cluster attributes.
    """
    def __init__(self, name, ca_cert, api_url):
        self.name    = name
        self.ca_cert = ca_cert
        self.api_url = api_url
