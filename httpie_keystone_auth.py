"""
OpenStack Keystone Auth plugin for HTTPie
"""
from urllib import parse

from httpie.plugins import AuthPlugin
import openstack


__version__ = "0.2.0"
__author__ = "Pavlo Shchelokovskyy"
__license__ = "MIT"


class KeystoneAuth:
    def __init__(self, cloud_name=None, password=None):
        self._cloud_name = cloud_name

    def __call__(self, req):
        # TODO: try to use TLS config from clouds.yaml
        # TODO: try to understand if there's a password set
        # in the clouds.yaml and prompt for password if it is absent
        cloud = openstack.connect(cloud=self._cloud_name)
        # TODO: handle API microversions easier
        token_header = cloud.session.get_auth_headers()
        req.headers.update(token_header)
        # mangle URL
        orig_parsed = parse.urlparse(req.url)
        try:
            # hoping that orig_parsed.netloc is a service type that
            # has an endpoint in the cloud
            # TODO: support service type aliases and project names
            service_type = orig_parsed.netloc
            endpoint = cloud.session.get_endpoint_data(
                service_type=service_type).url
        except Exception:
            # bail out, mangle nothing, probably a explicit url instead
            # of service type
            pass
        else:
            new_parsed = parse.urlparse(endpoint)
            req.url = parse.urlunparse(
                (new_parsed.scheme, new_parsed.netloc,
                 new_parsed.path + orig_parsed.path,
                 orig_parsed.params, orig_parsed.query, orig_parsed.fragment)
            )
        return req


class KeystoneAuthPlugin(AuthPlugin):
    name = "OpenStack Keystone Auth"
    auth_type = "keystone"
    description = (
        "Authorize against OpenStack Keystone using info from clouds.yaml file"
    )
    auth_require = False
    prompt_password = False

    def get_auth(self, username=None, password=None):
        return KeystoneAuth(cloud_name=username, password=password)
