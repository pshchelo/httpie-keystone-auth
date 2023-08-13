"""
OpenStack Keystone Auth plugin for HTTPie
"""
# TODO: try to handle debug logging (openstack.enable_logging(http_debug=True)
# TODO: try to use TLS config from clouds.yaml
# TODO: try to understand if there's a password set in the clouds.yaml
# and prompt for password if it is absent and auth_type is password-like
from urllib import parse

from httpie.plugins import AuthPlugin
import openstack
import os_service_types


__version__ = "0.2.0"
__author__ = "Pavlo Shchelokovskyy"
__license__ = "MIT"

service_types = os_service_types.get_service_types()


def _get_service_type(cloud, candidate):
    if cloud.has_service(candidate):
        return candidate
    # check for project and service type aliases
    project_service_type = service_types.get_service_data_for_project(
        candidate)
    types_and_aliases = service_types.get_all_types(
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


# adapted from keystoneauth1.session module
def _get_api_version_headers(service_type, microversion):
    header_service_type = service_types.get_service_type(service_type,
                                                         permissive=True)
    if header_service_type == "block-storage":
        header_service_type = "volume"
    headers = {
        "OpenStack-API-Version": f"{header_service_type} {microversion}"}
    if header_service_type == "compute":
        headers["X-OpenStack-Nova-API-Version"] = microversion
    elif header_service_type == "baremetal":
        headers["X-OpenStack-Ironic-API-Version"] = microversion
    elif header_service_type == "shared-file-system":
        headers["X-OpenStack-Manila-API-Version"] = microversion
    return headers


class KeystoneAuth:
    def __init__(self, cloud_name=None, password=None):
        self._cloud_name = cloud_name

    def __call__(self, req):
        cloud = openstack.connect(cloud=self._cloud_name)
        token_header = cloud.session.get_auth_headers()
        req.headers.update(token_header)
        # mangle URL
        orig_parsed = parse.urlparse(req.url)
        service_type = _get_service_type(cloud, orig_parsed.netloc)
        if service_type:
            endpoint = cloud.session.get_endpoint_data(
                service_type=service_type).url.rstrip("/")
            new_parsed = parse.urlparse(endpoint)
            req.url = parse.urlunparse(
                (new_parsed.scheme, new_parsed.netloc,
                 new_parsed.path + orig_parsed.path,
                 orig_parsed.params, orig_parsed.query, orig_parsed.fragment)
            )
            microversion = req.headers.pop("v", None)
            if microversion:
                microversion_headers = _get_api_version_headers(
                    service_type, microversion.decode())
                for h, v in microversion_headers.items():
                    req.headers.setdefault(h, v)
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
