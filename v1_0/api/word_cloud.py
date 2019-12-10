from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
import json
    
# We will do all tests for the famous author A. Accomazzi
params = {}
params['q'] = 'author:"Accomazzi,A" year:1991-1993'

class VisServiceTest(unittest.TestCase):
    def test_anonymous_user(self):
        # Get the word cloud
        r = anonymous_user.post('/vis/word-cloud', json={'query': [json.dumps(params)]})
        # This should get a 401 back
        self.assertEqual(r.status_code, 401)
    
    def check_word_cloud(self, user=authenticated_user):
        # Retrieve results for our query in 'params'
        r = user.post('/vis/word-cloud', json={'query': [json.dumps(params)]})
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        data = r.json()
        # We are sent back a dictionary
        self.assertIsInstance(data, dict)
        # Each entry of this dictionary is a dictionary
        expected_attr = ['idf','record_count','total_occurrences']
        for entry in list(data.values()):
            self.assertIsInstance(entry, dict)
            # With expected keys
            self.assertCountEqual(expected_attr, list(entry.keys()))

    def test_authenticated_user(self):
        self.check_word_cloud()

    def test_bumblebee_user(self):
        self.check_word_cloud(user=bumblebee_user)


if __name__ == '__main__':
    unittest.main()