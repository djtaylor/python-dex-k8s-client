class Dex_K8S_Bindings_Modules(object):
    """
    Class object for storing proto/grpc module paths.
    """
    def __init__(self, dex_version, mod_base):
        self.proto = '{}.v{}_pb2'.format(mod_base, dex_version.replace('.', '_'))
        self.grpc  = '{}.v{}_pb2_grpc'.format(mod_base, dex_version.replace('.', '_'))

class Dex_K8S_Bindings(object):
    """
    Class object for handling proto bindings for a particular
    version of the Dex API.
    """
    def __init__(self, settings, mod_base='dex_k8s_client.dexidp.dex.api'):
        self.version = settings.dex.version
        self.modules = Dex_K8S_Bindings_Modules(settings.dex.version, mod_base)
