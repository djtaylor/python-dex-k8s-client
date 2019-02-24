
class Dex_API_Settings(object):
    """
    Class object for containing settings for a client connection.
    """
    def __init__(self, *args, **kwargs):
        self.host = args[0]
        self.port = args[1]

        # If creating a secure channel
        self.ca_cert = kwargs.get('ca_cert')
        self.client_cert = kwargs.get('client_cert')
        self.client_key = kwargs.get('client_key')

        # Version of Dex API we are connecting to
        self.dex_version = kwargs.get('dex_version')
