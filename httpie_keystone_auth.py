"""
OpenStack Keystone Auth plugin for HTTPie
"""
from httpie.plugins import AuthPlugin
import openstack


__version__ = "0.1.1"
__author__ = "Pavlo Shchelokovskyy"
__license__ = "MIT"


class KeystoneAuth:
    def __init__(self, cloud=None):
        self._cloud = cloud

    def __call__(self, r):
        cloud = openstack.connect(cloud=self._cloud)
        # TODO: try to understand if there's a password set
        # in the clouds.yaml and prompt for password if it is absent
        token_header = cloud.session.get_auth_headers()
        r.headers.update(token_header)
        return r


class KeystoneAuthPlugin(AuthPlugin):
    name = "OpenStack Keystone Auth"
    auth_type = "keystone"
    description = ""
    auth_require = False
    prompt_password = False

    def get_auth(self, username=None, password=None):
        return KeystoneAuth(username)
