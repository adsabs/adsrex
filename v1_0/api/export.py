from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
import unittest
import json


class ExportServiceTest(unittest.TestCase):
    def test_anonymous_user(self):
        data = {"bibcode": ["2018EPJWC.18612003D"], "sort": "date desc, bibcode desc",
                "maxauthor": 2, "authorcutoff": 10, "keyformat": "%1H:%Y"}
        r = anonymous_user.post('/export/bibtex', json=data)
        self.assertEqual(r.status_code, 401)

    def check_export_service(self, user=authenticated_user):
        data = {"bibcode": ["2018EPJWC.18612003D"], "sort": "date desc, bibcode desc",
                "maxauthor": 2, "authorcutoff": 10, "keyformat": "%1H:%Y"}
        r = user.post('/export/bibtex', json=data)
        self.assertTrue(r.json() == {'msg': 'Retrieved 1 abstracts, starting with number 1.',
                                     'export': '@INPROCEEDINGS{Damon:2018,\n'
                                                '       author = {{Damon}, James and {Henneken}, Edwin and {Accomazzi}, Alberto},\n'
                                                '        title = "{Managing Institutional Bibliographies using the ADS API: A new workflow using Google Sheets}",\n'
                                                '    booktitle = {European Physical Journal Web of Conferences},\n'
                                                '         year = "2018",\n'
                                                '       series = {European Physical Journal Web of Conferences},\n'
                                                '       volume = {186},\n'
                                                '        month = "Jul",\n'
                                                '          eid = {12003},\n'
                                                '        pages = {12003},\n'
                                                '          doi = {10.1051/epjconf/201818612003},\n'
                                                '       adsurl = {https://dev.adsabs.harvard.edu/abs/2018EPJWC.18612003D},\n'
                                                '      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n'
                                                '}\n\n'
                                     })

    def test_authenticated_user(self):
        self.check_export_service()

    def test_bumblebee_user(self):
        self.check_export_service(user=bumblebee_user)

if __name__ == '__main__':
    unittest.main()
