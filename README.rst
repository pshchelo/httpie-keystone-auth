====================
httpie-keystone-auth
====================

OpenStack Keystone auth plugin for `HTTPie <https://httpie.org/>`_.

Installation
============

.. code-block:: bash

   $ pip install --upgrade httpie-keystone-auth

You should now see ``keystone`` under ``--auth-type / -A``
in ``$ http --help`` output.

Usage
=====

Plugin uses ``openstacksdk`` library to parse the ``clouds.yaml`` file and
get the token from Keystone.


A simple example of a ``clouds.yaml`` file is:

.. code-block:: yaml

   clouds:
     mycloud:
       auth:
         auth_url: <url of keystone endpoint>
         username: <username>
         password: <password>
         user_domain_name: <user domain name>
         project_name: <name of the project to authorize to>
         project_domain_name: <domain of the project>
    othercloud:
      auth:
        . . .

Read more about the format of the file and where to place it in
`openstacksdk docs <https://docs.openstack.org/openstacksdk/latest/user/config/configuration.html>`_

Using env var
-------------

You can set ``OS_CLOUD`` env var to a name of one of the clouds in the
``clouds.yaml`` file, which will be then used by plugin:

.. code-block:: bash

   export OS_CLOUD=mycloud
   http -A keystone devstack.local/images/v2/images

Passing cloud name explicitly
-----------------------------

Alternatively you can pass the name of the cloud from the ``clouds.yaml`` file
to use as 'username' to HTTPie:

.. code-block:: bash

   https -A keystone -a myothercloud images.othercloud.com/v2/images

Using service type instead of full service URL
----------------------------------------------

This plugin also simplifies working with OpenStack APIs by allowing you
to specify only the *service type* instead of full URL, e.g

.. code-block:: bash

   https -A keystone compute/servers

Under the hood, the plugin will check if there's any service in the OpenStack
service catalog of your cloud that has the service type as specified in the
first part (netloc) of your URL, and replace this with the endpoint
URL for this service as defined in the catalog for the region and endpoint type
(interface) as set in your ``clouds.yaml``. It will use API version as defined
in the ``clouds.yaml`` file and ``openstacksdk`` defaults.

Additionally, instead of service type that is actually registered
in the service catalog of the cloud, you can also use any of:

- official service type (like ``block-storage``)
- official service type alias (like ``volumev3``)
- OpenStack community project name (like ``cinder``)
- service name as registered in the catalog (can be whatever cloud operator
  decided to name it)

If a single endpoint matching such criteria is found, it will be used.

OpenStack API microversions
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Several OpenStack services use API microversions to alter the API behavior.
The actual header is pretty long and cumbersome to type, and it can vary
for some older versions of some services.

Instead, you can specify a simple header ``v``, and appropriate microversion
header will be included, together with legacy ones if required, e.g.

.. code-block:: bash

   https -A keystone compute/servers v:2.59 -v
   GET /v2.1/servers HTTP/1.1
   ...
   OpenStack-API-Version: compute 2.59 # modern API microversion header
   X-OpenStack-Nova-API-Version: 2.59 # legacy API microversion header
   ...

Note that this only works when using a service type etc instead of full URL.

Limitations
===========
If you are using cloud that needs custom CA bundle file to verify the TLS
connection, you will still have to pass it explicitly to HTTPie
even if it is already set in the ``clouds.yaml`` file.
