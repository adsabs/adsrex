from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
import json


class AuthorAffiliationServiceTest(unittest.TestCase):
    def test_anonymous_user(self):
        data = {"bibcode": ["2018EPJWC.18612003D"], "maxauthor":0, "numyears":4}
        r = anonymous_user.post('author-affiliation/search', json=data)
        self.assertEqual(r.status_code, 401)

    def check_author_affiliation_service(self, user=authenticated_user):
        data = {"bibcode": ["2018EPJWC.18612003D"], "maxauthor":0, "numyears":4}
        r = user.post('author-affiliation/search', json=data)
        self.assertTrue(r.json() == {"data": [
            {"affiliations": {"lastActiveDate": "2018/07", "name": "NASA ADS; orcid.org/0000-0002-4110-3511", "years": ["2018"]},
             "authorName": "Accomazzi, Alberto"},
            {"affiliations": {"lastActiveDate": "2018/07", "name": "NASA ADS; orcid.org/0000-0002-1069-2376", "years": ["2018"]},
             "authorName": "Damon, James"},
            {"affiliations": {"lastActiveDate": "2018/07", "name": "NASA ADS; orcid.org/0000-0003-4264-2450", "years": ["2018"]},
             "authorName": "Henneken, Edwin"}]})

    def test_authenticated_user(self):
        self.check_author_affiliation_service()

    def test_bumblebee_user(self):
        self.check_author_affiliation_service(user=bumblebee_user)

if __name__ == '__main__':
    unittest.main()
