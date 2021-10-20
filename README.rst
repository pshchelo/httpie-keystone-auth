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

This plugin can also simplify working with OpenStack APIs by allowing you
to specify only the *service type* instead of full URL, e.g

.. code-block:: bash

   https -A keystone compute/servers

Under the hood, the plugin will check if there's any service in the OpenStack
service catalog of your cloud that has the service type as specified in the
first part (netloc) of your URL, and replace this first path with endpoint
URL for this service as defined in the catalog for the region and endpoint type
(interface) as set in your ``clouds.yaml``.

Note on API versions
~~~~~~~~~~~~~~~~~~~~
Services in the OpenStack catalog can be versioned and unversioned.
In the case of an unversioned endpoint, you will have to provide the
version in your URL explicitly, for example:

- Image service has catalog entry as "https://glance.mycloud.com"
  To list images using v2 images API, you will have to call
  ``image/v2/images`` URL with HTTPie.
- Compute service usually has catalog entry that is both versioned
  and also contains the OpenStack project UUID the request is scoped to,
  like "https://nova.mycloud.com/v2.1/1234567890absdef1234567890absdef".
  In this case you should simply call HTTPie with e.g. ``compute/servers``
  URL to list servers.

Limitations
===========
If you are using cloud that needs custom CA bundle file to verify the TLS
connection, you will still have to pass it explicitly to HTTPie
even if it is already set in the ``clouds.yaml`` file.

TODO
====
- for password-like auth type, check that the password is provided in the
  ``clouds.yaml`` and prompt for password if it is not provided as "password"
  to HTTPie.
