Rbas
---

To start using RBAS, instantiate the ``RBAS`` object:

.. code:: python

    from rbas import RBAS
    rbs = RBAS()

The ``RBAS`` object keeps track of your *resources* and *permissions*
defined on them, handles *grants* over *roles* and provides utilities to
manage them.

Methods
------

``add_role(user, role)``
~~~~~~~~~~~~~~~~~~

Define a role.

-  ``user``: User which is to be assigned the role.

-  ``role``: Role to be defined for the user

.. code:: python

    >>> rbs.add_role('user1', 'r1')

``create_user(user, roles)``
~~~~~~~~~~~~~~~~~~

Creates a user.

-  ``user``: User which is to be created.

-  ``roles``: Roles to be associated with the user.

.. code:: python

    >>> rbs.create_user('user1')
    >>> rbs.create_user('user2', 'r1')
    >>> rbs.create_user('user3', ['r2', 'r1'])

``get_all_users()``
~~~~~~~~~~~~~~~~~~

Returns a set of all the users.

.. code:: python

    >>> rbs.get_all_users()
    {'user2', 'user3', 'user1'}

``get_role_user(user)``
~~~~~~~~~~~~~~~~~~

Returns all roles assigned to the user.

-  ``user``: User whose roles are to be returned.

.. code:: python

    >>> rbs.get_role_user('user3')
    {'r1', 'r2'}

``get_user_role(role)``
~~~~~~~~~~~~~~~~~~

Returns all users assigned to the role.

-  ``role``: Role of which users assigned are to be returned

.. code:: python

    >>> rbs.get_user_role('r1')
    {'user2', 'user3'}


``add_roles(roles)``
~~~~~~~~~~~~~~~~~~~~

Define multiple roles

-  ``roles``: An iterable of roles

.. code:: python

    acl.add_roles(['admin', 'root'])
    acl.get_roles()  # -> {'admin', 'root'}

``add_resource(resource)``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Define a resource.

-  ``resources``: the resource to define.

The resource will have no permissions defined but will appear in
``get_resources()``.

.. code:: python

    acl.add_resource('blog')
    acl.get_resources()  # -> {'blog'}

