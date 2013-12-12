import unittest

from sql4json.sql4json import Sql4Json

class Sql4JsonTests(unittest.TestCase):
    def test_qurey_on_test_data(self):
        f = open("sql4json/tests/test_data_files/test_data.json")
        json_str = f.read()
        f.close()

        query = Sql4Json(json_str, "SELECT term from facets/deviceInfo/terms where total > 10000")

        self.assertEqual([{"term":"iPhone"},{"term":"Other"},{"term":"iPad"},{"term":"iPod"}],query.get_results())
        
        expected = '''[
    {
        "term": "iPhone"
    },
    {
        "term": "Other"
    },
    {
        "term": "iPad"
    },
    {
        "term": "iPod"
    }
]'''
    
        self.assertEqual(expected, str(query))