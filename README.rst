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

Notes
=====

For now tested only with standard ``password`` auth type of Keystone,
but should work with any auth_type supported in the ``clouds.yaml`` file.

TODO
====
- simplify usage by allowing URLs in the form of
  ``<service-type-or-service-name>`` by getting them out from Keystone catalog
  of the cloud being used
- for password-like auth type, check that the password is provided in the
  ``clouds.yaml`` and prompt for password if it is not