``add_permission(resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define a permission on a resource.

-  ``resource``: the resource to define the permission on. Is created if
   was not previously defined.
-  ``permission``: the permission to define.

The defined permission is not granted to anyone, but will appear in
``get_permissions(resource)``.

.. code:: python

    acl.add_permission('blog', 'post')
    acl.get_permissions('blog')  # -> {'post'}

``add(structure)``
~~~~~~~~~~~~~~~~~~

Define the whole resource/permission structure with a single dict.

-  ``structure``: a dict that maps resources to an iterable of
   permissions.

.. code:: python

    acl.add({
        'blog': ['post'],
        'page': {'create', 'read', 'update', 'delete'},
    })

Remove
------

``remove_role(role)``
~~~~~~~~~~~~~~~~~~~~~

Remove the role and its grants.

-  ``role``: the role to remove.

.. code:: python

    acl.remove_role('admin')

``remove_resource(resource)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the resource along with its grants and permissions.

-  ``resource``: the resource to remove.

.. code:: python

    acl.remove_resource('blog')

``remove_permission(resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the permission from a resource.

-  ``resource``: the resource to remove the permission from.
-  ``permission``: the permission to remove.

The resource is not implicitly removed: it remains with an empty set of
permissions.

.. code:: python

    acl.remove_permission('blog', 'post')

``clear()``
~~~~~~~~~~~

Remove all roles, resources, permissions and grants.

Get
---

``get_roles()``
~~~~~~~~~~~~~~~

Get the set of defined roles.

.. code:: python

    acl.get_roles()  # -> {'admin', 'anonymous', 'registered'}

``get_resources()``
~~~~~~~~~~~~~~~~~~~

Get the set of defined resources, including those with empty permissions
set.

.. code:: python

    acl.get_resources()  # -> {'blog', 'page', 'article'}

``get_permissions(resource)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get the set of permissions for a resource.

-  ``resource``: the resource to get the permissions for.

.. code:: python

    acl.get_permissions('page')  # -> {'create', 'read', 'update', 'delete'}

``get()``
~~~~~~~~~

Get the *structure*: hash of all resources mapped to their permissions.

Returns a dict: ``{ resource: set(permission,...), ... }``.

.. code:: python

    acl.get()  # -> { blog: {'post'}, page: {'create', ...} }

Export and Import
-----------------

The ``Acl`` class is picklable:

.. code:: python

    acl = miracle.Acl()
    save = acl.__getstate__()

    #...

    acl = miracle.Acl()
    acl.__setstate__(save)

Authorize
=========

Grant Permissions
-----------------

``grant(role, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Grant a permission over resource to the specified role.

-  ``role``: The role to grant the access to
-  ``resource``: The resource to grant the access over
-  ``permission``: The permission to grant with

Roles, resources and permissions are implicitly created if missing.

.. code:: python

    acl.grant('admin', 'blog', 'delete')
    acl.grant('anonymous', 'page', 'view')

``grants(grants)``
~~~~~~~~~~~~~~~~~~

Add a structure of grants to the Acl.

-  ``grants``: A hash in the following form:
   ``{ role: { resource: set(permission) } }``.

.. code:: python

    acl.grants({
        'admin': {
            'blog': ['post'],
        },
        'anonymous': {
            'page': ['view']
        }
    })

``revoke(role, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Revoke a permission over a resource from the specified role.

.. code:: python

    acl.revoke('anonymous', 'page', 'view')
    acl.revoke('user', 'account', 'delete')

``revoke_all(role[, resource])``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Revoke all permissions from the specified role for all resources. If the
optional ``resource`` argument is provided - removes all permissions
from the specified resource.

.. code:: python

    acl.revoke_all('anonymous', 'page')  # revoke all permissions from a single resource
    acl.revoke_all('anonymous')  # revoke permissions from all resources

Check Permissions
-----------------

``check(role, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test whether the given role has access to the resource with the
specified permission.

-  ``role``: The role to check
-  ``resource``: The protected resource
-  ``permission``: The required permission

Returns a boolean.

.. code:: python

    acl.check('admin', 'blog') # True
    acl.check('anonymous', 'page', 'delete') # -> False

``check_any(roles, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test whether *any* of the given roles have access to the resource with
the specified permission.

-  ``roles``: An iterable of roles.

When no roles are provided, returns False.

``check_all(roles, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test whether *all* of the given roles have access to the resource with
the specified permission.

-  ``roles``: An iterable of roles.

When no roles are provided, returns False.

Show Grants
-----------

which\_permissions(role, resource)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List permissions that the provided role has over the resource:

.. code:: python

    acl.which_permissions('admin', 'blog')  # -> {'post'}

which\_permissions\_any(roles, resource)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List permissions that any of the provided roles have over the resource:

.. code:: python

    acl.which_permissions_any(['anonymous', 'registered'], 'page')  # -> {'view'}

which\_permissions\_all(roles, resource)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List permissions that all of the provided roles have over the resource:

.. code:: python

    acl.which_permissions_all(['anonymous', 'registered'], 'page')  # -> {'view'}

``which(role)``
~~~~~~~~~~~~~~~

Collect grants that the provided role has:

.. code:: python

    acl.which('admin')  # -> { blog: {'post'} }

``which_any(roles)``
~~~~~~~~~~~~~~~~~~~~

Collect grants that any of the provided roles have (union).

.. code:: python

    acl.which(['anonymous', 'registered'])  # -> { page: ['view'] }

``which_all(roles)``
~~~~~~~~~~~~~~~~~~~~

Collect grants that all of the provided roles have (intersection):

.. code:: python

    acl.which(['anonymous', 'registered'])  # -> { page: ['view'] }

``show()``
~~~~~~~~~~

Get all current grants.

Returns a dict ``{ role: { resource: set(permission) } }``.

.. code:: python

    acl.show()  # -> { admin: { blog: ['post'] } }

.. |Build Status| image:: https://travis-ci.org/kolypto/py-miracle.png?branch=master
   :target: https://travis-ci.org/kolypto/py-miracle

