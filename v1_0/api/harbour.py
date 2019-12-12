from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest


class HarbourServiceTest(unittest.TestCase):
    def test_anonymous_user(self):
        r = anonymous_user.get('harbour/mirrors')
        self.assertEqual(r.status_code, 401)

    def check_harbour_service(self, user=authenticated_user):
        r = user.get('harbour/mirrors')
        self.assertTrue('adsabs.harvard.edu' in r.json())

    def test_authenticated_user(self):
        self.check_harbour_service()

    def test_bumblebee_user(self):
        self.check_harbour_service(user=bumblebee_user)

if __name__ == '__main__':
    unittest.main()
