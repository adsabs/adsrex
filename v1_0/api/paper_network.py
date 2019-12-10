from v1_0.user_roles import anonymous_user, authenticated_user, bumblebee_user
from unittest import TestCase
import unittest
import json
    
# We will do all tests for the famous author A. Accomazzi
params = {}
params['q'] = 'author:"Accomazzi,A"'

class PaperNetworkTest(unittest.TestCase):
    def test_anonymous_user(self):
        # Try to get the paper network
        r = anonymous_user.post('/vis/paper-network', data=params)
        # We should get a 401 back
        self.assertEqual(r.status_code, 401)

    def check_paper_network(self, user=authenticated_user):
        ## Examine the paper network
        # Retrieve results for our query in 'params'
        r = user.post('/vis/paper-network', json={'query': [json.dumps(params)]})
        # We should get a 200 back
        self.assertEqual(r.status_code, 200)
        # Now we'll test the contents of what was sent back
        pdata = r.json()
        # We are sent back a dictionary
        self.assertIsInstance(pdata, dict)
        # This dictionary has two keys: 'msg' and 'data'
        self.assertIn('msg', pdata)
        self.assertIn('data', pdata)
        # The 'data' attribute has two keys: 'summaryGraph', 'fullGraph'
        self.assertIn('summaryGraph', pdata['data'])
        self.assertIn('fullGraph', pdata['data'])
        # Both graphs have the same attributes
        expected_attr = ['directed', 'graph', 'nodes', 'links', 'multigraph']
        self.assertCountEqual(expected_attr, list(pdata['data']['summaryGraph'].keys()))
        self.assertCountEqual(expected_attr, list(pdata['data']['fullGraph'].keys()))
        # The 'nodes' and 'links' attributes are lists of dictionaries in both graphs
        # Check the summaryGraph
        # First examine the nodes
        graph = pdata['data']['summaryGraph']
        self.assertIsInstance(graph['nodes'], list)
        expected_attr = ['paper_count', 'node_label', 'total_citations', 'node_name', 'top_common_references', 'total_reads', 'stable_index', 'id']
        for item in graph['nodes']:
            self.assertIsInstance(item, dict)
            self.assertCountEqual(expected_attr, list(item.keys()))
        # Now examine the links
        self.assertIsInstance(graph['links'], list)
        expected_attr = ['source', 'target', 'weight']
        for item in graph['links']:
            self.assertIsInstance(item, dict)
            self.assertCountEqual(expected_attr, list(item.keys()))
        # Now check the fullGraph
        # First examine the nodes
        graph = pdata['data']['fullGraph']
        self.assertIsInstance(graph['nodes'], list)
        expected_attr = ['read_count', 'group', 'title', 'first_author', 'citation_count', 'node_name', 'id', 'nodeWeight']
        for item in graph['nodes']:
            self.assertIsInstance(item, dict)
            self.assertCountEqual(expected_attr, list(item.keys()))
        # Now examine the links
        self.assertIsInstance(graph['links'], list)
        expected_attr = ['source', 'weight', 'overlap', 'target']
        for item in graph['links']:
            self.assertIsInstance(item, dict)
            self.assertCountEqual(expected_attr, list(item.keys()))

    def test_authenticated_user(self):
        self.check_paper_network()

    def test_bumblebee_user(self):
        self.check_paper_network(user=bumblebee_user)
        


if __name__ == '__main__':
    unittest.main()