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
        self.assertTrue(r.json() == {u'msg': u'Retrieved 1 abstracts, starting with number 1.',
                                     u'export': u'@INPROCEEDINGS{Damon:2018,\n'
                                                u'       author = {{Damon}, James and {Henneken}, Edwin and {Accomazzi}, Alberto},\n'
                                                u'        title = "{Managing Institutional Bibliographies using the ADS API: A new workflow using Google Sheets}",\n'
                                                u'    booktitle = {European Physical Journal Web of Conferences},\n'
                                                u'         year = "2018",\n'
                                                u'       series = {European Physical Journal Web of Conferences},\n'
                                                u'       volume = {186},\n'
                                                u'        month = "Jul",\n'
                                                u'          eid = {12003},\n'
                                                u'        pages = {12003},\n'
                                                u'          doi = {10.1051/epjconf/201818612003},\n'
                                                u'       adsurl = {https://dev.adsabs.harvard.edu/abs/2018EPJWC.18612003D},\n'
                                                u'      adsnote = {Provided by the SAO/NASA Astrophysics Data System}\n'
                                                u'}\n\n'
                                     })

    def test_authenticated_user(self):
        self.check_export_service()

    def test_bumblebee_user(self):
        self.check_export_service(user=bumblebee_user)

if __name__ == '__main__':
    unittest.main()
