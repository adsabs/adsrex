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
            "/alive",
            "/author-affiliation/alive",
            "/author-affiliation/export",
            "/author-affiliation/ready",
            "/author-affiliation/search",
            "/biblib/alive",
            "/biblib/classic",
            "/biblib/documents/<string:library>",
            "/biblib/libraries",
            "/biblib/libraries/operations/<string:library>",
            "/biblib/libraries/<string:library>",
            "/biblib/permissions/<string:library>",
            "/biblib/ready",
            "/biblib/resources",
            "/biblib/transfer/<string:library>",
            "/biblib/twopointoh",
            "/citation_helper/",
            "/citation_helper/alive",
            "/citation_helper/ready",
            "/export/aastex",
            "/export/aastex/<bibcode>",
            "/export/ads",
            "/export/ads/<bibcode>",
            "/export/alive",
            "/export/bibtex",
            "/export/bibtexabs",
            "/export/bibtexabs/<bibcode>",
            "/export/bibtex/<bibcode>",
            "/export/convert",
            "/export/csl",
            "/export/custom",
            "/export/dcxml",
            "/export/dcxml/<bibcode>",
            "/export/endnote",
            "/export/endnote/<bibcode>",
            "/export/icarus",
            "/export/icarus/<bibcode>",
            "/export/medlars",
            "/export/medlars/<bibcode>",
            "/export/mnras",
            "/export/mnras/<bibcode>",
            "/export/procite",
            "/export/procite/<bibcode>",
            "/export/ready",
            "/export/refabsxml",
            "/export/refabsxml/<bibcode>",
            "/export/refworks",
            "/export/refworks/<bibcode>",
            "/export/refxml",
            "/export/refxml/<bibcode>",
            "/export/ris",
            "/export/ris/<bibcode>",
            "/export/rss",
            "/export/rss/<bibcode>/",
            "/export/rss/<bibcode>/<path:link>",
            "/export/soph",
            "/export/soph/<bibcode>",
            "/export/votable",
            "/export/votable/<bibcode>",
            "/graphics/alive",
            "/graphics/ready",
            "/graphics/<string:bibcode>",
            "/harbour/alive",
            "/harbour/auth/classic",
            "/harbour/auth/twopointoh",
            "/harbour/export/twopointoh/<export>",
            "/harbour/libraries/classic/<int:uid>",
            "/harbour/libraries/twopointoh/<int:uid>",
            "/harbour/mirrors",
            "/harbour/myads/classic/<int:uid>",
            "/harbour/ready",
            "/harbour/user",
            "/harbour/version",
            "/metrics/",
            "/metrics/alive",
            "/metrics/ready",
            "/metrics/<string:bibcode>",
            "/oauth/authorize",
            "/oauth/errors/",
            "/oauth/info/",
            "/oauth/invalid/",
            "/oauth/ping/",
            "/oauth/ping/",
            "/oauth/token",
            "/objects/",
            "/objects/alive",
            "/objects/nedsrv",
            "/objects/query",
            "/objects/ready",
            "/objects/<string:objects>",
            "/objects/<string:objects>/<string:source>",
            "/orcid/alive",
            "/orcid/exchangeOAuthCode",
            "/orcid/export/<iso_datestring>",
            "/orcid/get-profile/<orcid_id>",
            "/orcid/<orcid_id>/orcid-profile",
            "/orcid/<orcid_id>/orcid-profile/<type>",
            "/orcid/<orcid_id>/orcid-work",
            "/orcid/<orcid_id>/orcid-works",
            "/orcid/<orcid_id>/orcid-works/<putcode>",
            "/orcid/orcid-name/<orcid_id>",
            "/orcid/preferences/<orcid_id>",
            "/orcid/ready",
            "/orcid/update-orcid-profile/<orcid_id>",
            "/orcid/update-status/<orcid_id>",
            "/protected",
            "/ready",
            "/reference/alive",
            "/reference/ready",
            "/reference/text",
            "/reference/text/<reference>",
            "/reference/xml",
            "/resolver/alive",
            "/resolver/<bibcode>",
            "/resolver/<bibcode>/<link_type>",
            "/resolver/<bibcode>/<link_type>:<path:id>",
            "/resolver/delete",
            "/resolver/ready",
            "/resolver/resources",
            "/resolver/update",
            "/search/alive",
            "/search/bigquery",
            "/search/qtree",
            "/search/query",
            "/search/ready",
            "/search/resources",
            "/search/status",
            "/search/tvrh",
            "/status",
            "/user/<string:identifier>",
            "/vault/alive",
            "/vault/configuration",
            "/vault/configuration/<key>",
            "/vault/execute_query/<queryid>",
            "/vault/query",
            "/vault/query2svg/<queryid>",
            "/vault/query/<queryid>",
            "/vault/ready",
            "/vault/user-data",
            "/vis/alive",
            "/vis/author-network",
            "/vis/paper-network",
            "/vis/ready",
            "/vis/word-cloud",
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