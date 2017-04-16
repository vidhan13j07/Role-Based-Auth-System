import unittest
import rbas

class TestRbas(unittest.TestCase):
    def test_user(self):
        rbs = rbas.RBAS()

        rbs.create_user('user1')
        rbs.create_user('user2', 'role1')
        self.assertSetEqual(rbs.get_role_user('user2'), set(['role1']))

        rbs.create_user('user3', ['role1', 'role2'])
        self.assertSetEqual(rbs.get_role_user('user3'), set(['role1', 'role2']))

        self.assertSetEqual(rbs.get_all_users(), set(['user1', 'user2', 'user3']))
        self.assertSetEqual(rbs.get_user_role('role1'), set(['user2', 'user3']))

        rbs.del_user('user2')
        self.assertSetEqual(rbs.get_all_users(), set(['user1', 'user3']))

        rbs.del_role_from_user('user3', 'role1')
        self.assertSetEqual(rbs.get_role_user('user3'), set(['role2']))

    def test_grant(self):
        rbs = rbas.RBAS()

        rbs.grant_action('r1', 'resource1', 'read')
        rbs.remove_resource('resource1')
        self.assertSetEqual(rbs.get_all_grants(), set())

        rbs.grant_action('r1', 'resource', 'read')
        rbs.grant_action('r1', 'resource', 'write')
        rbs.remove_action_resource('resource', 'read')
        self.assertEqual(list(rbs.get_all_grants()), [('r1', 'resource', 'write')])

    def test_role_grant(self):
        rbs = rbas.RBAS()

        rbs.grant_action('r1', 'resource1', 'read')
        rbs.grant_action('r2', 'resource1', 'read')
        rbs.grant_action('r1', 'resource1', 'write')
        rbs.grant_action('r2', 'resource1', 'delete')

        self.assertTrue(rbs.check_role('r1', 'resource1', 'write'))
        self.assertTrue(rbs.check_role('r2', 'resource1', 'delete'))
        self.assertFalse(rbs.check_role('r1', 'resource1', 'delete'))
        self.assertFalse(rbs.check_role('r2', 'resource1', 'write'))

    def test_user_grant(self):
        rbs = rbas.RBAS()

        l = [
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
        rbs.add('user1', l)
        self.assertTrue(rbs.check_user('user1', 'rs2', 'delete'))
        self.assertFalse(rbs.check_user('user1', 'rs2', 'read'))
        self.assertTrue(rbs.check_user('user1', 'rs1', 'read'))
        self.assertFalse(rbs.check_user('user1', 'rs4', 'delete'))

if __name__ == "__main__":
    unittest.main()
