"""
OpenStack Keystone Auth plugin for HTTPie
"""
from urllib import parse

from httpie.plugins import AuthPlugin
import openstack
import os_service_types


__version__ = "0.2.0"
__author__ = "Pavlo Shchelokovskyy"
__license__ = "MIT"


def _get_service_type(cloud, candidate):
    if cloud.has_service(candidate):
        return candidate
    st = os_service_types.get_service_types()
    # check for project and service type aliases
    project_service_type = st.get_service_data_for_project(candidate)
    types_and_aliases = st.get_all_types(
        project_service_type['service_type'] if project_service_type
        else candidate
    )
    exists = [t for t in types_and_aliases if cloud.has_service(t)]
    if len(exists) == 1:
        return exists[0]
    # check for service name
    endpoints_with_service_name = [
        e for e in cloud.service_catalog if e["name"] == candidate]
    if len(endpoints_with_service_name) == 1:
        return endpoints_with_service_name[0]["type"]
    return None


class KeystoneAuth:
    def __init__(self, cloud_name=None, password=None):
        self._cloud_name = cloud_name

    def __call__(self, req):
        # TODO: try to use TLS config from clouds.yaml
        # TODO: try to understand if there's a password set
        # in the clouds.yaml and prompt for password if it is absent
        cloud = openstack.connect(cloud=self._cloud_name)
        token_header = cloud.session.get_auth_headers()
        req.headers.update(token_header)
        # mangle URL
        orig_parsed = parse.urlparse(req.url)
        service_type = _get_service_type(cloud, orig_parsed.netloc)
        if service_type:
            endpoint = cloud.session.get_endpoint_data(
                service_type=service_type).url
            new_parsed = parse.urlparse(endpoint)
            req.url = parse.urlunparse(
                (new_parsed.scheme, new_parsed.netloc,
                 new_parsed.path + orig_parsed.path,
                 orig_parsed.params, orig_parsed.query, orig_parsed.fragment)
            )
            # TODO: handle API microversions easier
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
