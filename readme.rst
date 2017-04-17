RBAS
-------------------------------------------------------------------

To start using RBAS, instantiate the ``RBAS`` object:

.. code:: python

    from rbas import RBAS
    rbs = RBAS()

The ``RBAS`` object keeps track of your *resources* and *actions*
defined on them, handles *grants* over *roles* and provides utilities to
manage them.

Methods
-------------------------------------------------------------------

``add_role(user, role)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define a role.

-  ``user``: User which is to be assigned the role.

-  ``role``: Role to be defined for the user

.. code:: python

    >>> rbs.add_role('user1', 'role1')

``create_user(user, roles)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creates a user.

-  ``user``: User which is to be created.

-  ``roles``: Roles to be associated with the user.

.. code:: python

    >>> rbs.create_user('user1')
    >>> rbs.create_user('user2', 'role1')
    >>> rbs.create_user('user3', ['role2', 'role1'])

``get_all_users()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a *set* of all the users.

.. code:: python

    >>> rbs.get_all_users()
    {'user2', 'user3', 'user1'}

``get_role_user(user)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a *set* of roles assigned to the user.

-  ``user``: User whose roles are to be returned.

.. code:: python

    >>> rbs.get_role_user('user3')
    {'role1', 'role2'}

``get_user_role(role)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a *set* of users assigned to the role.

-  ``role``: Role of which users assigned are to be returned

.. code:: python

    >>> rbs.get_user_role('role1')
    {'user2', 'user3'}

``del_role_from_user(user, role)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the user from the role.

-  ``user``: User which has to be disassociated with the role.

-  ``role``: Role that has to be removed from the user.

  .. code:: python

    >>> rbs.del_role_from_user('user3', 'role1')

``del_user(user)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the user and its associated roles

-  ``user``: User which has to be deleted.

  .. code:: python

    >>> rbs.del_user('user1')

``grant_action(role, resource, action)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define an action of a role on the resource

-  ``role``: The role to grant the access to

-  ``resource``: The resource to grant the access over

-  ``action``: The action to grant with

.. code:: python

    >>> rbs.grant('role1', 'rs1', 'delete')
    >>> rbs.grant('role2', 'rs2', 'read')

``get_all_grants()``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Return all the grants

.. code:: python

    >>> rbs.get_all_grants()
    {('role1', 'rs1', 'delete'), ('role2', 'rs2', 'read')}

``remove_grant(role, resource, action)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove an action of a role on the resource

-  ``role``: Role of which action is to be removed from resource

-  ``resource``: Resource on which action is to be removed

-  ``action``: Action that is to be removed

.. code:: python

    >>> rbs.remove_grant('role1', 'rs1', 'delete')
    >>> rbs.get_all_grants()
    {('role2', 'rs2', 'read')}

``remove_resource(resource)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the resource from the grant.

-  ``resource``: Resource to be deleted

.. code:: python

    >>> rbs.remove_resource('rs2')
    >>> rbs.get_all_grants()
    {}

``remove_action_resource(resource, action)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the resource and action from the grant.

-  ``resource``: Resource to be deleted.

-  ``action``: Action to be deleted.

.. code:: python

    >>> rbs.grant_action('role1', 'rs2', 'read')
    >>> rbs.remove__action_resource('rs2', 'read')
    >>> rbs.get_all_grants()
    {}

``remove_all(role, resource=None)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the grants given to a role.

-  ``role``: Role of which actions on resources are to be removed

-  ``resource``: Resource on which action is to be removed.

.. code:: python

    >>> rbs.grant_action('role1', 'rs2', 'read')
    >>> rbs.grant_action('role1', 'rs1', 'write')
    >>> rbs.remove_all('role1')
    >>> rbs.get_all_grants()
    {}


``check_role(role, resource, action)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests whether the given role has access to an action for a resource

-  ``role``: The role to check

-  ``resource``: The protected resource

-  ``action``: The required action

Returns a *boolean*.

.. code:: python

    >>> rbs.check_role('role1', 'rs1', 'read')
    True
    >>> rbs.check_role('role1', 'rs1', 'delete')
    False

``check_user(user, resource, action)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tests whether the given role has access to an action for a resource

-  ``user``: The user to check

-  ``resource``: The protected resource

-  ``action``: The required action

Returns a *boolean*.

.. code:: python

    >>> rbs.check_role('user1', 'r1', 'read')
    True
    >>> rbs.check_role('user1', 'r1', 'delete')
    False

``add(user, obj)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Adding actions to resources with roles defined for user

-  ``user``: The user which is being added.

-  ``obj``: Nested dictionary containing all the information

.. code:: python

    >>> rbs = rbas.RBAS()

    >>> l = [
            {
                'name': 'r1',
                'resources': {
                        'rs1': ['read', 'delete'],
                        'rs2': ['write']
                    }
            },
            {
                'name': 'r2',
                'resources': {
                        'rs2': ['delete'],
                        'rs3': ['read']
                    }
            }
        ]

	>>> rbs.add('user1', l)
