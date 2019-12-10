from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
    
bibcodes = ['1993CoPhC..74..239H','1994GPC.....9...69H']

class MetricsServiceTest(unittest.TestCase):    
    def test_anonymous_user(self):
        # Request all metrics for two existing bibcodes
        r = anonymous_user.post('/metrics', json={'bibcodes': bibcodes})
        # We should get a 401 status
        self.assertEqual(r.status_code, 401)
        
    def test_authenticated_user(self, user=authenticated_user):
        # Request all metrics for two existing bibcodes
        r = user.post('/metrics', json={'bibcodes': bibcodes})
        # We should get a 200 status
        self.assertEqual(r.status_code, 200)
        # The results should be in a dictionary
        self.assertIsInstance(r.json(), dict)
        # Check if we get the expected attributes
        expected_attr = ['basic stats', 'citation stats refereed',
                         'histograms', 'citation stats', 'time series',
                         'basic stats refereed', 'indicators refereed',
                         'skipped bibcodes', 'indicators']
        self.assertCountEqual(list(r.json().keys()), expected_attr)
        # Check if we retrieved all histograms
        expected_hists = ['downloads', 'citations', 'reads', 'publications']
        self.assertCountEqual(list(r.json()['histograms'].keys()), expected_hists)
        # All histograms should have the expected constituents
        histdict = {
            'downloads': ['refereed downloads', 'all downloads normalized',
                          'all downloads', 'refereed downloads normalized'],
            'reads': ['refereed reads', 'all reads normalized', 
                      'all reads', 'refereed reads normalized'],
            'publications': ['refereed publications', 'all publications',
                             'refereed publications normalized',
                             'all publications normalized'],
            'citations': ['refereed to nonrefereed', 'nonrefereed to nonrefereed',
                          'nonrefereed to nonrefereed normalized', 'nonrefereed to refereed',
                          'refereed to refereed normalized', 'refereed to nonrefereed normalized',
                          'refereed to refereed', 'nonrefereed to refereed normalized']
                   }
        for hist in expected_hists:
            self.assertCountEqual(list(r.json()['histograms'][hist].keys()), histdict[hist])
        # All histogram constituents should be dictionaries
        for hist in expected_hists:
            for hh in histdict[hist]:
                self.assertIsInstance(r.json()['histograms'][hist][hh], dict)
        # Did we get all expected indicators?
        expected_stats = {
            'indicators': ['g', 'read10', 'm', 'i10', 'riq', 'h', 'i100', 'tori'],
            'indicators refereed': ['g', 'read10', 'm', 'i10', 'riq', 'h', 'i100', 'tori'],
            'basic stats': ['average number of downloads', 'average number of reads', 'median number of downloads', 'median number of reads', 
                            'normalized paper count', 'number of papers', 'recent number of downloads', 'recent number of reads',
                            'total number of downloads', 'total number of reads'],
            'basic stats refereed': ['median number of downloads', 'average number of reads',
                            'normalized paper count', 'recent number of reads', 'number of papers',
                            'recent number of downloads', 'total number of reads',
                            'median number of reads', 'total number of downloads',
                            'average number of downloads'],
            'citation stats': ['average number of citations', 'average number of refereed citations', 'median number of citations', 
                               'median number of refereed citations', 'normalized number of citations', 'normalized number of refereed citations', 
                               'number of citing papers', 'number of self-citations', 'self-citations', 'total number of citations', 
                               'total number of refereed citations'],
            'citation stats refereed': 
                               ['normalized number of citations', 'average number of refereed citations', 
                                'median number of citations', 'median number of refereed citations', 
                                'number of citing papers', 'average number of citations', 
                                'total number of refereed citations', 'normalized number of refereed citations', 
                                'number of self-citations', 'total number of citations'],
                               
            'time series': ['g', 'h', 'tori', 'i10', 'read10', 'i100']        
        }
        for entry in expected_stats:
            self.assertCountEqual(sorted(r.json()[entry].keys()), sorted(expected_stats[entry]))#, 'Wrong values for "%s, got: %s"' % (entry, r.json()[entry].keys()))
        # There should be no skipped bibcodes
        self.assertCountEqual(r.json()['skipped bibcodes'], [])
        # Sending an empty list of bibcodes to the service should give a 403
        r = user.post('/metrics', json={'bibcodes': []})
        self.assertEqual(r.status_code, 403)
        # Test getting metrics for just one bibcode via GET
        r = user.get('/metrics/%s' % bibcodes[0])
        # We should get a 200
        self.assertEqual(r.status_code, 200)
        # And posting just one bibcode should work too
        r = user.post('/metrics', json={'bibcodes': bibcodes[:1]})
        # We should get a 200 status
        self.assertEqual(r.status_code, 200)
    
    def test_bumblebee_user(self):
        self.test_authenticated_user(user=bumblebee_user)



if __name__ == '__main__':
    unittest.main()
