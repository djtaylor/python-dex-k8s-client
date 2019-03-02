from html.parser import HTMLParser

class Dex_K8S_OAuth2_Parser(object):
    """
    Class object for parsing out useful informaton from HTTP/HTML responses
    from Dex. Yes this is ugly, but I want to programmatically auth users
    to multiple Kubernetes cluster. So far this is the only way I have found.
    """

    @staticmethod
    def get_ldap_authentication_uri(html_content, settings):
        """
        Extract the URI for authenticating against the LDAP connector as well
        as the auth_code for the token request.
        """

        links = []
        class Parse_Authentication_Response(HTMLParser):
            def handle_starttag(self, tag, attrs):
                if tag != 'a':
                    return
                attr = dict(attrs)
                links.append(attr)

        parser = Parse_Authentication_Response()
        parser.feed(html_content)

        ldap_uri = None
        for link in links:
            if link['href'].startswith('/auth/ldap'):
                ldap_uri = link['href']
                break

        return 'https://{0}:{1}{2}'.format(
            settings.dex.host,
            settings.dex.https_port,
            ldap_uri
        )
