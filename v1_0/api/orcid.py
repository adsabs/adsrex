from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest

class TestIt(unittest.TestCase):

    def test_access(self):
        for x in ['/orcid/exchangeOAuthCode', 
                  ]:
            r = anonymous_user.get(x)
            assert r.status_code == 401 # right now it throws 500 (probably error with orcid service)
            
        r = bumblebee_user.get('/orcid/exchangeOAuthCode', params={'code': 'foo'})
        assert r.status_code == 400
        assert r.json()['error'] == 'invalid_grant'
        
        r = authenticated_user.get('/orcid/0000-0001-9886-2511/orcid-profile')
        assert r.status_code == 500 # TODO: should return a json error (orcid-authorizatin header is missing)
    
    
    def test_crossx_headers(self):
        for endpoint in [
                '/orcid/0000-0001-9886-2511/orcid-works',
                '/orcid/0000-0001-9886-2511/orcid-profile'
                ]:
            r = bumblebee_user.options(endpoint)
            
            assert 'access-control-allow-origin' in r.headers
            assert 'ui.adsabs.harvard.edu' in r.headers['access-control-allow-origin']
            assert 'access-control-allow-headers' in r.headers
            assert 'Orcid-Authorization' in r.headers['access-control-allow-headers']
            


if __name__ == '__main__':
    unittest.main()