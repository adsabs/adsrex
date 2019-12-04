from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
import json


class OracleServiceTest(unittest.TestCase):
    def test_anonymous_user(self):
        data = {"reader":"0000000000000000"}
        r = anonymous_user.post('/_oracle/readhist', json=data)
        self.assertEqual(r.status_code, 401)

    def check_oracle_service(self, user=authenticated_user):
        data = {"reader": "0000000000000000"}
        r = user.post('/_oracle/readhist', json=data)
        print r.json()
        self.assertTrue(r.json() == {u'query': u'(similar(topn(10, reader:0000000000000000, entry_date desc)) entdate:[NOW-5DAYS TO *])', u'error': u'no result from solr with status code=200'})

    def test_authenticated_user(self):
        self.check_oracle_service()

    def test_bumblebee_user(self):
        self.check_oracle_service(user=bumblebee_user)

if __name__ == '__main__':
    unittest.main()
