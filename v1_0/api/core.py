from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import time
import unittest
import adsmutils
import datetime


#resources as of Beehive@v1.0.122

api_resources = {
    "adsws.accounts": {
        "base": "/v1/accounts",
        "endpoints": [
            "/oauth/authorize",
            "/oauth/invalid/",
            "/oauth/errors/",
            "/oauth/token",
            "/oauth/ping/",
            "/oauth/ping/",
            "/oauth/info/",
            "/user/delete",
            "/change-password",
            "/change-email",
            "/bootstrap",
            "/protected",
            "/register",
            "/status",
            "/logout",
            "/ready",
            "/alive",
            "/token",
            "/csrf",
            "/user",
            "/reset-password/<string:token>",
            "/verify/<string:token>",
            "/info/<string:account_data>"
        ]
    },
    "adsws.api": {
        "base": "/v1",
        "endpoints": [
            "/harbour/auth/twopointoh",
            "/harbour/auth/classic",
            "/author-affiliation/search",
            "/author-affiliation/export",
            "/author-affiliation/ready",
            "/author-affiliation/alive",
            "/citation_helper/ready",
            "/citation_helper/alive",
            "/reference/ready",
            "/reference/alive",
            "/reference/text",
            "/reference/xml",
            "/resolver/resources",
            "/resolver/delete",
            "/resolver/update",
            "/resolver/ready",
            "/resolver/alive",
            "/graphics/ready",
            "/graphics/alive",
            "/harbour/mirrors",
            "/harbour/version",
            "/objects/nedsrv",
            "/objects/ready",
            "/objects/alive",
            "/objects/query",
            "/metrics/ready",
            "/metrics/alive",
            "/harbour/ready",
            "/harbour/alive",
            "/harbour/user",
            "/biblib/twopointoh",
            "/search/resources",
            "/biblib/resources",
            "/biblib/libraries",
            "/export/bibtexabs",
            "/export/refabsxml",
            "/search/bigquery",
            "/export/refworks",
            "/biblib/classic",
            "/export/endnote",
            "/export/procite",
            "/export/convert",
            "/export/medlars",
            "/export/votable",
            "/search/status",
            "/export/refxml",
            "/export/aastex",
            "/export/custom",
            "/export/bibtex",
            "/export/icarus",
            "/search/ready",
            "/search/alive",
            "/search/query",
            "/search/qtree",
            "/biblib/ready",
            "/biblib/alive",
            "/export/mnras",
            "/export/dcxml",
            "/export/ready",
            "/export/alive",
            "/search/tvrh",
            "/export/soph",
            "/export/csl",
            "/export/ris",
            "/export/ads",
            "/export/rss",
            "/orcid/exchangeOAuthCode",
            "/vault/configuration",
            "/oauth/authorize",
            "/vault/user-data",
            "/oauth/invalid/",
            "/oauth/errors/",
            "/oauth/token",
            "/vault/ready",
            "/vault/alive",
            "/vault/query",
            "/orcid/ready",
            "/orcid/alive",
            "/oauth/ping/",
            "/oauth/ping/",
            "/oauth/info/",
            "/vis/author-network",
            "/vis/paper-network",
            "/vis/word-cloud",
            "/vis/ready",
            "/vis/alive",
            "/citation_helper/",
            "/protected",
            "/objects/",
            "/metrics/",
            "/status",
            "/ready",
            "/alive",
            "/resolver/<bibcode>/<link_type>:<path:id>",
            "/harbour/libraries/twopointoh/<int:uid>",
            "/harbour/libraries/classic/<int:uid>",
            "/harbour/export/twopointoh/<export>",
            "/harbour/myads/classic/<int:uid>",
            "/biblib/libraries/operations/<string:library>",
            "/export/rss/<bibcode>/<path:link>",
            "/orcid/<orcid_id>/orcid-profile/<type>",
            "/orcid/<orcid_id>/orcid-works/<putcode>",
            "/reference/text/<reference>",
            "/resolver/<bibcode>/<link_type>",
            "/objects/<string:objects>/<string:source>",
            "/biblib/permissions/<string:library>",
            "/biblib/documents/<string:library>",
            "/biblib/libraries/<string:library>",
            "/export/bibtexabs/<bibcode>",
            "/export/refabsxml/<bibcode>",
            "/biblib/transfer/<string:library>",
            "/export/refworks/<bibcode>",
            "/export/endnote/<bibcode>",
            "/export/procite/<bibcode>",
            "/export/votable/<bibcode>",
            "/export/medlars/<bibcode>",
            "/export/bibtex/<bibcode>",
            "/export/refxml/<bibcode>",
            "/export/icarus/<bibcode>",
            "/export/aastex/<bibcode>",
            "/export/dcxml/<bibcode>",
            "/export/mnras/<bibcode>",
            "/export/soph/<bibcode>",
            "/export/ris/<bibcode>",
            "/export/ads/<bibcode>",
            "/export/rss/<bibcode>/",
            "/orcid/update-orcid-profile/<orcid_id>",
            "/vault/execute_query/<queryid>",
            "/vault/configuration/<key>",
            "/orcid/update-status/<orcid_id>",
            "/orcid/get-profile/<orcid_id>",
            "/orcid/preferences/<orcid_id>",
            "/orcid/orcid-name/<orcid_id>",
            "/vault/query2svg/<queryid>",
            "/orcid/export/<iso_datestring>",
            "/vault/query/<queryid>",
            "/orcid/<orcid_id>/orcid-profile",
            "/orcid/<orcid_id>/orcid-works",
            "/orcid/<orcid_id>/orcid-work",
            "/resolver/<bibcode>",
            "/graphics/<string:bibcode>",
            "/objects/<string:objects>",
            "/metrics/<string:bibcode>",
            "/user/<string:identifier>"
        ]
    },
    "adsws.feedback": {
        "base": "/v1/feedback",
        "endpoints": [
            "/oauth/authorize",
            "/oauth/invalid/",
            "/oauth/errors/",
            "/oauth/token",
            "/oauth/ping/",
            "/oauth/ping/",
            "/oauth/info/",
            "/ready",
            "/alive",
            "/slack"
        ]
    }
}

