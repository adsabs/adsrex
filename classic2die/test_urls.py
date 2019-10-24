from classic2die.user_roles import anonymous_user_classic, authenticated_user_classic
import unittest
    
bibcodes = ['1993CoPhC..74..239H','1994GPC.....9...69H']

class TestPattenrs(unittest.TestCase):
    
    def test_anonymous_user(self): 
        self.check_urls(user=anonymous_user_classic)
    
    def test_authenticated_user(self):
        self.check_urls(user=authenticated_user_classic)
        
    def check_urls(self, user=anonymous_user_classic):
        # it makes no difference if those are accessed by authenticated user
        # or anonymous user
        
        
        # (  0) /cgi-bin/t2png?<params> freq=11235128 (internal traffic: 1.00, orig_status=200)
        r = user.get('/cgi-bin/t2png?bg=%23FFFFFF&/seri/NASCP/3111/200/0000103.000&db_key=AST&bits=3&scale=8&filetype=.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  1) /abs/<19> freq=3027798 (internal traffic: 0.12, orig_status=200)
        r = user.get('/abs/1998SPIE.3368..392B')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  2) /favicon.ico freq=1860777 (internal traffic: 0.68, orig_status=200)
        r = user.get('/favicon.ico')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  3) /full/<3/19/16> freq=1149235 (internal traffic: 0.99, orig_status=200)
        r = user.get('/full/gif/1988ApJ...329L..57T/L000057.000.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  4) /cgi-bin/nph-data_query?<params> freq=955869 (internal traffic: 0.71, orig_status=200)
        r = user.get('/cgi-bin/nph-data_query?bibcode=2012ApJ...760...34F&db_key=AST&link_type=ARTICLE')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  5) /cgi-bin/nph-abs_connect?<params> freq=729533 (internal traffic: 0.77, orig_status=200)
        r = user.get('/cgi-bin/nph-abs_connect?qsearch=&bibcode=0803983468&start_nr=0&nr_to_return=30&sort=SCORE&data_type=XML&version=1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  6) /full/<10/4/5/4/0/24> freq=724223 (internal traffic: 0.99, orig_status=200)
        r = user.get('/full/thumbnails/seri/ApJ../0329//1988ApJ...329L..57T.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  7) /full/<6/4/5/4/0/24> freq=723631 (internal traffic: 0.99, orig_status=200)
        r = user.get('/full/record/seri/ApJ../0329//1988ApJ...329L..57T.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  8) /full/<19> freq=479145 (internal traffic: 0.05, orig_status=200)
        r = user.get('/full/1995ESASP.371...79M')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (  9) /doi/<7/6> freq=387419 (internal traffic: 0.02, orig_status=200)
        r = user.get('/doi/10.1086/177092')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 10) /full/<19/16> freq=370508 (internal traffic: 0.97, orig_status=200)
        r = user.get('/full/1951C&T....67....1B/0000008.000.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 11) /abstract_service.html freq=319857 (internal traffic: 0.15, orig_status=200)
        r = user.get('/abstract_service.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 12) /cgi-bin/nph-iarticle_query?<params> freq=317369 (internal traffic: 0.81, orig_status=200)
        r = user.get('/cgi-bin/nph-iarticle_query?1951C%26T....67....1B&defaultprint=YES&page_ind=6&filetype=.pdf')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 13) /cgi-bin/nph-ref_query?<params> freq=310869 (internal traffic: 0.32, orig_status=200)
        r = user.get('/cgi-bin/nph-ref_query?bibcode=2012PhPl...19h2902W&amp;refs=CITATIONS&amp;db_key=PHY')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 14) /cgi-bin/t2png?<params> freq=238054 (internal traffic: 1.00, orig_status=304)
        r = user.get('/cgi-bin/t2png?bg=%23FFFFFF&/conf/foap./2007/200/0000579.000&db_key=AST&bits=3&scale=8&filetype=.jpg')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 15) / freq=225000 (internal traffic: 0.14, orig_status=200)
        r = user.get('/')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 16) /cgi-bin/basic_connect?<params> freq=163385 (internal traffic: 0.59, orig_status=200)
        r = user.get('/cgi-bin/basic_connect?qsearch=Dr+James+Webb&version=1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 17) /figs/newlogo.gif freq=135019 (internal traffic: 0.85, orig_status=200)
        r = user.get('/figs/newlogo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 18) /abs_doc/classic_form_analytics.js freq=122442 (internal traffic: 0.99, orig_status=200)
        r = user.get('/abs_doc/classic_form_analytics.js')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 19) /figs/dot.gif freq=108436 (internal traffic: 0.87, orig_status=200)
        r = user.get('/figs/dot.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 20) /figs/newlogo_small.gif freq=104679 (internal traffic: 0.87, orig_status=200)
        r = user.get('/figs/newlogo_small.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 21) /pdf<0/19> freq=103256 (internal traffic: 0.04, orig_status=200)
        r = user.get('/pdf/1990ApJ...359..267K')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 22) /figs/cfalogo.gif freq=103079 (internal traffic: 0.88, orig_status=200)
        r = user.get('/figs/cfalogo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 23) /figs/nasalogo.gif freq=102252 (internal traffic: 0.88, orig_status=200)
        r = user.get('/figs/nasalogo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 24) /cgi-bin/nph-ref_history?<params> freq=87250 (internal traffic: 0.91, orig_status=200)
        r = user.get('/cgi-bin/nph-ref_history?refs=AR&bibcode=2019arXiv190900340K')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 25) /abs/<19> freq=81913 (internal traffic: 0.14, orig_status=200)
        r = user.head('/abs/2019A&A...622A.193A')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 26) /cgi-bin/nph-manage_account?<params> freq=80016 (internal traffic: 0.40, orig_status=200)
        r = user.get('/cgi-bin/nph-manage_account?man_cmd=login&man_url=http://adsabs.harvard.edu/cgi-bin/nph-manage%5faccount%3fman%5fcmd%3dlogin%26man%5furl%3dhttp%3a//adsabs.harvard.edu/abs/2017Sci...357..687T')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 27) /cgi-bin/access_denied freq=78455 (internal traffic: 0.53, orig_status=403)
        r = user.get('/cgi-bin/access_denied')
        self.assertEquals(r.status_code, 403)
        
        
        
        # ( 28) /cgi-bin/author_form?<params> freq=78371 (internal traffic: 0.73, orig_status=200)
        r = user.get('/cgi-bin/author_form?author=Mattor,+N&fullauthor=Mattor,%20Nathan&charset=UTF-8&db_key=PHY')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 29) /cgi-bin/nph-bib_query?<params> freq=75411 (internal traffic: 0.68, orig_status=200)
        r = user.get('/cgi-bin/nph-bib_query?bibcode=2019arXiv190502773B&data_type=BIBTEX&db_key=PRE&nocookieset=1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 30) /cgi-bin/nph-abs_connect freq=70251 (internal traffic: 0.96, orig_status=200)
        r = user.post('/cgi-bin/nph-abs_connect')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 31) /figs/adslogo.gif freq=67185 (internal traffic: 0.99, orig_status=200)
        r = user.get('/figs/adslogo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 32) /ads_abstracts.html freq=57286 (internal traffic: 0.78, orig_status=200)
        r = user.get('/ads_abstracts.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 33) /cgi-bin/bib_query?<params> freq=49817 (internal traffic: 0.11, orig_status=200)
        r = user.get('/cgi-bin/bib_query?arXiv:1511.06066')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 34) /figs/xml.gif freq=48349 (internal traffic: 0.99, orig_status=200)
        r = user.get('/figs/xml.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 35) * freq=47740 (internal traffic: 0.00, orig_status=200)
        r = user.options('*')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 36) /cgi-bin/nph-basic_connect?<params> freq=47386 (internal traffic: 0.06, orig_status=200)
        r = user.get('/cgi-bin/nph-basic_connect?qsearch=10%2E1021%2Facs%2Ejcim%2E9b00620&start_nr=0&nr_to_return=30&sort=SCORE&data_type=XML&version=1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 37) /cgi-bin/nph-basic_connect freq=44468 (internal traffic: 1.00, orig_status=200)
        r = user.post('/cgi-bin/nph-basic_connect')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 38) /figs/addtomyyahoo.gif freq=44265 (internal traffic: 0.99, orig_status=200)
        r = user.get('/figs/addtomyyahoo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 39) /cgi-bin/exec_myads2?<params> freq=38624 (internal traffic: 0.06, orig_status=200)
        r = user.get('/cgi-bin/exec_myads2?id=372349790&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 40) /figs/nasalogo_med.png freq=37684 (internal traffic: 1.00, orig_status=200)
        r = user.get('/figs/nasalogo_med.png')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 41) /figs/si_logo.gif freq=37550 (internal traffic: 1.00, orig_status=200)
        r = user.get('/figs/si_logo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 42) /abs_doc/ads.css freq=36660 (internal traffic: 1.00, orig_status=200)
        r = user.get('/abs_doc/ads.css')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 43) /figs/myadslogo.gif freq=33025 (internal traffic: 0.02, orig_status=200)
        r = user.get('/figs/myadslogo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 44) /abs/<19> freq=29979 (internal traffic: 0.01, orig_status=302)
        r = user.get('/abs/2010AAS...21545104O')
        self.assertEquals(r.status_code, 302)
        
        
        
        # ( 45) /favicon.ico freq=28792 (internal traffic: 0.51, orig_status=304)
        r = user.get('/favicon.ico')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 46) /full/<4/5/4/0/16> freq=21402 (internal traffic: 0.92, orig_status=200)
        r = user.get('/full/seri/JRASC/0103//0000066.000.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 47) /articles/abstracts/<4/5/23> freq=17626 (internal traffic: 0.89, orig_status=200)
        r = user.get('/articles/abstracts/1976/ApJ../1976ApJ...203..297S.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 48) /cgi-bin/exec_myads2/all?<params> freq=13904 (internal traffic: 0.00, orig_status=200)
        r = user.get('/cgi-bin/exec_myads2/all?id=316154300&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 49) /cgi-bin/basic_connect?<params> freq=13172 (internal traffic: 0.01, orig_status=302)
        r = user.get('/cgi-bin/basic_connect?qsearch=Shankland%2C+p&amp;version=1')
        self.assertEquals(r.status_code, 302)
        
        
        
        # ( 50) /physics_service.html freq=10911 (internal traffic: 0.63, orig_status=200)
        r = user.get('/physics_service.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 51) /abs_doc/classic_form_analytics.js freq=10155 (internal traffic: 0.99, orig_status=304)
        r = user.get('/abs_doc/classic_form_analytics.js')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 52) /cgi-bin/exec_myads2?<params> freq=9690 (internal traffic: 0.00, orig_status=200)
        r = user.head('/cgi-bin/exec_myads2?id=364380276&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 53) /abs/<9> freq=9634 (internal traffic: 0.79, orig_status=404)
        r = user.get('/abs/undefined')
        self.assertEquals(r.status_code, 404)
        
        
        
        # ( 54) /figs/ads_logo_medium_dark_trans_background.png freq=8416 (internal traffic: 0.00, orig_status=200)
        r = user.get('/figs/ads_logo_medium_dark_trans_background.png')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 55) /abs/<19> freq=8201 (internal traffic: 0.07, orig_status=404)
        r = user.get('/abs/2019AIPC.2142m0005C')
        self.assertEquals(r.status_code, 404)
        
        
        
        # ( 56) /abstract_service.html/legacy freq=7590 (internal traffic: 0.99, orig_status=200)
        r = user.get('/abstract_service.html/legacy')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 57) /bib_abs.html freq=6886 (internal traffic: 0.65, orig_status=200)
        r = user.get('/bib_abs.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 58) /full/<19> freq=6722 (internal traffic: 0.71, orig_status=200)
        r = user.head('/full/1959BAN....14..323V')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 59) /abstract_service.html/ freq=6545 (internal traffic: 0.04, orig_status=200)
        r = user.get('/abstract_service.html/')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 60) /cgi-bin/abs_connect?<params> freq=6259 (internal traffic: 0.10, orig_status=200)
        r = user.get('/cgi-bin/abs_connect?data_type=VOTABLE&DEC=60&RA=16&SR=.1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 61) /cgi-bin/nph-abs_connect freq=5514 (internal traffic: 0.06, orig_status=200)
        r = user.get('/cgi-bin/nph-abs_connect')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 62) /apple-touch-icon.png freq=5345 (internal traffic: 0.00, orig_status=404)
        r = user.get('/apple-touch-icon.png')
        self.assertEquals(r.status_code, 404)
        
        
        
        # ( 63) /full/<10/4/5/4/0/16> freq=5052 (internal traffic: 0.99, orig_status=200)
        r = user.get('/full/thumbnails/seri/IrAJ./0020//0000102,002.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 64) /cgi-bin/pref_set freq=4748 (internal traffic: 0.83, orig_status=302)
        r = user.get('/cgi-bin/pref_set')
        self.assertEquals(r.status_code, 302)
        
        
        
        # ( 65) /cgi-bin/nph-data_query?<params> freq=4642 (internal traffic: 0.64, orig_status=200)
        r = user.head('/cgi-bin/nph-data_query?bibcode=1988JOSAB...5..243D&link_type=ARTICLE&db_key=PHY&high=')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 66) / freq=4555 (internal traffic: 0.08, orig_status=200)
        r = user.head('/')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 67) /abs/<19/9/0> freq=4452 (internal traffic: 1.00, orig_status=404)
        r = user.post('/abs/2003PhDT........62K/trackback/')
        self.assertEquals(r.status_code, 404)
        
        
        
        # ( 68) /ads_browse.html freq=4422 (internal traffic: 0.77, orig_status=200)
        r = user.get('/ads_browse.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 69) /apple-touch-icon-precomposed.png freq=4369 (internal traffic: 0.00, orig_status=404)
        r = user.get('/apple-touch-icon-precomposed.png')
        self.assertEquals(r.status_code, 404)
        
        
        
        # ( 70) /full/<6/4/5/4/0/16> freq=4339 (internal traffic: 0.99, orig_status=200)
        r = user.get('/full/record/seri/IrAJ./0020//0000102,002.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 71) /abs/<28> freq=4333 (internal traffic: 0.08, orig_status=200)
        r = user.get('/abs/1975tads.book.....R%E5%AF%86')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 72) /full/<3/4/5/4/0/16> freq=4312 (internal traffic: 0.98, orig_status=200)
        r = user.get('/full/gif/seri/IrAJ./0020//0000102,002.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 73) /abs/<34> freq=4072 (internal traffic: 0.00, orig_status=200)
        r = user.get('/abs/1989STIA...9051377A%EF%BF%BD%C3%9C')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 74) /cgi-bin/nph-toc_query?<params> freq=4029 (internal traffic: 0.10, orig_status=200)
        r = user.get('/cgi-bin/nph-toc_query?journal=ApJ&volume=LATEST&data_type=RSS&db_key=AST')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 75) /favicon.ico freq=3915 (internal traffic: 0.00, orig_status=200)
        r = user.head('/favicon.ico')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 76) /figs/dot.gif freq=3913 (internal traffic: 0.71, orig_status=304)
        r = user.get('/figs/dot.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 77) /cgi-bin/bib_query?<params> freq=3912 (internal traffic: 0.01, orig_status=404)
        r = user.get('/cgi-bin/bib_query?1991RC3.9.C...0000d')
        self.assertEquals(r.status_code, 404)
        
        
        
        # ( 78) /cgi-bin/nph-manage_account freq=3728 (internal traffic: 0.98, orig_status=200)
        r = user.post('/cgi-bin/nph-manage_account')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 79) /doi/<7/5/7> freq=3646 (internal traffic: 0.44, orig_status=200)
        r = user.get('/doi/10.1093/mnras/stz2615')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 80) /abs/<23> freq=3631 (internal traffic: 0.32, orig_status=200)
        r = user.get('/abs/1997A&amp;A...321..293S')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 81) /figs/myadslogo.gif freq=3484 (internal traffic: 0.01, orig_status=304)
        r = user.get('/figs/myadslogo.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 82) /abs_doc/help_pages/art_service.html freq=3388 (internal traffic: 0.97, orig_status=404)
        r = user.get('/abs_doc/help_pages/art_service.html')
        self.assertEquals(r.status_code, 404)
        
        
        
        # ( 83) /default_service.html freq=3347 (internal traffic: 0.02, orig_status=200)
        r = user.get('/default_service.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 84) /?<params> freq=3292 (internal traffic: 0.33, orig_status=200)
        r = user.get('/?author=2')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 85) /figs/arxiv_logo.gif freq=3278 (internal traffic: 0.19, orig_status=200)
        r = user.get('/figs/arxiv_logo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 86) /figs/nasalogo.gif freq=3126 (internal traffic: 0.89, orig_status=304)
        r = user.get('/figs/nasalogo.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 87) /figs/cfalogo.gif freq=3069 (internal traffic: 0.89, orig_status=304)
        r = user.get('/figs/cfalogo.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 88) /abs_doc/help_pages/search.html freq=3044 (internal traffic: 0.53, orig_status=200)
        r = user.get('/abs_doc/help_pages/search.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 89) /figs/newlogo_small.gif freq=3023 (internal traffic: 0.89, orig_status=304)
        r = user.get('/figs/newlogo_small.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 90) /figs/adslogo.gif freq=2955 (internal traffic: 0.99, orig_status=304)
        r = user.get('/figs/adslogo.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 91) /abs_doc/help_pages/images/adslogo.gif freq=2867 (internal traffic: 0.97, orig_status=200)
        r = user.get('/abs_doc/help_pages/images/adslogo.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 92) /cgi-bin/basic_connect?<params> freq=2866 (internal traffic: 0.00, orig_status=200)
        r = user.head('/cgi-bin/basic_connect?qsearch=10.1016/j.jaad.2015.07.028')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 93) /figs/newlogo.gif freq=2857 (internal traffic: 0.87, orig_status=304)
        r = user.get('/figs/newlogo.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # ( 94) /abs_doc/help_pages/images/dot.gif freq=2847 (internal traffic: 0.97, orig_status=200)
        r = user.get('/abs_doc/help_pages/images/dot.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 95) /abs_doc/help_pages/images/goup.gif freq=2791 (internal traffic: 0.97, orig_status=200)
        r = user.get('/abs_doc/help_pages/images/goup.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 96) /abs_doc/help_pages/images/right.gif freq=2767 (internal traffic: 0.97, orig_status=200)
        r = user.get('/abs_doc/help_pages/images/right.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 97) /abs_doc/help_pages/images/left.gif freq=2663 (internal traffic: 0.97, orig_status=200)
        r = user.get('/abs_doc/help_pages/images/left.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 98) /cgi-bin/insert_login/credentials freq=2647 (internal traffic: 0.00, orig_status=200)
        r = user.get('/cgi-bin/insert_login/credentials')
        self.assertEquals(r.status_code, 200)
        
        
        
        # ( 99) /cgi-bin/iarticle_query?<params> freq=2639 (internal traffic: 0.12, orig_status=200)
        r = user.get('/cgi-bin/iarticle_query?journal=AbbOO&volume=0001&type=SCREEN_THMB')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (100) /plus/mytag_js.php?<params> freq=2603 (internal traffic: 0.75, orig_status=404)
        r = user.post('/plus/mytag_js.php?aid=511348')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (101) /abstract_service.html/legacy freq=2574 (internal traffic: 0.01, orig_status=302)
        r = user.get('/abstract_service.html/legacy')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (102) /figs/addtomyyahoo.gif freq=2530 (internal traffic: 1.00, orig_status=304)
        r = user.get('/figs/addtomyyahoo.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # (103) /figs/xml.gif freq=2495 (internal traffic: 0.99, orig_status=304)
        r = user.get('/figs/xml.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # (104) /cgi-bin/exec_myads2/?<params> freq=2386 (internal traffic: 0.00, orig_status=200)
        r = user.get('/cgi-bin/exec_myads2/?id=303307024&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (105) /full/<89> freq=2290 (internal traffic: 0.00, orig_status=404)
        r = user.get('/full/bibcode=2019APS..MARF66013F&data_type=PDF_HIGH&whole_paper=YES&type=PRINTER&filetype=.pdf')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (106) /cgi-bin/exec_myads2?<params> freq=2283 (internal traffic: 0.19, orig_status=304)
        r = user.get('/cgi-bin/exec_myads2?id=342951612&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 304)
        
        
        
        # (107) /cgi-bin/list_connect?<params> freq=2249 (internal traffic: 0.58, orig_status=200)
        r = user.get('/cgi-bin/list_connect?version=1&aut_xct=YES&db_key=AST&aut_list=stone%2C+j')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (108) /basic_search.html freq=2223 (internal traffic: 0.48, orig_status=200)
        r = user.get('/basic_search.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (109) /abs_doc/faq.html freq=2202 (internal traffic: 0.33, orig_status=200)
        r = user.get('/abs_doc/faq.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (110) /full/<20> freq=2113 (internal traffic: 0.00, orig_status=200)
        r = user.get('/full/1977AJ.....82.1013L7')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (111) /figs/nasalogo_med.png freq=2052 (internal traffic: 1.00, orig_status=304)
        r = user.get('/figs/nasalogo_med.png')
        self.assertEquals(r.status_code, 304)
        
        
        
        # (112) /apple-touch-icon.png freq=1990 (internal traffic: 0.00, orig_status=404)
        r = user.head('/apple-touch-icon.png')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (113) /apple-touch-icon-precomposed.png freq=1989 (internal traffic: 0.00, orig_status=404)
        r = user.head('/apple-touch-icon-precomposed.png')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (114) /doi/<7/6> freq=1922 (internal traffic: 0.02, orig_status=302)
        r = user.get('/doi/10.1086/176149')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (115) /abs/<16> freq=1863 (internal traffic: 0.00, orig_status=200)
        r = user.get('/abs/arXiv:1807.07702')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (116) /abs_doc/ads.css freq=1858 (internal traffic: 1.00, orig_status=304)
        r = user.get('/abs_doc/ads.css')
        self.assertEquals(r.status_code, 304)
        
        
        
        # (117) /abs/<18> freq=1841 (internal traffic: 0.22, orig_status=200)
        r = user.get('/abs/1985EnTR........15')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (118) /figs/si_logo.gif freq=1800 (internal traffic: 1.00, orig_status=304)
        r = user.get('/figs/si_logo.gif')
        self.assertEquals(r.status_code, 304)
        
        
        
        # (119) /cgi-bin/bib_query?<params> freq=1738 (internal traffic: 0.03, orig_status=200)
        r = user.head('/cgi-bin/bib_query?2000ApJ...535...30J')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (120) /cgi-bin/access_denied freq=1690 (internal traffic: 0.01, orig_status=403)
        r = user.head('/cgi-bin/access_denied')
        self.assertEquals(r.status_code, 403)
        
        
        
        # (121) /robots.txt freq=1657 (internal traffic: 0.03, orig_status=200)
        r = user.get('/robots.txt')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (122) /cgi-bin/exec_myads2/all?<params> freq=1582 (internal traffic: 0.00, orig_status=304)
        r = user.get('/cgi-bin/exec_myads2/all?id=358139204&db_ley=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 304)
        
        
        
        # (123) /doi/<7/24> freq=1528 (internal traffic: 0.00, orig_status=200)
        r = user.get('/doi/10.1111/j.1365-2966.2012.21965.x')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (124) /cgi-bin/article_queryform?<params> freq=1523 (internal traffic: 0.73, orig_status=200)
        r = user.get('/cgi-bin/article_queryform?bibcode=1971ApJ...165..181W&letter=0&db_key=AST&page=181&plate=&fiche=&cover=&pagetype=.')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (125) /cgi-bin/nph-basic_connect freq=1491 (internal traffic: 0.10, orig_status=200)
        r = user.get('/cgi-bin/nph-basic_connect')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (126) /cgi-bin/nph-iarticle_query?<params> freq=1455 (internal traffic: 0.47, orig_status=200)
        r = user.head('/cgi-bin/nph-iarticle_query?1978ApJ...225..357S&data_type=PDF_HIGH&whole_paper=YES&type=PRINTER&filetype=.pdf')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (127) /abs_doc/help_pages/results.html freq=1402 (internal traffic: 0.39, orig_status=200)
        r = user.get('/abs_doc/help_pages/results.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (128) /cgi-bin/nph-abs_connect?<params> freq=1400 (internal traffic: 0.16, orig_status=200)
        r = user.head('/cgi-bin/nph-abs_connect?db_key=AST&db_key=PHY&sim_query=YES&ned_query=YES&aut_xct=YES&aut_logic=OR&obj_logic=OR&author=Douglas%2C+A.+Vibert%0D%0ADouglas%2C+A.+V.&object=&start_mon=&start_year=&end_mon=&end_year=1982')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (129) /abs/<20> freq=1270 (internal traffic: 0.09, orig_status=404)
        r = user.get('/abs/2002A&A...349...415T')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (130) /abs_doc/list_funcs.js freq=1256 (internal traffic: 0.99, orig_status=200)
        r = user.get('/abs_doc/list_funcs.js')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (131) /cgi-bin/myads2_set freq=1251 (internal traffic: 1.00, orig_status=200)
        r = user.post('/cgi-bin/myads2_set')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (132) /cgi-bin/nph-bib_query?<params> freq=1215 (internal traffic: 0.04, orig_status=200)
        r = user.head('/cgi-bin/nph-bib_query?bibcode=1962IAUS...14..419S&db_key=AST&high=3e6fbfd69f01910')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (133) /doi/<7/17> freq=1195 (internal traffic: 0.18, orig_status=200)
        r = user.get('/doi/10.1038/s41550-019-0892-y')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (134) /cgi-bin/myads2_set?<params> freq=1187 (internal traffic: 0.11, orig_status=302)
        r = user.get('/cgi-bin/myads2_set?')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (135) /abs_doc/help_pages/taggedformat.html freq=1187 (internal traffic: 0.10, orig_status=200)
        r = user.get('/abs_doc/help_pages/taggedformat.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (136) /myads/ freq=1170 (internal traffic: 0.38, orig_status=200)
        r = user.get('/myADS/')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (137) /myads freq=1159 (internal traffic: 0.36, orig_status=301)
        r = user.get('/myADS')
        self.assertEquals(r.status_code, 301)
        
        
        
        # (138) /user.php?<params> freq=1145 (internal traffic: 0.00, orig_status=404)
        r = user.get('/user.php?act=login')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (139) /proxy5/check.php freq=1133 (internal traffic: 0.00, orig_status=404)
        r = user.post('/proxy5/check.php')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (140) /preprint_service.html freq=1132 (internal traffic: 0.70, orig_status=200)
        r = user.get('/preprint_service.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (141) /cgi-bin/bib_query?<params> freq=1099 (internal traffic: 0.01, orig_status=302)
        r = user.get('/cgi-bin/bib_query?arXiv%3A1706.08555=')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (142) /cgi-bin/pref_set?<params> freq=1055 (internal traffic: 0.93, orig_status=302)
        r = user.get('/cgi-bin/pref_set?2&abs_proxy=http://adsabs.harvard.edu')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (143) /xmlrpc.php?<params> freq=1040 (internal traffic: 0.00, orig_status=404)
        r = user.get('/xmlrpc.php?rsd')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (144) /cgi-bin/exec_myads2?<params> freq=1012 (internal traffic: 0.00, orig_status=304)
        r = user.head('/cgi-bin/exec_myads2?id=364380276&db_key=DAILY_PRE&rss=2.1')
        self.assertEquals(r.status_code, 304)
        
        
        
        # (145) /abs/<23> freq=1002 (internal traffic: 0.02, orig_status=302)
        r = user.get('/abs/2000A+ACY-A...355L..27H')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (146) /abs_doc/help_pages/data.html freq=968 (internal traffic: 0.21, orig_status=200)
        r = user.get('/abs_doc/help_pages/data.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (147) /abs_doc/site_map/ freq=966 (internal traffic: 0.60, orig_status=200)
        r = user.get('/abs_doc/site_map/')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (148) /cms/wp-includes/wlwmanifest.xml freq=957 (internal traffic: 0.00, orig_status=404)
        r = user.get('/cms/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (149) /site/wp-includes/wlwmanifest.xml freq=956 (internal traffic: 0.00, orig_status=404)
        r = user.get('/site/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (150) /wordpress/wp-includes/wlwmanifest.xml freq=956 (internal traffic: 0.00, orig_status=404)
        r = user.get('/wordpress/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (151) /abs_doc/journal_abbr.html freq=954 (internal traffic: 0.82, orig_status=200)
        r = user.get('/abs_doc/journal_abbr.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (152) /blog/wp-includes/wlwmanifest.xml freq=953 (internal traffic: 0.00, orig_status=404)
        r = user.get('/blog/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (153) /wp/wp-includes/wlwmanifest.xml freq=953 (internal traffic: 0.00, orig_status=404)
        r = user.get('/wp/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (154) /admin_aspcms/_system/aspcms_sitesetting.asp freq=951 (internal traffic: 0.67, orig_status=404)
        r = user.post('/admin_aspcms/_system/AspCms_SiteSetting.asp')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (155) /full/<19/16> freq=950 (internal traffic: 0.45, orig_status=200)
        r = user.head('/full/2003JAHH....6...46S/0000046.000.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (156) /wp-includes/wlwmanifest.xml freq=949 (internal traffic: 0.00, orig_status=404)
        r = user.get('/wp-includes/wlwmanifest.xml')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (157) /cgi-bin/nph-journal_query?<params> freq=930 (internal traffic: 0.79, orig_status=200)
        r = user.get('/cgi-bin/nph-journal_query?journal=2003cigs.book.....F&page=1&type=SCREEN_THMB')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (158) /full/<4/5/4/16> freq=914 (internal traffic: 0.18, orig_status=200)
        r = user.get('/full/seri/QJRAS/0026/0000151.000.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (159) /cgi-bin/manage_account freq=898 (internal traffic: 0.02, orig_status=200)
        r = user.get('/cgi-bin/manage_account')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (160) /user_feedback.html freq=860 (internal traffic: 0.61, orig_status=200)
        r = user.get('/user_feedback.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (161) /cgi-bin/manage_account/credentials?<params> freq=836 (internal traffic: 0.00, orig_status=200)
        r = user.post('/cgi-bin/manage_account/credentials?man_email=apal%40szofi.net&man_cmd=elogin&man_passwd=qqriq123')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (162) /abs_doc/help_pages/overview.html freq=799 (internal traffic: 0.21, orig_status=200)
        r = user.get('/abs_doc/help_pages/overview.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (163) /doi/<7/5/6> freq=795 (internal traffic: 0.02, orig_status=200)
        r = user.get('/doi/10.1093/mnras/stz514')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (164) /cgi-bin/xauthor_queryform?<params> freq=775 (internal traffic: 0.75, orig_status=200)
        r = user.get('/cgi-bin/xauthor_queryform?db_key=AST')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (165) /cgi-bin/list_connect?<params> freq=774 (internal traffic: 1.00, orig_status=302)
        r = user.get('/cgi-bin/list_connect?aut_list=A*&aut_list_ln=YES&db_key=PHY')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (166) /abs/<20> freq=768 (internal traffic: 0.07, orig_status=302)
        r = user.get('/abs/2017NatSR...741548O.')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (167) /abs_doc/help_pages/ freq=768 (internal traffic: 0.55, orig_status=200)
        r = user.get('/abs_doc/help_pages/')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (168) /full/<19> freq=746 (internal traffic: 0.01, orig_status=302)
        r = user.get('/full/1992ASPC...28..123C')
        self.assertEquals(r.status_code, 302)
        
        
        
        # (169) /mirrors.html freq=722 (internal traffic: 0.34, orig_status=200)
        r = user.get('/mirrors.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (170) /config/aspcms_config.asp freq=711 (internal traffic: 0.75, orig_status=404)
        r = user.post('/config/AspCms_Config.asp')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (171) /abs_doc/journals2.html freq=683 (internal traffic: 0.25, orig_status=200)
        r = user.get('/abs_doc/journals2.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (172) /cgi-bin/get_file?<params> freq=683 (internal traffic: 0.53, orig_status=200)
        r = user.get('/cgi-bin/get_file?pdfs/SPAW./1915/1915SPAW.......844E.pdf')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (173) /doi/<19> freq=659 (internal traffic: 0.01, orig_status=200)
        r = user.get('/doi/2016PhDT........49B')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (174) /full/<3/19/25> freq=659 (internal traffic: 1.00, orig_status=200)
        r = user.get('/full/gif/1983JHA....14..137V/0000137.000.html?high=478aa91ccd09202')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (175) /utility/convert/data/config.inc.php freq=652 (internal traffic: 0.66, orig_status=404)
        r = user.post('/utility/convert/data/config.inc.php')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (176) /figs/newlogo.gif freq=650 (internal traffic: 0.76, orig_status=206)
        r = user.get('/figs/newlogo.gif')
        self.assertEquals(r.status_code, 206)
        
        
        
        # (177) /abs_doc/refereed.html freq=640 (internal traffic: 0.38, orig_status=200)
        r = user.get('/abs_doc/refereed.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (178) /article_service.html freq=629 (internal traffic: 0.54, orig_status=200)
        r = user.get('/article_service.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (179) /full/<6/4/5/4/24> freq=625 (internal traffic: 0.72, orig_status=200)
        r = user.get('/full/record/seri/Astr./0007/1970Astr....7..154D.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (180) /index.php?<params> freq=605 (internal traffic: 0.69, orig_status=404)
        r = user.get('/index.php?c=api&m=data2&auth=50ce0d2401ce4802751739552c8e4467&param=update_avatar&file=data:image/php;base64,eGJzaGVsbCUzQyUzRnBocCUwQSUyNHN0JTIwJTNEJTIwQGNyZWF0ZV9mdW5jdGlvbiUyOCUyNyUyNyUyQyUyMCUyNF9QT1NUJTVCJTI3aHhxOTkxMjE3JTI3JTVEJTI5JTNCJTBBJTI0c3QlMjglMjklM0I=')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (181) /doi/<7/5/9> freq=597 (internal traffic: 0.00, orig_status=200)
        r = user.get('/doi/10.1093/mnras/167.1.31P')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (182) /abs_doc/help_pages/art_retrieve.html freq=591 (internal traffic: 0.39, orig_status=200)
        r = user.get('/abs_doc/help_pages/art_retrieve.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (183) /abstract_service.html?<params> freq=583 (internal traffic: 0.58, orig_status=500)
        r = user.get('/abstract_service.html?nosetcookie=1')
        self.assertEquals(r.status_code, 500)
        
        
        
        # (184) /index.html freq=579 (internal traffic: 0.13, orig_status=200)
        r = user.get('/index.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (185) /plus/90sec.php freq=576 (internal traffic: 0.67, orig_status=404)
        r = user.post('/plus/90sec.php')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (186) /doi/<7/6> freq=563 (internal traffic: 0.34, orig_status=200)
        r = user.head('/doi/10.1086/161749')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (187) /doi/<7/4/6> freq=561 (internal traffic: 0.38, orig_status=200)
        r = user.get('/doi/10.1093/pasj/psx137')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (188) /journals_service.html freq=558 (internal traffic: 0.32, orig_status=200)
        r = user.get('/journals_service.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (189) /abs_doc/site_map/map.html freq=556 (internal traffic: 0.97, orig_status=200)
        r = user.get('/abs_doc/site_map/map.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (190) /abs_doc/site_map/images/question.gif freq=550 (internal traffic: 1.00, orig_status=200)
        r = user.get('/abs_doc/site_map/images/question.gif')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (191) /doi/<7/17> freq=549 (internal traffic: 0.00, orig_status=404)
        r = user.get('/doi/10.1017/S0251107X00007136')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (192) /cgi-bin/dexterstart.pl?<params> freq=544 (internal traffic: 0.47, orig_status=200)
        r = user.get('/cgi-bin/dexterstart.pl?bibcode=1995ApJS...96..371N&imagepath=seri/ApJS./0096//600/0000399.000&db_key=AST&page=399&bits=4')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (193) /fdgq.php freq=538 (internal traffic: 0.64, orig_status=404)
        r = user.post('/fdgq.php')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (194) /abs_doc/site_map/desc.html freq=532 (internal traffic: 0.99, orig_status=200)
        r = user.get('/abs_doc/site_map/desc.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (195) /abs_doc/help_pages/citations.html freq=523 (internal traffic: 0.56, orig_status=200)
        r = user.get('/abs_doc/help_pages/citations.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (196) /abstract_service.html freq=519 (internal traffic: 0.27, orig_status=200)
        r = user.head('/abstract_service.html')
        self.assertEquals(r.status_code, 200)
        
        
        
        # (197) /abs... freq=516 (internal traffic: 1.00, orig_status=404)
        r = user.get('/abs...')
        self.assertEquals(r.status_code, 404)
        
        
        
        # (198) /plus/mytag_js.php?<params> freq=509 (internal traffic: 0.67, orig_status=404)
        r = user.get('/plus/mytag_js.php?dopost=saveedit&arrs1%5B%5D=99&arrs1%5B%5D=102&arrs1%5B%5D=103&arrs1%5B%5D=95&arrs1%5B%5D=100&arrs1%5B%5D=98&arrs1%5B%5D=112&arrs1%5B%5D=114&arrs1%5B%5D=101&arrs1%5B%5D=102&arrs1%5B%5D=105&arrs1%5B%5D=120&arrs2%5B%5D=109&arrs2%5B%5D=121&arrs2%5B%5D=116&arrs2%5B%5D=97&arrs2%5B%5D=103&arrs2%5B%5D=96&arrs2%5B%5D=32&arrs2%5B%5D=40&arrs2%5B%5D=97&arrs2%5B%5D=105&arrs2%5B%5D=100&arrs2%5B%5D=44&arrs2%5B%5D=110&arrs2%5B%5D=111&arrs2%5B%5D=114&arrs2%5B%5D=109&arrs2%5B%5D=98&arrs2%5B%5D=111&arrs2%5B%5D=100&arrs2%5B%5D=121&arrs2%5B%5D=41&arrs2%5B%5D=32&arrs2%5B%5D=86&arrs2%5B%5D=65&arrs2%5B%5D=76&arrs2%5B%5D=85&arrs2%5B%5D=69&arrs2%5B%5D=83&arrs2%5B%5D=40&arrs2%5B%5D=57&arrs2%5B%5D=48&arrs2%5B%5D=57&arrs2%5B%5D=48&arrs2%5B%5D=44&arrs2%5B%5D=39&arrs2%5B%5D=60&arrs2%5B%5D=63&arrs2%5B%5D=112&arrs2%5B%5D=104&arrs2%5B%5D=112&arrs2%5B%5D=32&arrs2%5B%5D=101&arrs2%5B%5D=99&arrs2%5B%5D=104&arrs2%5B%5D=111&arrs2%5B%5D=32&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=100&arrs2%5B%5D=101&arrs2%5B%5D=100&arrs2%5B%5D=101&arrs2%5B%5D=99&arrs2%5B%5D=109&arrs2%5B%5D=115&arrs2%5B%5D=32&arrs2%5B%5D=53&arrs2%5B%5D=46&arrs2%5B%5D=55&arrs2%5B%5D=32&arrs2%5B%5D=48&arrs2%5B%5D=100&arrs2%5B%5D=97&arrs2%5B%5D=121&arrs2%5B%5D=60&arrs2%5B%5D=98&arrs2%5B%5D=114&arrs2%5B%5D=62&arrs2%5B%5D=103&arrs2%5B%5D=117&arrs2%5B%5D=105&arrs2%5B%5D=103&arrs2%5B%5D=101&arrs2%5B%5D=44&arrs2%5B%5D=32&arrs2%5B%5D=57&arrs2%5B%5D=48&arrs2%5B%5D=115&arrs2%5B%5D=101&arrs2%5B%5D=99&arrs2%5B%5D=46&arrs2%5B%5D=111&arrs2%5B%5D=114&arrs2%5B%5D=103&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=59&arrs2%5B%5D=64&arrs2%5B%5D=112&arrs2%5B%5D=114&arrs2%5B%5D=101&arrs2%5B%5D=103&arrs2%5B%5D=95&arrs2%5B%5D=114&arrs2%5B%5D=101&arrs2%5B%5D=112&arrs2%5B%5D=108&arrs2%5B%5D=97&arrs2%5B%5D=99&arrs2%5B%5D=101&arrs2%5B%5D=40&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=47&arrs2%5B%5D=91&arrs2%5B%5D=99&arrs2%5B%5D=111&arrs2%5B%5D=112&arrs2%5B%5D=121&arrs2%5B%5D=114&arrs2%5B%5D=105&arrs2%5B%5D=103&arrs2%5B%5D=104&arrs2%5B%5D=116&arrs2%5B%5D=93&arrs2%5B%5D=47&arrs2%5B%5D=101&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=44&arrs2%5B%5D=36&arrs2%5B%5D=95&arrs2%5B%5D=82&arrs2%5B%5D=69&arrs2%5B%5D=81&arrs2%5B%5D=85&arrs2%5B%5D=69&arrs2%5B%5D=83&arrs2%5B%5D=84&arrs2%5B%5D=91&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=103&arrs2%5B%5D=117&arrs2%5B%5D=105&arrs2%5B%5D=103&arrs2%5B%5D=101&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=93&arrs2%5B%5D=44&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=101&arrs2%5B%5D=114&arrs2%5B%5D=114&arrs2%5B%5D=111&arrs2%5B%5D=114&arrs2%5B%5D=39&arrs2%5B%5D=39&arrs2%5B%5D=41&arrs2%5B%5D=59&arrs2%5B%5D=63&arrs2%5B%5D=62&arrs2%5B%5D=39&arrs2%5B%5D=41&arrs2%5B%5D=59&arrs2%5B%5D=0')
        self.assertEquals(r.status_code, 404)
