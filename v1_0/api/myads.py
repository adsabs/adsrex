from v1_0.user_roles import anonymous_user, authenticated_user
import unittest
from adsmutils import get_date

class TestIt(unittest.TestCase):
    def test_anonymous_user(self):
        for x in ['/vault/configuration', 
                  '/vault/user-data', 
                  '/vault/query/sfsfs-sfsdfsdf-sfsdf-sfsdf']:
            r = anonymous_user.get(x)
            assert r.status_code == 401
        
        # should be accessible? return 404 when not exists (well, no 404 - because we don't want to give up information)
        r = anonymous_user.get('/vault/query2svg/113dc6ef2e612ffe1a0de9a16e7f494e')
        assert r.status_code == 401
    
    def test_authenticated_user(self):
        # bumblebee config
        r = authenticated_user.get('/vault/configuration')
        assert r.status_code == 200
        assert isinstance(r.json(), dict)
        assert 'link_servers' not in r.json()
        
        r = authenticated_user.get('/vault/configuration/link_servers')
        assert r.status_code == 200
        assert isinstance(r.json(), list)
        assert len(r.json()) > 100
        
        
        foo = get_date().isoformat()
        # server side user storage
        r = authenticated_user.post('/vault/user-data', json={'link_server': foo})
        assert r.status_code == 200
        assert r.json()['link_server'] == foo
        
        r = authenticated_user.get('/vault/user-data')
        assert r.status_code == 200
        assert isinstance(r.json(), dict)
        assert r.json()['link_server'] == foo
        
        
        # i'm using my own access token, once we switch to a dedicated account
        # made only for testing, the qid will change too
        r = authenticated_user.post('/vault/query', json={'q': '*:*'})
        assert r.status_code == 200
        assert isinstance(r.json(), dict)
        qid = r.json()['qid']
        numFound = r.json()['numFound']
        
        r = authenticated_user.get('/vault/query/%s' % qid)
        assert r.status_code == 200
        assert 'numfound' in r.json()
        
        r = authenticated_user.get('/vault/execute_query/%s' % qid)
        assert r.status_code == 200
        assert r.json()['responseHeader']['params']['q'] == '*:*'
        assert r.json()['responseHeader']['params']['fl'] == 'id'
        assert r.json()['responseHeader']['params']['x-amzn-trace-id']
        assert r.json()['response']
        self.assertAlmostEqual(r.json()['response']['numFound'], int(numFound), delta=10000)
        
        r = authenticated_user.get('/vault/execute_query/%s?fl=recid' % qid)
        assert r.status_code == 200
        assert r.json()['responseHeader']['params']['q'] == '*:*'
        assert r.json()['responseHeader']['params']['fl'] == 'recid'
        assert r.json()['response']
        
        
        # 113dc6ef2e612ffe1a0de9a16e7f494e
        r = authenticated_user.get('/vault/query2svg/%s' % qid)
        assert 'svg' in r.text
        assert r.headers.get('Content-Type') == 'image/svg+xml'
        

if __name__ == '__main__':
    unittest.main()        
