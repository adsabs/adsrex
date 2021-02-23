from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
    
bibcode = '2012ApJ...750L..25J'
    
class GraphicsServiceTest(unittest.TestCase):
    def test_anonymous_user(self):
        # Try to get graphics info for an existing bibcode
        r = anonymous_user.get('/graphics/%s'%bibcode)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)
        # The same for a non-existing bibcode
        r = anonymous_user.get('/graphics/foo')
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)
    
    def test_authenticated_user(self, user=authenticated_user):
        # Get graphics for an existing bibcode
        r = user.get('/graphics/%s'%bibcode)
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        data = r.json()
        # The data structure sent back has a 'bibcode' entry,
        # which should contain the request bibcode
        self.assertEqual(data['bibcode'], bibcode)
        # The attribute 'figures' should be a list
        self.assertIsInstance(data['figures'], list)
        # The list of figures should not be empty
        self.assertTrue(len(data['figures']) > 0)
        # The attribute 'images' refers to a list
        self.assertIsInstance(data['figures'][0]['images'], list)
        # A non-existing bibcode should still return a 200
        r = user.get('/graphics/foo')
        self.assertEqual(r.status_code, 200)
        # But the data structure sent back should have an 'Error' attribute
        self.assertIn('Error', r.json())
    
    def test_bumblebee_user(self):
        self.test_authenticated_user(user=bumblebee_user)


if __name__ == '__main__':
    unittest.main()