class CitationHelperServiceTest(unittest.TestCase):
    def test_resources(self):
        
        # /v1/resources doesn't exist (but I think it should exist)
        r = anonymous_user.get('/resources')
        assert r.status_code == 404
        
        # the response is organized from the perspective of the ADS developer/ API maintainer
        # but API users probably expect to see something like:
        # {
        # '/v1': {
        #    'endpoints': [
        #       '/search/query'
        #        ...
        #     ]
        #  },
        # '/v2': {
        #    'endpoints': [
        #       '/search/newquery',
        #       ...
        #     ]
        #  }
        # }
        #
        # If we run two versions of the API alongside, I don't see 
        # how the current structure can communicate two different 
        # 'bases'
        
        # hack to get to the resources
        url = '/'.join(anonymous_user.get_config('API_URL').split('/')[0:-1])
        r = anonymous_user.get( url + '/resources')
        resources = r.json()
        
        self.assertDictContainsSubset(api_resources, resources)
    
    def test_limits_authenticated(self):    
        self.check_limits(user=authenticated_user)
    def test_limits_bbb(self):    
        self.check_limits(user=bumblebee_user)
        
    def check_limits(self, user=authenticated_user):
        # Check the response contains Headers
        # and the limits are there
        r = user.get('/search/query', params={'q': 'title:"%s"' % time.time()})
        assert r.headers['X-Ratelimit-Limit']
        
        old_limit = int(r.headers['X-RateLimit-Remaining'])
        r = user.get('/search/query', params={'q': 'title:"%s"' % time.time()})
        assert r.headers['X-RateLimit-Remaining'] == str(old_limit-1)
        assert 'X-RateLimit-Reset' in r.headers
        
        
    def test_bootstrap(self):
        expires = datetime.datetime.fromordinal(adsmutils.get_date().toordinal() + 5)
        params = {'expires': expires.isoformat(), 'ratelimit': 0.001, 'create_new' : False}
        r = authenticated_user.get('/accounts/bootstrap', params=params)
        a = r.json()
        
        r = anonymous_user.get('/accounts/bootstrap', params=params)
        b = r.json()
        
        # currently fails, it returns 'anonymous' for the
        # authenticated user if the user in db has empty 'is_active' column
        # also, the ratelimits must allow for more clients (i.e. be not fully
        # consumed)
        assert a['username'] != b['username']
        assert a['access_token'] != b['access_token']
        assert a['username'] == 'tester@ads'
        assert b['username'] == 'anonymous@ads'
        
        # repeating the bootstrap request should give you the
        # same access token
        for x in xrange(5):
            r = anonymous_user.get('/accounts/bootstrap', params=params, headers={'Authorization': 'Bearer %s' % b['access_token']})
            assert r.json()['access_token'] == b['access_token']
            
        for x in xrange(5):
            r = authenticated_user.get('/accounts/bootstrap', params=params)
            assert r.json()['access_token'] == a['access_token']
            
            
    def test_crossx_headers(self):
        # XXX: this should be improved (but in general, the microservices
        # should test for headers that they require (e.g. Orcid-Authorization
        # is tested in orcid)
        for endpoint in [
                         '/accounts/bootstrap'
                         ]:
            r = bumblebee_user.options(endpoint)
            
            # the value of this header will differ between staging and production
            assert 'access-control-allow-origin' in r.headers
            assert 'ui.adsabs.harvard.edu' in r.headers['access-control-allow-origin']
            assert 'access-control-allow-headers' in r.headers
            assert r.headers['access-control-allow-headers']
        
            
if __name__ == '__main__':
    unittest.main()            