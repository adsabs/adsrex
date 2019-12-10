from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
import json

object_query = 'object:((Andromeda OR SMC) AND LMC)'
identifiers  = [3133169, 1575544, 2419335, 3253618]
objects = ["NGC 224"]

class ObjectServiceTest(unittest.TestCase):
    def test_anonymous_user(self, user=anonymous_user):
        # Try to get object info for an object query
        r = user.post('/objects/query', json={'query': object_query})
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)
        # Try to get object info for a list of object identifiers
        r = user.post('/objects', json={'identifiers': identifiers})
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)
        # Try to get object info for Classic NED objects search
        payload = {'objects': objects}
        payload['start_year'] = 2016
        payload['output_format'] = 'classic'
        payload['refereed_status'] = 'refereed'
        r = user.post('/objects/nedsrv', json=payload)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)

    def test_authenticated_user(self, user=authenticated_user):
        # Request translation for object query
        r = user.post('/objects/query', json={'query': object_query})
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # The results should be in a dictionary
        self.assertIsInstance(r.json(), dict)
        # Are we getting the expected response
        response = r.json()
        # The response has attribute 'query'
        self.assertCountEqual(list(response.keys()), ['query'])
        # We just want to know that the translated query
        # has the fields simbid:, ned: and abs: in it
        self.assertTrue(response['query'].find('simbid:') > 0)
        self.assertTrue(response['query'].find('nedid:') > 0)
        self.assertTrue(response['query'].find('abs:') > 0)
        # Try to get object info for a list of object identifiers
        r = user.post('/objects', json={'identifiers': identifiers})
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # The results should be in a dictionary
        self.assertIsInstance(r.json(), dict)
        # Check the content sent back
        response = r.json()
        # The keys of the response should be the identifiers submitted
        self.assertCountEqual(list(map(int, list(response.keys()))), identifiers)

    def test_bumblebee_user(self):
        self.test_authenticated_user(user=bumblebee_user)

        

if __name__ == '__main__':
    unittest.main()
