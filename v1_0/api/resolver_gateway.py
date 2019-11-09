from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
import json
import v1_0.config as config


class ResolverGatewayTest(unittest.TestCase):
    def test_anonymous_user(self):
        r = anonymous_user.get(config.API_URL.rsplit('/', 1)[0] + '/link_gateway/2018EPJWC.18612003D/abstract')
        self.assertEqual(r.status_code, 200)

    def check_resolver_gateway(self, user=authenticated_user):
        r = anonymous_user.get(config.API_URL.rsplit('/', 1)[0] + '/link_gateway/2018EPJWC.18612003D/abstract')
        self.assertEqual(r.status_code, 200)

        r = anonymous_user.get(config.API_URL.rsplit('/', 1)[0] + '/link_gateway/2018EPJWC.18612003D/abstract')
        self.assertEqual(r.status_code, 200)

    def test_authenticated_user(self):
        self.check_resolver_gateway()

    def test_bumblebee_user(self):
        self.check_resolver_gateway(user=bumblebee_user)

if __name__ == '__main__':
    unittest.main()
