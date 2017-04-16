import unittest
import rbas

class TestRbas(unittest.TestCase):
    def test_user(self):
        rbs = rbas.RBAS()

        rbs.create_user('user1')
        rbs.create_user('user2', 'role1')
        self.assertSetEqual(rbs.get_role_user('user2'), {'role1'})

        rbs.create_user('user3', ['role1', 'role2'])
        self.assertSetEqual(rbs.get_role_user('user3'), {'role1', 'role2'})

        self.assertSetEqual(rbs.get_all_users(), {'user1', 'user2', 'user3'})
        self.assertSetEqual(rbs.get_user_role('role1'), {'user2', 'user3'})

        rbs.del_user('user2')
        self.assertSetEqual(rbs.get_all_users(), {'user1', 'user3'})

        rbs.del_role_from_user('user3', 'role1')
        self.assertSetEqual(rbs.get_role_user('user3'), {'role2'})

    def test_resources(self):
        rbs = rbas.RBAS()

        rbs.add_resources('r1')
        rbs.add_resources('r2')
        self.assertSetEqual(rbs.get_all_resources(), {'r1', 'r2'})

        rbs.del_resource('r1')
        self.assertSetEqual(rbs.get_all_resources(), {'r2'})

        rbs.add_resources('r3', ['read', 'write'])
        self.assertSetEqual(rbs.get_actions_resource('r3'), {'read', 'write'})

        rbs.del_action_resource('r3', 'read')
        self.assertSetEqual(rbs.get_actions_resource('r3'), {'write'})


if __name__ == "__main__":
    unittest.main()
