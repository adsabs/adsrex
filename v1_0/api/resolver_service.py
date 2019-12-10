from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
import json


class ResolverServiceTest(unittest.TestCase):
    def test_anonymous_user(self):
        r = anonymous_user.get('/resolver/2018EPJWC.18612003D')
        self.assertEqual(r.status_code, 401)

    def check_resolver_service(self, user=authenticated_user):
        r = user.get('/resolver/2018EPJWC.18612003D/abstract')
        self.assertTrue(r.json() == {'action': 'redirect', 'link': '/abs/2018EPJWC.18612003D/abstract', 'service': '/abs/2018EPJWC.18612003D/abstract', 'link_type': 'ABSTRACT'})

        r = user.get('/resolver/2018EPJWC.18612003D/esource')
        self.assertTrue(r.json() == {'action': 'redirect', 'link': 'https://doi.org/10.1051%2Fepjconf%2F201818612003', 'service': 'https://doi.org/10.1051%2Fepjconf%2F201818612003', 'link_type': 'ESOURCE'})

    def test_authenticated_user(self):
        self.check_resolver_service()

    def test_bumblebee_user(self):
        self.check_resolver_service(user=bumblebee_user)

if __name__ == '__main__':
    unittest.main()
