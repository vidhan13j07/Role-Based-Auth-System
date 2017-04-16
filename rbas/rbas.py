from collections import defaultdict

class RBAS(object):

    def __init__(self):
        # Users alongwith thier roles: { user: set(roles) }
        self.users = defaultdict(set)

        # Roles alongwith the users: { role: set(users) }
        self.roles = defaultdict(set)

        # Set of tuple objects
        self.grant = set()

    def add_role(self, _user, role):
        """
        Add a role

        :param _user: User which is to be assigned the role
        :type _user: str
        :param role: Role to be defined for the user
        :type role: str
        """
        self.users[_user].add(role)
        if role not in self.roles:
            self.roles[role] = set()
        self.roles[role].add(_user)

    def create_user(self, _user, roles=None):
        """
        Creating a user.

        :param _user: User which is to be created
        :type _user: str
        :param role: Role to be associated with the user
        :type role: str ot list
        """
        self.users[_user] = set()
        if roles:
            if isinstance(roles, str):
                roles = [roles]
            for role in roles:
                self.add_role(_user, role)

    def get_all_users(self):
        """
        Returns all the users

        :rtype: set()
        """
        return set(self.users.keys())

    def get_role_user(self, _user):
        """
        Returns all roles assigned to a user

        :param _user: user whose roles are to be returned
        :type _user: str
        :rtype: set()
        """
        return self.users[_user]

    def get_user_role(self, _role):
        """
        Returns all users assigned the role

        :param _role: Role of which users assigned are to be returned
        :type _role: str
        :rtype: set()
        """
        return self.roles[_role]

    def del_role_from_user(self, _user, _role):
        """
        Remove the user from the role

        :param _user: User which has to be disassociated with the role
        :type _user: str
        :param _role: Role that has to be removed from the user
        :type _role: str
        """
        self.users[_user].discard(_role)
        self.roles[_role].discard(_user)
        if self.roles[_role] == set():
            del self.roles[_role]
            self.grant = set([tup for tup in self.grant if tup[0] != _role])

    def del_user(self, _user):
        """
        Remove the user and its associated roles

        :param _user: user to be deleted
        :type _user: str
        """
        if _user in self.users:
            for role in self.users[_user]:
                self.roles[role].discard(_user)
                if self.roles[role] == set():
                    del self.roles[role]
                    self.grant = set([tup for tup in self.grant if tup[0] != role])
            del self.users[_user]

    def grant_action(self, role, resource, action):
        """
        Define an action of a role on the resource

        :param role: Role which can perform action
        :type role: str
        :param resource: Resource on which action can be performed
        :type resource: str
        :param action: Action that is permitted to be performed
        :type action: str
        """
        tup = (role, resource, action)
        self.grant.add(tup)

    def get_all_grants(self):
        """
        Return all the grants

        :rtype: set()
        """
        return self.grant

    def remove_grant(self, role, resource, action):
        """
        Remove an action of a role on the resource

        :param role: Role of which can perform action is to be removed from resource
        :type role: str
        :param resource: Resource on which action is to be removed
        :type resource: str
        :param action: Action that is to be removed
        :type action: str
        """
        tup = (role, resource, action)
        self.grant.discard(tup)

    def remove_resource(self, resource):
        """
        Remove the resource from the grant

        :param resource: Resource to be deleted
        :type resource: str
        """
        self.grant = set([tup for tup in self.grant if tup[1] != resource])

    def remove_action_resource(self, resource, action):
        """
        Remove the resource from the grant

        :param resource: Resource to be deleted
        :type resource: str
        :param action: Action to be deleted
        :type resource: str
        """
        self.grant = set([tup for tup in self.grant if tup[1] != resource or tup[2] != action])


    def remove_all(self, role, resource=None):
        """
        Define an action of a role on the resource

        :param role: Role of which actions on resources are to be removed
        :type role: str
        :param resource: Resource on which action is to be removed
        :type resource: str or None
        """
        self.grant = {tup for tup in self.grant if not (tup[0] == role and (resource is None or tup[1] == resource))}

    def check_role(self, role, resource, action):
        """
        Tests whether the given role has access to an action for a resource

        :param role: Role on which the check is to done.
        :type role: str
        :param resource: Resource on which check is to be done.
        :type resource: str
        :param action: Action which is to be checked
        :type action: str
        :rtype: bool
        """
        return (role, resource, action) in self.grant

    def check_user(self, user, resource, action):
        """
        Tests whether the given role has access to an action for a resource

        :param user: User on which the check is to done.
        :type user: str
        :param resource: Resource on which check is to be done.
        :type resource: str
        :param action: Action which is to be checked
        :type action: str
        :rtype: bool
        """
        ok = False
        for role in self.users[user]:
            if self.check_role(role, resource, action):
                ok = True
        return ok

    def add(self, user, obj):
        """
        Adding actions to resources with roles defined for user

        {user: [role, {resource, action}]}

        :param obj: Nested dictionary containing all the information
        :type obj: dict
        """
        roleslist = []
        for role in obj:
            roleslist.append(role['name'])
            for key, value in role['resources'].items():
                for it in value:
                    self.grant_action(role['name'], key, it)
        self.create_user(user, roleslist)
