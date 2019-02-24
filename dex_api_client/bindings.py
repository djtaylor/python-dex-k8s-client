class Dex_API_Bindings_Modules(object):
    """
    Class object for storing proto/grpc module paths.
    """
    def __init__(self, dex_version, mod_base):
        self.proto = '{}.v{}_pb2'.format(mod_base, dex_version.replace('.', '_'))
        self.grpc  = '{}.v{}_pb2_grpc'.format(mod_base, dex_version.replace('.', '_'))

class Dex_API_Bindings(object):
    """
    Class object for handling proto bindings for a particular
    version of the Dex API.
    """
    def __init__(self, settings, mod_base='dex_api_client.dexidp.dex.api'):
        self.version = settings.dex_version
        self.modules = Dex_API_Bindings_Modules(settings.dex_version, mod_base)
