import unittest

from sql4json.sql4json import Sql4Json


class Sql4JsonTests(unittest.TestCase):
    def test_qurey_on_test_data(self):
        f = open("sql4json/tests/test_data_files/test_data.json")
        json_str = f.read()
        f.close()

        query = Sql4Json(json_str, "SELECT term from facets/deviceInfo/terms where total > 10000")

        self.assertEqual([{"term": "iPhone"}, {"term": "Other"}, {"term": "iPad"}, {"term": "iPod"}],
                         query.get_results())

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


    def test_qurey_on_hierarchy_of_arrays(self):
        f = open("sql4json/tests/test_data_files/hierarchy_of_arrays.json")
        json_str = f.read()
        f.close()

        query = Sql4Json(json_str, 'SELECT id from people/records where id > 2 and id < 5')
        self.assertEqual([{"id": 3}, {"id": 4}], query.get_results())

    def test_qurey_on_root_array_with_subarrays(self):
        f = open("sql4json/tests/test_data_files/root_array_with_subarray.json")
        json_str = f.read()
        f.close()

        query = Sql4Json(json_str, 'SELECT * from records')
        self.assertEqual(
            [{
                 "first_name": "David",
                 "id": 4,
                 "last_name": "Davidson"
             },
             {
                 "first_name": "Eric",
                 "id": 5,
                 "last_name": "Ericson"
             },
             {
                 "first_name": "Frank",
                 "id": 6,
                 "last_name": "Franklin"
             }]
            , query.get_results())