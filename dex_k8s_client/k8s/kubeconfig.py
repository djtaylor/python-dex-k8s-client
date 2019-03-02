from yaml import load as load_yaml
from io import StringIO

TEMPLATE = """
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: {cluster_ca}
    server: "{api_url}"
  name: {cluster_name}
contexts:
- context:
    cluster: {cluster_name}
    user: {email}
  name: {cluster_name}
current-context: {cluster_name}
kind: Config
preferences: {{}}
users:
- name: {email}
  user:
    auth-provider:
      config:
        client-id: {client_id}
        client-secret: {client_secret}
        id-token: {id_token}
        idp-issuer-url: {issuer_url}
        refresh-token: {refresh_token}
      name: oidc
"""

class Dex_K8S_KubeConfig(object):
    """
    Class object for constructing a kubeconfig.
    """
    @staticmethod
    def from_template(**kwargs):
        """
        Construct and return a kubeconfig from a template.
        """
        return load_yaml(StringIO(TEMPLATE.format(**kwargs)))
