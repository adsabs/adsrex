from classic2die.user_roles import anonymous_user_classic, authenticated_user_classic
import unittest
from urlparse import urlparse
import pickle
import os
import sys
    
bibcodes = ['1993CoPhC..74..239H','1994GPC.....9...69H']

class TestPatterns(unittest.TestCase):
    
    
    def test_anonymous_user(self): 
        self.check_urls(user=anonymous_user_classic)
    
    def xtest_authenticated_user(self):
        self.check_urls(user=authenticated_user_classic)
        
    def assertRedirected(self, user, r, target, code=302):
        self.assertEquals(r.status_code, code)
        self.assertTrue('Location' in r.headers)
        expected = '%s/%s' % (user.get_config('BBB_URL'), target)
        u = urlparse(expected)
        expected = u.geturl().replace(u.path, u.path.replace('//', '/'))
        self.assertEquals(r.headers['Location'], expected)
    
    def p(self, r):
        print 'url', r.url
        print 'status', r.status_code
        for x in sorted(r.headers.items(), key=lambda x:x[0]):
            print x[0], x[1]
        print 'text', r.text[0:100].replace('\n', '\\n')
        print 'len', len(r.text)
            
        
    @property
    def cache(self):
        if os.path.exists('classic2die.cache'):
            with open('classic2die.cache', 'rb') as f:
                return pickle.load(f)
        return {'finished': {}}
    
    def persist_cache(self, cache):
        with open('classic2die.cache', 'wb') as fo:
            pickle.dump(cache, fo)
        
    def check_urls(self, user=anonymous_user_classic):
        cache = self.cache
        
        # it makes no difference if those are accessed by authenticated user
        # or anonymous user
        try:
            for m in sorted(dir(self)):
                if m.startswith('url_'):
                    key = '%s%s' % (str(user.__class__), m)
                    if key in cache['finished']:
                        print 'skipping %s (already ran with result: %s)' % (m, cache['finished'][key])
                        continue

                    getattr(self, m)(user=user)
                    cache['finished'][key] = True
        finally:
            if 'last-failed' in cache and cache['last-failed'] == key:
                cache['finished'][key] = False
            cache['last-failed'] = key
            self.persist_cache(cache)

        
    def url_000(self, user=anonymous_user_classic):
        """
        (000) /cgi-bin/t2png?<params> freq=11235128 (internal traffic: 1.00, orig_status=200)
        """
        r = user.get('/cgi-bin/t2png?bg=%23FFFFFF&/seri/NASCP/3111/200/0000103.000&db_key=AST&bits=3&scale=8&filetype=.gif')
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.text.startswith(u'GIF87'))
    
    
    def url_001(self, user=anonymous_user_classic):
        """
        (001) /abs/<19> freq=3027798 (internal traffic: 0.12, orig_status=200)
        """
        r = user.get('/abs/1998SPIE.3368..392B')
        
        # going to bbb (core should respond)
        self.assertRedirected(user, r, '/abs/1998SPIE.3368..392B')
        
        # we see the abstract
        r = user.get(r.headers['Location'])
        self.assertEquals(r.status_code, 200)
        self.assertTrue('Programmable personality interface for the dynamic infrared scene generator' in r.text)
    
    
    def url_002(self, user=anonymous_user_classic):
        """
        (002) /favicon.ico freq=1860777 (internal traffic: 0.68, orig_status=200)
        """
        r = user.get('/favicon.ico')
        self.assertEquals(r.status_code, 200)
        #TODO: what should happen if resource exists on both sites? like favicon.ico here?
    
    
    def url_003(self, user=anonymous_user_classic):
        """
        (003) /full/<3/19/16> freq=1149235 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/full/gif/1988ApJ...329L..57T/L000057.000.html')
        self.assertEquals(r.status_code, 200)
        
    
    
    def url_004(self, user=anonymous_user_classic):
        """
        (004) /cgi-bin/nph-data_query?<params> freq=955869 (internal traffic: 0.71, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-data_query?bibcode=2012ApJ...760...34F&db_key=AST&link_type=ARTICLE')
        self.assertRedirected(user, r, '/link_gateway/2012ApJ...760...34F/esource')
        
        r = user.get(r.headers['Location'])
        self.assertTrue(r.status_code, 200)
        self.assertTrue('<a href="https://arxiv.org/abs/1210.0085">https://arxiv.org/abs/1210.0085</a>' in r.text)
    
    
    def url_005(self, user=anonymous_user_classic):
        """
        (005) /cgi-bin/nph-abs_connect?<params> freq=729533 (internal traffic: 0.77, orig_status=200)
        """
        
        # this query is valid, but finds nothing on classic side; but it asks for XML (which should go through)
        r = user.get('/cgi-bin/nph-abs_connect?qsearch=&bibcode=0803983468&start_nr=0&nr_to_return=30&sort=SCORE&data_type=XML&version=1')
        self.assertEquals(r.status_code, 200)
        self.assertTrue('</records>' in r.text)
        
        r = user.get('/cgi-bin/nph-abs_connect?qsearch=&bibcode=0803983468&start_nr=0&nr_to_return=30&sort=SCORE&data_type=HTM&version=1')
        self.assertRedirected(user, r, '/tugboat/classicSearchRedirect?qsearch=&bibcode=0803983468&start_nr=0&nr_to_return=30&sort=SCORE&data_type=HTM&version=1')
        
        r = user.get(r.headers['Location'])
        self.assertRedirected(user, r, '/search/q%3D%2A:%2A%26sort%3Ddate%20desc%2C%20bibcode%20desc%26rows%3D30%26start%3D0%26format%3DHTM%26unprocessed_parameter%3DAll%20object%20queries%20include%20SIMBAD%20and%20NED%20search%20results.%26unprocessed_parameter%3DPlease%20note%20Min%20Score%20is%20deprecated.%26unprocessed_parameter%3DUse%20For%20Weighting%26unprocessed_parameter%3DRelative%20Weights%26unprocessed_parameter%3DWeighted%20Scoring%26unprocessed_parameter%3DSynonym%20Replacement/')

        
        # ERROR: this fills the form with '*:*' query and completely forgets the submitted value
        # this might mean that there are other combinations of parameters that might result in
        # a response, but incorrect results
        r = user.get(r.headers['Location'])
        self.assertTrue(r.status_code, 200)
        self.assertTrue('0803983468' in r.text) # fails
    
    
    def url_006(self, user=anonymous_user_classic):
        """
        (006) /full/<10/4/5/4/0/24> freq=724223 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/full/thumbnails/seri/ApJ../0329//1988ApJ...329L..57T.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_007(self, user=anonymous_user_classic):
        """
        (007) /full/<6/4/5/4/0/24> freq=723631 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/full/record/seri/ApJ../0329//1988ApJ...329L..57T.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_008(self, user=anonymous_user_classic):
        """
        (008) /full/<19> freq=479145 (internal traffic: 0.05, orig_status=200)
        """
        r = user.get('/full/1995ESASP.371...79M')
        self.assertEquals(r.status_code, 200)
        self.assertTrue('http://articles.adsabs.harvard.edu/seri/ESASP/0371//1995ESASP.371...79M.html' in r.text)
    
    
    def url_009(self, user=anonymous_user_classic):
        """
        (009) /doi/<7/6> freq=387419 (internal traffic: 0.02, orig_status=200)
        """
        r = user.get('/doi/10.1086/177092')
        self.assertRedirected(user, r, '/abs/10.1086/177092')
    
    
    def url_010(self, user=anonymous_user_classic):
        """
        (010) /full/<19/16> freq=370508 (internal traffic: 0.97, orig_status=200)
        """
        r = user.get('/full/1951C&T....67....1B/0000008.000.html')
        self.assertEquals(r.status_code, 200)
        self.assertTrue('<frame src="http://articles.adsabs.harvard.edu/full/gif/1951C%26T....67....1B/0000008.000.html" name="gif">' in r.text)
    
    
    def url_011(self, user=anonymous_user_classic):
        """
        (011) /abstract_service.html freq=319857 (internal traffic: 0.15, orig_status=200)
        """
        r = user.get('/abstract_service.html')
        self.assertRedirected(user, r, '/classic-form') # for AA: should be '/classic-form/'
        
        # TODO: remove once above is fixed
        r = user.get(r.headers['Location'])
        # SBC: request to https://dev.adsabs.harvard.edu/classic-form
        # gets redirected to http://dev.adsabs.harvard.edu/classic-form/
        # note the wrong protocol
        
        self.assertRedirected(user, r, '/classic-form/', 301) # fails, https != http
        
        r = user.get(r.headers['Location'])
        self.assertEquals(r.status_code, 200)
        
    
    def url_012(self, user=anonymous_user_classic):
        """
        (012) /cgi-bin/nph-iarticle_query?<params> freq=317369 (internal traffic: 0.81, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-iarticle_query?1951C%26T....67....1B&defaultprint=YES&page_ind=6&filetype=.pdf')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.headers['Content-Type'], 'application/pdf')
    
    
    def url_013(self, user=anonymous_user_classic):
        """
        (013) /cgi-bin/nph-ref_query?<params> freq=310869 (internal traffic: 0.32, orig_status=200)
        """
        # AA: should this not be translated? i think we can handle it
        r = user.get('/cgi-bin/nph-ref_query?bibcode=2012PhPl...19h2902W&amp;refs=CITATIONS&amp;db_key=PHY')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.headers['Content-Type'], 'text/html; charset=ISO-8859-1')
        
    
    def url_014(self, user=anonymous_user_classic):
        """
        (014) /cgi-bin/t2png?<params> freq=238054 (internal traffic: 1.00, orig_status=304)
        """
        r = user.get('/cgi-bin/t2png?bg=%23FFFFFF&/conf/foap./2007/200/0000579.000&db_key=AST&bits=3&scale=8&filetype=.jpg')
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.headers['Content-Type'], 'image/jpeg')
    
    
    def url_015(self, user=anonymous_user_classic):
        """
        (015) / freq=225000 (internal traffic: 0.14, orig_status=200)
        """
        # for AA: this displays the classic form, shouldn't it redirect to BBB?
        r = user.get('/')
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.headers['Content-Type'], 'text/html; charset=UTF-8')
    
    
    def url_016(self, user=anonymous_user_classic):
        """
        (016) /cgi-bin/basic_connect?<params> freq=163385 (internal traffic: 0.59, orig_status=200)
        """
        r = user.get('/cgi-bin/basic_connect?qsearch=Dr+James+Webb&version=1')
        # for AA: it does not redirecto to tugboat
        self.assertRedirected(user, r, '/tugboat/classicSearchRedirect?qsearch=Dr+James+Webb&version=1') # fails
    
    
    def url_017(self, user=anonymous_user_classic):
        """
        (017) /figs/newlogo.gif freq=135019 (internal traffic: 0.85, orig_status=200)
        """
        r = user.get('/figs/newlogo.gif')
        self.p(r)
        self.assertEquals(r.status_code, 200)
    
    
    def url_018(self, user=anonymous_user_classic):
        """
        (018) /abs_doc/classic_form_analytics.js freq=122442 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/abs_doc/classic_form_analytics.js')
        self.assertEquals(r.status_code, 200)
    
    
    def url_019(self, user=anonymous_user_classic):
        """
        (019) /figs/dot.gif freq=108436 (internal traffic: 0.87, orig_status=200)
        """
        r = user.get('/figs/dot.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_020(self, user=anonymous_user_classic):
        """
        (020) /figs/newlogo_small.gif freq=104679 (internal traffic: 0.87, orig_status=200)
        """
        r = user.get('/figs/newlogo_small.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_021(self, user=anonymous_user_classic):
        """
        (021) /pdf<0/19> freq=103256 (internal traffic: 0.04, orig_status=200)
        """
        r = user.get('/pdf/1990ApJ...359..267K')
        self.assertEquals(r.status_code, 200)
    
    
    def url_022(self, user=anonymous_user_classic):
        """
        (022) /figs/cfalogo.gif freq=103079 (internal traffic: 0.88, orig_status=200)
        """
        r = user.get('/figs/cfalogo.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_023(self, user=anonymous_user_classic):
        """
        (023) /figs/nasalogo.gif freq=102252 (internal traffic: 0.88, orig_status=200)
        """
        r = user.get('/figs/nasalogo.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_024(self, user=anonymous_user_classic):
        """
        (024) /cgi-bin/nph-ref_history?<params> freq=87250 (internal traffic: 0.91, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-ref_history?refs=AR&bibcode=2019arXiv190900340K')
        self.assertEquals(r.status_code, 200)
    
    
    def url_025(self, user=anonymous_user_classic):
        """
        (025) /abs/<19> freq=81913 (internal traffic: 0.14, orig_status=200)
        """
        r = user.head('/abs/2019A&A...622A.193A')
        self.assertEquals(r.status_code, 200)
    
    
    def url_026(self, user=anonymous_user_classic):
        """
        (026) /cgi-bin/nph-manage_account?<params> freq=80016 (internal traffic: 0.40, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-manage_account?man_cmd=login&man_url=http://adsabs.harvard.edu/cgi-bin/nph-manage%5faccount%3fman%5fcmd%3dlogin%26man%5furl%3dhttp%3a//adsabs.harvard.edu/abs/2017Sci...357..687T')
        self.assertEquals(r.status_code, 200)
    
    
    def url_027(self, user=anonymous_user_classic):
        """
        (027) /cgi-bin/access_denied freq=78455 (internal traffic: 0.53, orig_status=403)
        """
        r = user.get('/cgi-bin/access_denied')
        self.assertEquals(r.status_code, 403)
    
    
    def url_028(self, user=anonymous_user_classic):
        """
        (028) /cgi-bin/author_form?<params> freq=78371 (internal traffic: 0.73, orig_status=200)
        """
        r = user.get('/cgi-bin/author_form?author=Mattor,+N&fullauthor=Mattor,%20Nathan&charset=UTF-8&db_key=PHY')
        self.assertEquals(r.status_code, 200)
    
    
    def url_029(self, user=anonymous_user_classic):
        """
        (029) /cgi-bin/nph-bib_query?<params> freq=75411 (internal traffic: 0.68, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-bib_query?bibcode=2019arXiv190502773B&data_type=BIBTEX&db_key=PRE&nocookieset=1')
        self.assertEquals(r.status_code, 200)
    
    
    def url_030(self, user=anonymous_user_classic):
        """
        (030) /cgi-bin/nph-abs_connect freq=70251 (internal traffic: 0.96, orig_status=200)
        """
        r = user.post('/cgi-bin/nph-abs_connect')
        self.assertEquals(r.status_code, 200)
    
    
    def url_031(self, user=anonymous_user_classic):
        """
        (031) /figs/adslogo.gif freq=67185 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/figs/adslogo.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_032(self, user=anonymous_user_classic):
        """
        (032) /ads_abstracts.html freq=57286 (internal traffic: 0.78, orig_status=200)
        """
        r = user.get('/ads_abstracts.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_033(self, user=anonymous_user_classic):
        """
        (033) /cgi-bin/bib_query?<params> freq=49817 (internal traffic: 0.11, orig_status=200)
        """
        r = user.get('/cgi-bin/bib_query?arXiv:1511.06066')
        self.assertEquals(r.status_code, 200)
    
    
    def url_034(self, user=anonymous_user_classic):
        """
        (034) /figs/xml.gif freq=48349 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/figs/xml.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_035(self, user=anonymous_user_classic):
        """
        (035) * freq=47740 (internal traffic: 0.00, orig_status=200)
        """
        r = user.options('*')
        self.assertEquals(r.status_code, 200)
    
    
    def url_036(self, user=anonymous_user_classic):
        """
        (036) /cgi-bin/nph-basic_connect?<params> freq=47386 (internal traffic: 0.06, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-basic_connect?qsearch=10%2E1021%2Facs%2Ejcim%2E9b00620&start_nr=0&nr_to_return=30&sort=SCORE&data_type=XML&version=1')
        self.assertEquals(r.status_code, 200)
    
    
    def url_037(self, user=anonymous_user_classic):
        """
        (037) /cgi-bin/nph-basic_connect freq=44468 (internal traffic: 1.00, orig_status=200)
        """
        r = user.post('/cgi-bin/nph-basic_connect')
        self.assertEquals(r.status_code, 200)
    
    
    def url_038(self, user=anonymous_user_classic):
        """
        (038) /figs/addtomyyahoo.gif freq=44265 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/figs/addtomyyahoo.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_039(self, user=anonymous_user_classic):
        """
        (039) /cgi-bin/exec_myads2?<params> freq=38624 (internal traffic: 0.06, orig_status=200)
        """
        r = user.get('/cgi-bin/exec_myads2?id=372349790&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 200)
    
    
    def url_040(self, user=anonymous_user_classic):
        """
        (040) /figs/nasalogo_med.png freq=37684 (internal traffic: 1.00, orig_status=200)
        """
        r = user.get('/figs/nasalogo_med.png')
        self.assertEquals(r.status_code, 200)
    
    
    def url_041(self, user=anonymous_user_classic):
        """
        (041) /figs/si_logo.gif freq=37550 (internal traffic: 1.00, orig_status=200)
        """
        r = user.get('/figs/si_logo.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_042(self, user=anonymous_user_classic):
        """
        (042) /abs_doc/ads.css freq=36660 (internal traffic: 1.00, orig_status=200)
        """
        r = user.get('/abs_doc/ads.css')
        self.assertEquals(r.status_code, 200)
    
    
    def url_043(self, user=anonymous_user_classic):
        """
        (043) /figs/myadslogo.gif freq=33025 (internal traffic: 0.02, orig_status=200)
        """
        r = user.get('/figs/myadslogo.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_044(self, user=anonymous_user_classic):
        """
        (044) /abs/<19> freq=29979 (internal traffic: 0.01, orig_status=302)
        """
        r = user.get('/abs/2010AAS...21545104O')
        self.assertEquals(r.status_code, 302)
    
    
    def url_045(self, user=anonymous_user_classic):
        """
        (045) /favicon.ico freq=28792 (internal traffic: 0.51, orig_status=304)
        """
        r = user.get('/favicon.ico')
        self.assertEquals(r.status_code, 304)
    
    
    def url_046(self, user=anonymous_user_classic):
        """
        (046) /full/<4/5/4/0/16> freq=21402 (internal traffic: 0.92, orig_status=200)
        """
        r = user.get('/full/seri/JRASC/0103//0000066.000.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_047(self, user=anonymous_user_classic):
        """
        (047) /articles/abstracts/<4/5/23> freq=17626 (internal traffic: 0.89, orig_status=200)
        """
        r = user.get('/articles/abstracts/1976/ApJ../1976ApJ...203..297S.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_048(self, user=anonymous_user_classic):
        """
        (048) /cgi-bin/exec_myads2/all?<params> freq=13904 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/cgi-bin/exec_myads2/all?id=316154300&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 200)
    
    
    def url_049(self, user=anonymous_user_classic):
        """
        (049) /cgi-bin/basic_connect?<params> freq=13172 (internal traffic: 0.01, orig_status=302)
        """
        r = user.get('/cgi-bin/basic_connect?qsearch=Shankland%2C+p&amp;version=1')
        self.assertEquals(r.status_code, 302)
    
    
    def url_050(self, user=anonymous_user_classic):
        """
        (050) /physics_service.html freq=10911 (internal traffic: 0.63, orig_status=200)
        """
        r = user.get('/physics_service.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_051(self, user=anonymous_user_classic):
        """
        (051) /abs_doc/classic_form_analytics.js freq=10155 (internal traffic: 0.99, orig_status=304)
        """
        r = user.get('/abs_doc/classic_form_analytics.js')
        self.assertEquals(r.status_code, 304)
    
    
    def url_052(self, user=anonymous_user_classic):
        """
        (052) /cgi-bin/exec_myads2?<params> freq=9690 (internal traffic: 0.00, orig_status=200)
        """
        r = user.head('/cgi-bin/exec_myads2?id=364380276&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 200)
    
    
    def url_053(self, user=anonymous_user_classic):
        """
        (053) /abs/<9> freq=9634 (internal traffic: 0.79, orig_status=404)
        """
        r = user.get('/abs/undefined')
        self.assertEquals(r.status_code, 404)
    
    
    def url_054(self, user=anonymous_user_classic):
        """
        (054) /figs/ads_logo_medium_dark_trans_background.png freq=8416 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/figs/ads_logo_medium_dark_trans_background.png')
        self.assertEquals(r.status_code, 200)
    
    
    def url_055(self, user=anonymous_user_classic):
        """
        (055) /abs/<19> freq=8201 (internal traffic: 0.07, orig_status=404)
        """
        r = user.get('/abs/2019AIPC.2142m0005C')
        self.assertEquals(r.status_code, 404)
    
    
    def url_056(self, user=anonymous_user_classic):
        """
        (056) /abstract_service.html/legacy freq=7590 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/abstract_service.html/legacy')
        self.assertEquals(r.status_code, 200)
    
    
    def url_057(self, user=anonymous_user_classic):
        """
        (057) /bib_abs.html freq=6886 (internal traffic: 0.65, orig_status=200)
        """
        r = user.get('/bib_abs.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_058(self, user=anonymous_user_classic):
        """
        (058) /full/<19> freq=6722 (internal traffic: 0.71, orig_status=200)
        """
        r = user.head('/full/1959BAN....14..323V')
        self.assertEquals(r.status_code, 200)
    
    
    def url_059(self, user=anonymous_user_classic):
        """
        (059) /abstract_service.html/ freq=6545 (internal traffic: 0.04, orig_status=200)
        """
        r = user.get('/abstract_service.html/')
        self.assertEquals(r.status_code, 200)
    
    
    def url_060(self, user=anonymous_user_classic):
        """
        (060) /cgi-bin/abs_connect?<params> freq=6259 (internal traffic: 0.10, orig_status=200)
        """
        r = user.get('/cgi-bin/abs_connect?data_type=VOTABLE&DEC=60&RA=16&SR=.1')
        self.assertEquals(r.status_code, 200)
    
    
    def url_061(self, user=anonymous_user_classic):
        """
        (061) /cgi-bin/nph-abs_connect freq=5514 (internal traffic: 0.06, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-abs_connect')
        self.assertEquals(r.status_code, 200)
    
    
    def url_062(self, user=anonymous_user_classic):
        """
        (062) /apple-touch-icon.png freq=5345 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/apple-touch-icon.png')
        self.assertEquals(r.status_code, 404)
    
    
    def url_063(self, user=anonymous_user_classic):
        """
        (063) /full/<10/4/5/4/0/16> freq=5052 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/full/thumbnails/seri/IrAJ./0020//0000102,002.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_064(self, user=anonymous_user_classic):
        """
        (064) /cgi-bin/pref_set freq=4748 (internal traffic: 0.83, orig_status=302)
        """
        r = user.get('/cgi-bin/pref_set')
        self.assertEquals(r.status_code, 302)
    
    
    def url_065(self, user=anonymous_user_classic):
        """
        (065) /cgi-bin/nph-data_query?<params> freq=4642 (internal traffic: 0.64, orig_status=200)
        """
        r = user.head('/cgi-bin/nph-data_query?bibcode=1988JOSAB...5..243D&link_type=ARTICLE&db_key=PHY&high=')
        self.assertEquals(r.status_code, 200)
    
    
    def url_066(self, user=anonymous_user_classic):
        """
        (066) / freq=4555 (internal traffic: 0.08, orig_status=200)
        """
        r = user.head('/')
        self.assertEquals(r.status_code, 200)
    
    
    def url_067(self, user=anonymous_user_classic):
        """
        (067) /abs/<19/9/0> freq=4452 (internal traffic: 1.00, orig_status=404)
        """
        r = user.post('/abs/2003PhDT........62K/trackback/')
        self.assertEquals(r.status_code, 404)
    
    
    def url_068(self, user=anonymous_user_classic):
        """
        (068) /ads_browse.html freq=4422 (internal traffic: 0.77, orig_status=200)
        """
        r = user.get('/ads_browse.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_069(self, user=anonymous_user_classic):
        """
        (069) /apple-touch-icon-precomposed.png freq=4369 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/apple-touch-icon-precomposed.png')
        self.assertEquals(r.status_code, 404)
    
    
    def url_070(self, user=anonymous_user_classic):
        """
        (070) /full/<6/4/5/4/0/16> freq=4339 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/full/record/seri/IrAJ./0020//0000102,002.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_071(self, user=anonymous_user_classic):
        """
        (071) /abs/<28> freq=4333 (internal traffic: 0.08, orig_status=200)
        """
        r = user.get('/abs/1975tads.book.....R%E5%AF%86')
        self.assertEquals(r.status_code, 200)
    
    
    def url_072(self, user=anonymous_user_classic):
        """
        (072) /full/<3/4/5/4/0/16> freq=4312 (internal traffic: 0.98, orig_status=200)
        """
        r = user.get('/full/gif/seri/IrAJ./0020//0000102,002.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_073(self, user=anonymous_user_classic):
        """
        (073) /abs/<34> freq=4072 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/abs/1989STIA...9051377A%EF%BF%BD%C3%9C')
        self.assertEquals(r.status_code, 200)
    
    
    def url_074(self, user=anonymous_user_classic):
        """
        (074) /cgi-bin/nph-toc_query?<params> freq=4029 (internal traffic: 0.10, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-toc_query?journal=ApJ&volume=LATEST&data_type=RSS&db_key=AST')
        self.assertEquals(r.status_code, 200)
    
    
    def url_075(self, user=anonymous_user_classic):
        """
        (075) /favicon.ico freq=3915 (internal traffic: 0.00, orig_status=200)
        """
        r = user.head('/favicon.ico')
        self.assertEquals(r.status_code, 200)
    
    
    def url_076(self, user=anonymous_user_classic):
        """
        (076) /figs/dot.gif freq=3913 (internal traffic: 0.71, orig_status=304)
        """
        r = user.get('/figs/dot.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_077(self, user=anonymous_user_classic):
        """
        (077) /cgi-bin/bib_query?<params> freq=3912 (internal traffic: 0.01, orig_status=404)
        """
        r = user.get('/cgi-bin/bib_query?1991RC3.9.C...0000d')
        self.assertEquals(r.status_code, 404)
    
    
    def url_078(self, user=anonymous_user_classic):
        """
        (078) /cgi-bin/nph-manage_account freq=3728 (internal traffic: 0.98, orig_status=200)
        """
        r = user.post('/cgi-bin/nph-manage_account')
        self.assertEquals(r.status_code, 200)
    
    
    def url_079(self, user=anonymous_user_classic):
        """
        (079) /doi/<7/5/7> freq=3646 (internal traffic: 0.44, orig_status=200)
        """
        r = user.get('/doi/10.1093/mnras/stz2615')
        self.assertEquals(r.status_code, 200)
    
    
    def url_080(self, user=anonymous_user_classic):
        """
        (080) /abs/<23> freq=3631 (internal traffic: 0.32, orig_status=200)
        """
        r = user.get('/abs/1997A&amp;A...321..293S')
        self.assertEquals(r.status_code, 200)
    
    
    def url_081(self, user=anonymous_user_classic):
        """
        (081) /figs/myadslogo.gif freq=3484 (internal traffic: 0.01, orig_status=304)
        """
        r = user.get('/figs/myadslogo.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_082(self, user=anonymous_user_classic):
        """
        (082) /abs_doc/help_pages/art_service.html freq=3388 (internal traffic: 0.97, orig_status=404)
        """
        r = user.get('/abs_doc/help_pages/art_service.html')
        self.assertEquals(r.status_code, 404)
    
    
    def url_083(self, user=anonymous_user_classic):
        """
        (083) /default_service.html freq=3347 (internal traffic: 0.02, orig_status=200)
        """
        r = user.get('/default_service.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_084(self, user=anonymous_user_classic):
        """
        (084) /?<params> freq=3292 (internal traffic: 0.33, orig_status=200)
        """
        r = user.get('/?author=2')
        self.assertEquals(r.status_code, 200)
    
    
    def url_085(self, user=anonymous_user_classic):
        """
        (085) /figs/arxiv_logo.gif freq=3278 (internal traffic: 0.19, orig_status=200)
        """
        r = user.get('/figs/arxiv_logo.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_086(self, user=anonymous_user_classic):
        """
        (086) /figs/nasalogo.gif freq=3126 (internal traffic: 0.89, orig_status=304)
        """
        r = user.get('/figs/nasalogo.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_087(self, user=anonymous_user_classic):
        """
        (087) /figs/cfalogo.gif freq=3069 (internal traffic: 0.89, orig_status=304)
        """
        r = user.get('/figs/cfalogo.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_088(self, user=anonymous_user_classic):
        """
        (088) /abs_doc/help_pages/search.html freq=3044 (internal traffic: 0.53, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/search.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_089(self, user=anonymous_user_classic):
        """
        (089) /figs/newlogo_small.gif freq=3023 (internal traffic: 0.89, orig_status=304)
        """
        r = user.get('/figs/newlogo_small.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_090(self, user=anonymous_user_classic):
        """
        (090) /figs/adslogo.gif freq=2955 (internal traffic: 0.99, orig_status=304)
        """
        r = user.get('/figs/adslogo.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_091(self, user=anonymous_user_classic):
        """
        (091) /abs_doc/help_pages/images/adslogo.gif freq=2867 (internal traffic: 0.97, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/images/adslogo.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_092(self, user=anonymous_user_classic):
        """
        (092) /cgi-bin/basic_connect?<params> freq=2866 (internal traffic: 0.00, orig_status=200)
        """
        r = user.head('/cgi-bin/basic_connect?qsearch=10.1016/j.jaad.2015.07.028')
        self.assertEquals(r.status_code, 200)
    
    
    def url_093(self, user=anonymous_user_classic):
        """
        (093) /figs/newlogo.gif freq=2857 (internal traffic: 0.87, orig_status=304)
        """
        r = user.get('/figs/newlogo.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_094(self, user=anonymous_user_classic):
        """
        (094) /abs_doc/help_pages/images/dot.gif freq=2847 (internal traffic: 0.97, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/images/dot.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_095(self, user=anonymous_user_classic):
        """
        (095) /abs_doc/help_pages/images/goup.gif freq=2791 (internal traffic: 0.97, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/images/goup.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_096(self, user=anonymous_user_classic):
        """
        (096) /abs_doc/help_pages/images/right.gif freq=2767 (internal traffic: 0.97, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/images/right.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_097(self, user=anonymous_user_classic):
        """
        (097) /abs_doc/help_pages/images/left.gif freq=2663 (internal traffic: 0.97, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/images/left.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_098(self, user=anonymous_user_classic):
        """
        (098) /cgi-bin/insert_login/credentials freq=2647 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/cgi-bin/insert_login/credentials')
        self.assertEquals(r.status_code, 200)
    
    
    def url_099(self, user=anonymous_user_classic):
        """
        (099) /cgi-bin/iarticle_query?<params> freq=2639 (internal traffic: 0.12, orig_status=200)
        """
        r = user.get('/cgi-bin/iarticle_query?journal=AbbOO&volume=0001&type=SCREEN_THMB')
        self.assertEquals(r.status_code, 200)
    
    
    def url_100(self, user=anonymous_user_classic):
        """
        (100) /plus/mytag_js.php?<params> freq=2603 (internal traffic: 0.75, orig_status=404)
        """
        r = user.post('/plus/mytag_js.php?aid=511348')
        self.assertEquals(r.status_code, 404)
    
    
    def url_101(self, user=anonymous_user_classic):
        """
        (101) /abstract_service.html/legacy freq=2574 (internal traffic: 0.01, orig_status=302)
        """
        r = user.get('/abstract_service.html/legacy')
        self.assertEquals(r.status_code, 302)
    
    
    def url_102(self, user=anonymous_user_classic):
        """
        (102) /figs/addtomyyahoo.gif freq=2530 (internal traffic: 1.00, orig_status=304)
        """
        r = user.get('/figs/addtomyyahoo.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_103(self, user=anonymous_user_classic):
        """
        (103) /figs/xml.gif freq=2495 (internal traffic: 0.99, orig_status=304)
        """
        r = user.get('/figs/xml.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_104(self, user=anonymous_user_classic):
        """
        (104) /cgi-bin/exec_myads2/?<params> freq=2386 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/cgi-bin/exec_myads2/?id=303307024&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 200)
    
    
    def url_105(self, user=anonymous_user_classic):
        """
        (105) /full/<89> freq=2290 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/full/bibcode=2019APS..MARF66013F&data_type=PDF_HIGH&whole_paper=YES&type=PRINTER&filetype=.pdf')
        self.assertEquals(r.status_code, 404)
    
    
    def url_106(self, user=anonymous_user_classic):
        """
        (106) /cgi-bin/exec_myads2?<params> freq=2283 (internal traffic: 0.19, orig_status=304)
        """
        r = user.get('/cgi-bin/exec_myads2?id=342951612&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 304)
    
    
    def url_107(self, user=anonymous_user_classic):
        """
        (107) /cgi-bin/list_connect?<params> freq=2249 (internal traffic: 0.58, orig_status=200)
        """
        r = user.get('/cgi-bin/list_connect?version=1&aut_xct=YES&db_key=AST&aut_list=stone%2C+j')
        self.assertEquals(r.status_code, 200)
    
    
    def url_108(self, user=anonymous_user_classic):
        """
        (108) /basic_search.html freq=2223 (internal traffic: 0.48, orig_status=200)
        """
        r = user.get('/basic_search.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_109(self, user=anonymous_user_classic):
        """
        (109) /abs_doc/faq.html freq=2202 (internal traffic: 0.33, orig_status=200)
        """
        r = user.get('/abs_doc/faq.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_110(self, user=anonymous_user_classic):
        """
        (110) /full/<20> freq=2113 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/full/1977AJ.....82.1013L7')
        self.assertEquals(r.status_code, 200)
    
    
    def url_111(self, user=anonymous_user_classic):
        """
        (111) /figs/nasalogo_med.png freq=2052 (internal traffic: 1.00, orig_status=304)
        """
        r = user.get('/figs/nasalogo_med.png')
        self.assertEquals(r.status_code, 304)
    
    
    def url_112(self, user=anonymous_user_classic):
        """
        (112) /apple-touch-icon.png freq=1990 (internal traffic: 0.00, orig_status=404)
        """
        r = user.head('/apple-touch-icon.png')
        self.assertEquals(r.status_code, 404)
    
    
    def url_113(self, user=anonymous_user_classic):
        """
        (113) /apple-touch-icon-precomposed.png freq=1989 (internal traffic: 0.00, orig_status=404)
        """
        r = user.head('/apple-touch-icon-precomposed.png')
        self.assertEquals(r.status_code, 404)
    
    
    def url_114(self, user=anonymous_user_classic):
        """
        (114) /doi/<7/6> freq=1922 (internal traffic: 0.02, orig_status=302)
        """
        r = user.get('/doi/10.1086/176149')
        self.assertEquals(r.status_code, 302)
    
    
    def url_115(self, user=anonymous_user_classic):
        """
        (115) /abs/<16> freq=1863 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/abs/arXiv:1807.07702')
        self.assertEquals(r.status_code, 200)
    
    
    def url_116(self, user=anonymous_user_classic):
        """
        (116) /abs_doc/ads.css freq=1858 (internal traffic: 1.00, orig_status=304)
        """
        r = user.get('/abs_doc/ads.css')
        self.assertEquals(r.status_code, 304)
    
    
    def url_117(self, user=anonymous_user_classic):
        """
        (117) /abs/<18> freq=1841 (internal traffic: 0.22, orig_status=200)
        """
        r = user.get('/abs/1985EnTR........15')
        self.assertEquals(r.status_code, 200)
    
    
    def url_118(self, user=anonymous_user_classic):
        """
        (118) /figs/si_logo.gif freq=1800 (internal traffic: 1.00, orig_status=304)
        """
        r = user.get('/figs/si_logo.gif')
        self.assertEquals(r.status_code, 304)
    
    
    def url_119(self, user=anonymous_user_classic):
        """
        (119) /cgi-bin/bib_query?<params> freq=1738 (internal traffic: 0.03, orig_status=200)
        """
        r = user.head('/cgi-bin/bib_query?2000ApJ...535...30J')
        self.assertEquals(r.status_code, 200)
    
    
    def url_120(self, user=anonymous_user_classic):
        """
        (120) /cgi-bin/access_denied freq=1690 (internal traffic: 0.01, orig_status=403)
        """
        r = user.head('/cgi-bin/access_denied')
        self.assertEquals(r.status_code, 403)
    
    
    def url_121(self, user=anonymous_user_classic):
        """
        (121) /robots.txt freq=1657 (internal traffic: 0.03, orig_status=200)
        """
        r = user.get('/robots.txt')
        self.assertEquals(r.status_code, 200)
    
    
    def url_122(self, user=anonymous_user_classic):
        """
        (122) /cgi-bin/exec_myads2/all?<params> freq=1582 (internal traffic: 0.00, orig_status=304)
        """
        r = user.get('/cgi-bin/exec_myads2/all?id=358139204&db_ley=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 304)
    
    
    def url_123(self, user=anonymous_user_classic):
        """
        (123) /doi/<7/24> freq=1528 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/doi/10.1111/j.1365-2966.2012.21965.x')
        self.assertEquals(r.status_code, 200)
    
    
    def url_124(self, user=anonymous_user_classic):
        """
        (124) /cgi-bin/article_queryform?<params> freq=1523 (internal traffic: 0.73, orig_status=200)
        """
        r = user.get('/cgi-bin/article_queryform?bibcode=1971ApJ...165..181W&letter=0&db_key=AST&page=181&plate=&fiche=&cover=&pagetype=.')
        self.assertEquals(r.status_code, 200)
    
    
    def url_125(self, user=anonymous_user_classic):
        """
        (125) /cgi-bin/nph-basic_connect freq=1491 (internal traffic: 0.10, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-basic_connect')
        self.assertEquals(r.status_code, 200)
    
    
    def url_126(self, user=anonymous_user_classic):
        """
        (126) /cgi-bin/nph-iarticle_query?<params> freq=1455 (internal traffic: 0.47, orig_status=200)
        """
        r = user.head('/cgi-bin/nph-iarticle_query?1978ApJ...225..357S&data_type=PDF_HIGH&whole_paper=YES&type=PRINTER&filetype=.pdf')
        self.assertEquals(r.status_code, 200)
    
    
    def url_127(self, user=anonymous_user_classic):
        """
        (127) /abs_doc/help_pages/results.html freq=1402 (internal traffic: 0.39, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/results.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_128(self, user=anonymous_user_classic):
        """
        (128) /cgi-bin/nph-abs_connect?<params> freq=1400 (internal traffic: 0.16, orig_status=200)
        """
        r = user.head('/cgi-bin/nph-abs_connect?db_key=AST&db_key=PHY&sim_query=YES&ned_query=YES&aut_xct=YES&aut_logic=OR&obj_logic=OR&author=Douglas%2C+A.+Vibert%0D%0ADouglas%2C+A.+V.&object=&start_mon=&start_year=&end_mon=&end_year=1982')
        self.assertEquals(r.status_code, 200)
    
    
    def url_129(self, user=anonymous_user_classic):
        """
        (129) /abs/<20> freq=1270 (internal traffic: 0.09, orig_status=404)
        """
        r = user.get('/abs/2002A&A...349...415T')
        self.assertEquals(r.status_code, 404)
    
    
    def url_130(self, user=anonymous_user_classic):
        """
        (130) /abs_doc/list_funcs.js freq=1256 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/abs_doc/list_funcs.js')
        self.assertEquals(r.status_code, 200)
    
    
    def url_131(self, user=anonymous_user_classic):
        """
        (131) /cgi-bin/myads2_set freq=1251 (internal traffic: 1.00, orig_status=200)
        """
        r = user.post('/cgi-bin/myads2_set')
        self.assertEquals(r.status_code, 200)
    
    
    def url_132(self, user=anonymous_user_classic):
        """
        (132) /cgi-bin/nph-bib_query?<params> freq=1215 (internal traffic: 0.04, orig_status=200)
        """
        r = user.head('/cgi-bin/nph-bib_query?bibcode=1962IAUS...14..419S&db_key=AST&high=3e6fbfd69f01910')
        self.assertEquals(r.status_code, 200)
    
    
    def url_133(self, user=anonymous_user_classic):
        """
        (133) /doi/<7/17> freq=1195 (internal traffic: 0.18, orig_status=200)
        """
        r = user.get('/doi/10.1038/s41550-019-0892-y')
        self.assertEquals(r.status_code, 200)
    
    
    def url_134(self, user=anonymous_user_classic):
        """
        (134) /cgi-bin/myads2_set?<params> freq=1187 (internal traffic: 0.11, orig_status=302)
        """
        r = user.get('/cgi-bin/myads2_set?')
        self.assertEquals(r.status_code, 302)
    
    
    def url_135(self, user=anonymous_user_classic):
        """
        (135) /abs_doc/help_pages/taggedformat.html freq=1187 (internal traffic: 0.10, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/taggedformat.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_136(self, user=anonymous_user_classic):
        """
        (136) /myads/ freq=1170 (internal traffic: 0.38, orig_status=200)
        """
        r = user.get('/myADS/')
        self.assertEquals(r.status_code, 200)
    
    
    def url_137(self, user=anonymous_user_classic):
        """
        (137) /myads freq=1159 (internal traffic: 0.36, orig_status=301)
        """
        r = user.get('/myADS')
        self.assertEquals(r.status_code, 301)
    
    
    def url_138(self, user=anonymous_user_classic):
        """
        (138) /user.php?<params> freq=1145 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/user.php?act=login')
        self.assertEquals(r.status_code, 404)
    
    
    def url_139(self, user=anonymous_user_classic):
        """
        (139) /proxy5/check.php freq=1133 (internal traffic: 0.00, orig_status=404)
        """
        r = user.post('/proxy5/check.php')
        self.assertEquals(r.status_code, 404)
    
    
    def url_140(self, user=anonymous_user_classic):
        """
        (140) /preprint_service.html freq=1132 (internal traffic: 0.70, orig_status=200)
        """
        r = user.get('/preprint_service.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_141(self, user=anonymous_user_classic):
        """
        (141) /cgi-bin/bib_query?<params> freq=1099 (internal traffic: 0.01, orig_status=302)
        """
        r = user.get('/cgi-bin/bib_query?arXiv%3A1706.08555=')
        self.assertEquals(r.status_code, 302)
    
    
    def url_142(self, user=anonymous_user_classic):
        """
        (142) /cgi-bin/pref_set?<params> freq=1055 (internal traffic: 0.93, orig_status=302)
        """
        r = user.get('/cgi-bin/pref_set?2&abs_proxy=http://adsabs.harvard.edu')
        self.assertEquals(r.status_code, 302)
    
    
    def url_143(self, user=anonymous_user_classic):
        """
        (143) /xmlrpc.php?<params> freq=1040 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/xmlrpc.php?rsd')
        self.assertEquals(r.status_code, 404)
    
    
    def url_144(self, user=anonymous_user_classic):
        """
        (144) /cgi-bin/exec_myads2?<params> freq=1012 (internal traffic: 0.00, orig_status=304)
        """
        r = user.head('/cgi-bin/exec_myads2?id=364380276&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 304)
    
    
    def url_145(self, user=anonymous_user_classic):
        """
        (145) /abs/<23> freq=1002 (internal traffic: 0.02, orig_status=302)
        """
        r = user.get('/abs/2000A+ACY-A...355L..27H')
        self.assertEquals(r.status_code, 302)
    
    
    def url_146(self, user=anonymous_user_classic):
        """
        (146) /abs_doc/help_pages/data.html freq=968 (internal traffic: 0.21, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/data.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_147(self, user=anonymous_user_classic):
        """
        (147) /abs_doc/site_map/ freq=966 (internal traffic: 0.60, orig_status=200)
        """
        r = user.get('/abs_doc/site_map/')
        self.assertEquals(r.status_code, 200)
    
    
    def url_148(self, user=anonymous_user_classic):
        """
        (148) /cms/wp-includes/wlwmanifest.xml freq=957 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/cms/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
    
    
    def url_149(self, user=anonymous_user_classic):
        """
        (149) /site/wp-includes/wlwmanifest.xml freq=956 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/site/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
    
    
    def url_150(self, user=anonymous_user_classic):
        """
        (150) /wordpress/wp-includes/wlwmanifest.xml freq=956 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/wordpress/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
    
    
    def url_151(self, user=anonymous_user_classic):
        """
        (151) /abs_doc/journal_abbr.html freq=954 (internal traffic: 0.82, orig_status=200)
        """
        r = user.get('/abs_doc/journal_abbr.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_152(self, user=anonymous_user_classic):
        """
        (152) /blog/wp-includes/wlwmanifest.xml freq=953 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/blog/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
    
    
    def url_153(self, user=anonymous_user_classic):
        """
        (153) /wp/wp-includes/wlwmanifest.xml freq=953 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/wp/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
    
    
    def url_154(self, user=anonymous_user_classic):
        """
        (154) /admin_aspcms/_system/aspcms_sitesetting.asp freq=951 (internal traffic: 0.67, orig_status=404)
        """
        r = user.post('/admin_aspcms/_system/AspCms_SiteSetting.asp')
        self.assertEquals(r.status_code, 404)
    
    
    def url_155(self, user=anonymous_user_classic):
        """
        (155) /full/<19/16> freq=950 (internal traffic: 0.45, orig_status=200)
        """    
        r = user.head('/full/2003JAHH....6...46S/0000046.000.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_156(self, user=anonymous_user_classic):
        """
        (156) /wp-includes/wlwmanifest.xml freq=949 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
    
    
    def url_157(self, user=anonymous_user_classic):
        """
        (157) /cgi-bin/nph-journal_query?<params> freq=930 (internal traffic: 0.79, orig_status=200)
        """
        r = user.get('/cgi-bin/nph-journal_query?journal=2003cigs.book.....F&page=1&type=SCREEN_THMB')
        self.assertEquals(r.status_code, 200)
    
    
    def url_158(self, user=anonymous_user_classic):
        """
        (158) /full/<4/5/4/16> freq=914 (internal traffic: 0.18, orig_status=200)
        """
        r = user.get('/full/seri/QJRAS/0026/0000151.000.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_159(self, user=anonymous_user_classic):
        """
        (159) /cgi-bin/manage_account freq=898 (internal traffic: 0.02, orig_status=200)
        """
        r = user.get('/cgi-bin/manage_account')
        self.assertEquals(r.status_code, 200)
    
    
    def url_160(self, user=anonymous_user_classic):
        """
        (160) /user_feedback.html freq=860 (internal traffic: 0.61, orig_status=200)
        """
        r = user.get('/user_feedback.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_161(self, user=anonymous_user_classic):
        """
        (161) /cgi-bin/manage_account/credentials?<params> freq=836 (internal traffic: 0.00, orig_status=200)
        """
        r = user.post('/cgi-bin/manage_account/credentials?man_email=apal%40szofi.net&man_cmd=elogin&man_passwd=qqriq123')
        self.assertEquals(r.status_code, 200)
    
    
    def url_162(self, user=anonymous_user_classic):
        """
        (162) /abs_doc/help_pages/overview.html freq=799 (internal traffic: 0.21, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/overview.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_163(self, user=anonymous_user_classic):
        """
        (163) /doi/<7/5/6> freq=795 (internal traffic: 0.02, orig_status=200)
        """
        r = user.get('/doi/10.1093/mnras/stz514')
        self.assertEquals(r.status_code, 200)
    
    
    def url_164(self, user=anonymous_user_classic):
        """
        (164) /cgi-bin/xauthor_queryform?<params> freq=775 (internal traffic: 0.75, orig_status=200)
        """
        r = user.get('/cgi-bin/xauthor_queryform?db_key=AST')
        self.assertEquals(r.status_code, 200)
    
    
    def url_165(self, user=anonymous_user_classic):
        """
        (165) /cgi-bin/list_connect?<params> freq=774 (internal traffic: 1.00, orig_status=302)
        """
        r = user.get('/cgi-bin/list_connect?aut_list=A*&aut_list_ln=YES&db_key=PHY')
        self.assertEquals(r.status_code, 302)
    
    
    def url_166(self, user=anonymous_user_classic):
        """
        (166) /abs/<20> freq=768 (internal traffic: 0.07, orig_status=302)
        """
        r = user.get('/abs/2017NatSR...741548O.')
        self.assertEquals(r.status_code, 302)
    
    
    def url_167(self, user=anonymous_user_classic):
        """
        (167) /abs_doc/help_pages/ freq=768 (internal traffic: 0.55, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/')
        self.assertEquals(r.status_code, 200)
    
    
    def url_168(self, user=anonymous_user_classic):
        """
        (168) /full/<19> freq=746 (internal traffic: 0.01, orig_status=302)
        """
        r = user.get('/full/1992ASPC...28..123C')
        self.assertEquals(r.status_code, 302)
    
    
    def url_169(self, user=anonymous_user_classic):
        """
        (169) /mirrors.html freq=722 (internal traffic: 0.34, orig_status=200)
        """
        r = user.get('/mirrors.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_170(self, user=anonymous_user_classic):
        """
        (170) /config/aspcms_config.asp freq=711 (internal traffic: 0.75, orig_status=404)
        """
        r = user.post('/config/AspCms_Config.asp')
        self.assertEquals(r.status_code, 404)
    
    
    def url_171(self, user=anonymous_user_classic):
        """
        (171) /abs_doc/journals2.html freq=683 (internal traffic: 0.25, orig_status=200)
        """
        r = user.get('/abs_doc/journals2.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_172(self, user=anonymous_user_classic):
        """
        (172) /cgi-bin/get_file?<params> freq=683 (internal traffic: 0.53, orig_status=200)
        """
        r = user.get('/cgi-bin/get_file?pdfs/SPAW./1915/1915SPAW.......844E.pdf')
        self.assertEquals(r.status_code, 200)
    
    
    def url_173(self, user=anonymous_user_classic):
        """
        (173) /doi/<19> freq=659 (internal traffic: 0.01, orig_status=200)
        """
        r = user.get('/doi/2016PhDT........49B')
        self.assertEquals(r.status_code, 200)
    
    
    def url_174(self, user=anonymous_user_classic):
        """
        (174) /full/<3/19/25> freq=659 (internal traffic: 1.00, orig_status=200)
        """
        r = user.get('/full/gif/1983JHA....14..137V/0000137.000.html?high=478aa91ccd09202')
        self.assertEquals(r.status_code, 200)
    
    
    def url_175(self, user=anonymous_user_classic):
        """
        (175) /utility/convert/data/config.inc.php freq=652 (internal traffic: 0.66, orig_status=404)
        """
        r = user.post('/utility/convert/data/config.inc.php')
        self.assertEquals(r.status_code, 404)
    
    
    def url_176(self, user=anonymous_user_classic):
        """
        (176) /figs/newlogo.gif freq=650 (internal traffic: 0.76, orig_status=206)
        """
        r = user.get('/figs/newlogo.gif')
        self.assertEquals(r.status_code, 206)
    
    
    def url_177(self, user=anonymous_user_classic):
        """
        (177) /abs_doc/refereed.html freq=640 (internal traffic: 0.38, orig_status=200)
        """
        r = user.get('/abs_doc/refereed.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_178(self, user=anonymous_user_classic):
        """
        (178) /article_service.html freq=629 (internal traffic: 0.54, orig_status=200)
        """
        r = user.get('/article_service.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_179(self, user=anonymous_user_classic):
        """
        (179) /full/<6/4/5/4/24> freq=625 (internal traffic: 0.72, orig_status=200)
        """
        r = user.get('/full/record/seri/Astr./0007/1970Astr....7..154D.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_180(self, user=anonymous_user_classic):
        """
        (180) /index.php?<params> freq=605 (internal traffic: 0.69, orig_status=404)
        """
        r = user.get('/index.php?c=api&m=data2&auth=50ce0d2401ce4802751739552c8e4467&param=update_avatar&file=data:image/php;base64,eGJzaGVsbCUzQyUzRnBocCUwQSUyNHN0JTIwJTNEJTIwQGNyZWF0ZV9mdW5jdGlvbiUyOCUyNyUyNyUyQyUyMCUyNF9QT1NUJTVCJTI3aHhxOTkxMjE3JTI3JTVEJTI5JTNCJTBBJTI0c3QlMjglMjklM0I=')
        self.assertEquals(r.status_code, 404)
    
    
    def url_181(self, user=anonymous_user_classic):
        """
        (181) /doi/<7/5/9> freq=597 (internal traffic: 0.00, orig_status=200)
        """
        r = user.get('/doi/10.1093/mnras/167.1.31P')
        self.assertEquals(r.status_code, 200)
    
    
    def url_182(self, user=anonymous_user_classic):
        """
        (182) /abs_doc/help_pages/art_retrieve.html freq=591 (internal traffic: 0.39, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/art_retrieve.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_183(self, user=anonymous_user_classic):
        """
        (183) /abstract_service.html?<params> freq=583 (internal traffic: 0.58, orig_status=500)
        """
        r = user.get('/abstract_service.html?nosetcookie=1')
        self.assertEquals(r.status_code, 500)
    
    
    def url_184(self, user=anonymous_user_classic):
        """
        (184) /index.html freq=579 (internal traffic: 0.13, orig_status=200)
        """
        r = user.get('/index.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_185(self, user=anonymous_user_classic):
        """
        (185) /plus/90sec.php freq=576 (internal traffic: 0.67, orig_status=404)
        """
        r = user.post('/plus/90sec.php')
        self.assertEquals(r.status_code, 404)
    
    
    def url_186(self, user=anonymous_user_classic):
        """
        (186) /doi/<7/6> freq=563 (internal traffic: 0.34, orig_status=200)
        """
        r = user.head('/doi/10.1086/161749')
        self.assertEquals(r.status_code, 200)
    
    
    def url_187(self, user=anonymous_user_classic):
        """
        (187) /doi/<7/4/6> freq=561 (internal traffic: 0.38, orig_status=200)
        """
        r = user.get('/doi/10.1093/pasj/psx137')
        self.assertEquals(r.status_code, 200)
    
    
    def url_188(self, user=anonymous_user_classic):
        """
        (188) /journals_service.html freq=558 (internal traffic: 0.32, orig_status=200)
        """
        r = user.get('/journals_service.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_189(self, user=anonymous_user_classic):
        """
        (189) /abs_doc/site_map/map.html freq=556 (internal traffic: 0.97, orig_status=200)
        """
        r = user.get('/abs_doc/site_map/map.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_190(self, user=anonymous_user_classic):
        """
        (190) /abs_doc/site_map/images/question.gif freq=550 (internal traffic: 1.00, orig_status=200)
        """
        r = user.get('/abs_doc/site_map/images/question.gif')
        self.assertEquals(r.status_code, 200)
    
    
    def url_191(self, user=anonymous_user_classic):
        """
        (191) /doi/<7/17> freq=549 (internal traffic: 0.00, orig_status=404)
        """
        r = user.get('/doi/10.1017/S0251107X00007136')
        self.assertEquals(r.status_code, 404)
    
    
    def url_192(self, user=anonymous_user_classic):
        """
        (192) /cgi-bin/dexterstart.pl?<params> freq=544 (internal traffic: 0.47, orig_status=200)
        """
        r = user.get('/cgi-bin/dexterstart.pl?bibcode=1995ApJS...96..371N&imagepath=seri/ApJS./0096//600/0000399.000&db_key=AST&page=399&bits=4')
        self.assertEquals(r.status_code, 200)
    
    
    def url_193(self, user=anonymous_user_classic):
        """
        (193) /fdgq.php freq=538 (internal traffic: 0.64, orig_status=404)
        """
        r = user.post('/fdgq.php')
        self.assertEquals(r.status_code, 404)
    
    
    def url_194(self, user=anonymous_user_classic):
        """
        (194) /abs_doc/site_map/desc.html freq=532 (internal traffic: 0.99, orig_status=200)
        """
        r = user.get('/abs_doc/site_map/desc.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_195(self, user=anonymous_user_classic):
        """
        (195) /abs_doc/help_pages/citations.html freq=523 (internal traffic: 0.56, orig_status=200)
        """
        r = user.get('/abs_doc/help_pages/citations.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_196(self, user=anonymous_user_classic):
        """
        (196) /abstract_service.html freq=519 (internal traffic: 0.27, orig_status=200)
        """
        r = user.head('/abstract_service.html')
        self.assertEquals(r.status_code, 200)
    
    
    def url_197(self, user=anonymous_user_classic):
        """
        (197) /abs... freq=516 (internal traffic: 1.00, orig_status=404)
        """
        r = user.get('/abs...')
        self.assertEquals(r.status_code, 404)
    
    
    def url_198(self, user=anonymous_user_classic):
        """
        (198) /plus/mytag_js.php?<params> freq=509 (internal traffic: 0.67, orig_status=404)
        """
        r = user.get('/plus/mytag_js.php?dopost=saveedit&arrs1%5B%5D=99&arrs1%5B%5D=102&arrs1%5B%5D=103&arrs1%5B%5D=95&arrs1%5B%5D=100&arrs1%5B%5D=98&arrs1%5B%5D=112&arrs1%5B%5D=114&arrs1%5B%5D=101&arrs1%5B%5D=102&arrs1%5B%5D=105&arrs1%5B%5D=120&arrs2%5B%5D=109&arrs2%5B%5D=121&arrs2%5B%5D=116&arrs2%5B%5D=97&arrs2%5B%5D=103&arrs2%5B%5D=96&arrs2%5B%5D=32&arrs2%5B%5D=40&arrs2%5B%5D=97&arrs2%5B%5D=105&arrs2%5B%5D=100&arrs2%5B%5D=44&arrs2%5B%5D=110&arrs2%5B%5D=111&arrs2%5B%5D=114&arrs2%5B%5D=109&arrs2%5B%5D=98&arrs2%5B%5D=111&arrs2%5B%5D=100&arrs2%5B%5D=121&arrs2%5B%5D=41&arrs2%5B%5D=32&arrs2%5B%5D=86&arrs2%5B%5D=65&arrs2%5B%5D=76&arrs2%5B%5D=85&arrs2%5B%5D=69&arrs2%5B%5D=83&arrs2%5B%5D=40&arrs2%5B%5D=57&arrs2%5B%5D=48&arrs2%5B%5D=57&arrs2%5B%5D=48&arrs2%5B%5D=44&arrs2%5B%5D=39&arrs2%5B%5D=60&arrs2%5B%5D=63&arrs2%5B%5D=112&arrs2%5B%5D=104&arrs2%5B%5D=112&arrs2%5B%5D=32&arrs2%5B%5D=101&arrs2%5B%5D=99&arrs2%5B%5D=104&arrs2%5B%5D=111&arrs2%5B%5D=32&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=100&arrs2%5B%5D=101&arrs2%5B%5D=100&arrs2%5B%5D=101&arrs2%5B%5D=99&arrs2%5B%5D=109&arrs2%5B%5D=115&arrs2%5B%5D=32&arrs2%5B%5D=53&arrs2%5B%5D=46&arrs2%5B%5D=55&arrs2%5B%5D=32&arrs2%5B%5D=48&arrs2%5B%5D=100&arrs2%5B%5D=97&arrs2%5B%5D=121&arrs2%5B%5D=60&arrs2%5B%5D=98&arrs2%5B%5D=114&arrs2%5B%5D=62&arrs2%5B%5D=103&arrs2%5B%5D=117&arrs2%5B%5D=105&arrs2%5B%5D=103&arrs2%5B%5D=101&arrs2%5B%5D=44&arrs2%5B%5D=32&arrs2%5B%5D=57&arrs2%5B%5D=48&arrs2%5B%5D=115&arrs2%5B%5D=101&arrs2%5B%5D=99&arrs2%5B%5D=46&arrs2%5B%5D=111&arrs2%5B%5D=114&arrs2%5B%5D=103&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=59&arrs2%5B%5D=64&arrs2%5B%5D=112&arrs2%5B%5D=114&arrs2%5B%5D=101&arrs2%5B%5D=103&arrs2%5B%5D=95&arrs2%5B%5D=114&arrs2%5B%5D=101&arrs2%5B%5D=112&arrs2%5B%5D=108&arrs2%5B%5D=97&arrs2%5B%5D=99&arrs2%5B%5D=101&arrs2%5B%5D=40&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=47&arrs2%5B%5D=91&arrs2%5B%5D=99&arrs2%5B%5D=111&arrs2%5B%5D=112&arrs2%5B%5D=121&arrs2%5B%5D=114&arrs2%5B%5D=105&arrs2%5B%5D=103&arrs2%5B%5D=104&arrs2%5B%5D=116&arrs2%5B%5D=93&arrs2%5B%5D=47&arrs2%5B%5D=101&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=44&arrs2%5B%5D=36&arrs2%5B%5D=95&arrs2%5B%5D=82&arrs2%5B%5D=69&arrs2%5B%5D=81&arrs2%5B%5D=85&arrs2%5B%5D=69&arrs2%5B%5D=83&arrs2%5B%5D=84&arrs2%5B%5D=91&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=103&arrs2%5B%5D=117&arrs2%5B%5D=105&arrs2%5B%5D=103&arrs2%5B%5D=101&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=93&arrs2%5B%5D=44&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=101&arrs2%5B%5D=114&arrs2%5B%5D=114&arrs2%5B%5D=111&arrs2%5B%5D=114&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=41&arrs2%5B%5D=59&arrs2%5B%5D=63&arrs2%5B%5D=62&arrs2%5B%5D=39&arrs2%5B%5D=41&arrs2%5B%5D=59&arrs2%5B%5D=0')
        self.assertEquals(r.status_code, 404)
    
if __name__ == '__main__':
    unittest.main()