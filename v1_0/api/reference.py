from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
import json


class ReferenceServiceTest(unittest.TestCase):
    def test_anonymous_user(self):
        data = {"reference":["Damon 2018, European Physical Journal Web of Conferences, 186, 12003"]}
        r = anonymous_user.post('/reference/text', json=data)
        self.assertEqual(r.status_code, 401)

    def check_reference_service(self, user=authenticated_user):
        data = {"reference":["Damon 2018, European Physical Journal Web of Conferences, 186, 12003"]}
        r = user.post('/reference/text', json=data)
        self.assertTrue(r.json() == {u'resolved': u'0.7 2018EPJWC.18612003D -- Damon 2018, European Physical Journal Web of Conferences, 186, 12003'})

    def test_authenticated_user(self):
        self.check_reference_service()

    def test_bumblebee_user(self):
        self.check_reference_service(user=bumblebee_user)

if __name__ == '__main__':
    unittest.main()
