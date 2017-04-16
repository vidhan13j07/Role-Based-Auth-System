from collections import defaultdict

class RBAS(object):

    def __init__(self):
        # Users alongwith thier roles: { user: set(roles) }
        self.users = defaultdict(set)

        # Roles alongwith the users: { role: set(users) }
        self.roles = defaultdict(set)

        # Resource alongwith actions that can be performed
        self.resources = defaultdict(set)

        # Set of dict objects
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

    def add_action_to_resource(self, resource, action):
        """
        Add action to the resource

        :param resource: Resource on which action can be performed
        :type resource: str
        :param action: Action which is to be performed
        :type action: str
        """
        self.resources[resource].add(action)

    def add_resources(self, _resource, actions=None):
        """
        Adding a resource.

        :param _resource: Resource to be added.
        :type _resource: str or list
        :param actions: actions given to the resource
        :type actions: list or str or None
        """
        self.resources[_resource] = set()
        if actions:
            if isinstance(actions, str):
                actions = [actions]
            for action in actions:
                self.add_action_to_resource(_resource, action)

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

    def get_all_resources(self):
        """
        Returns all the resources

        :rtype: set()
        """
        return set(self.resources.keys())

    def get_actions_resource(self, resource):
        """
        Returns all the actions given to a resource

        :param resource: Resource whose actions are to be returned
        :type resource: str
        :rtype: set()
        """
        return self.resources[resource]

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

    def del_action_resource(self, _resource, action):
        """
        Remove the action given to a resource

        :param _resource: Resource from which action is to be removed
        :type _resource: str
        :param action: Action which is to be removed
        :type action: str
        """
        self.resources[_resource].discard(action)
        self.grant = set([tup for tup in self.grant if tup[1] != _resource and tup[2] != action])


    def del_resource(self, _resource):
        """
        Remove the resource

        :param _resource: Resource to be removed
        :type _resource: str
        """
        del self.resources[_resource]
        self.grant = set([tup for tup in self.grant if tup[1] != _resource])

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
        self.grant.add((role, resource, action))
