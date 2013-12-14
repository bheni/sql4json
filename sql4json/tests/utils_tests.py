import unittest
import json

from sql4json.utils import *

class DictionaryPathTests(unittest.TestCase):
    def test_get_root(self):
        data = {"a":1, "b":2, "c":3}

        self.assertEqual((True, [data]), get_elements_by_path(data, "/"))
        self.assertEqual((True, [data]), get_elements_by_path(data, "."))
        self.assertEqual((True, [data]), get_elements_by_path(data, "\\"))

    def test_get_element(self):
        data = {"a":1, "b":2, "c":3}

        self.assertEqual((True, [1]), get_elements_by_path(data, "a"))
        self.assertEqual((True, [1]), get_elements_by_path(data, "/a"))

    def test_get_sub_element(self):
        data = {"a":1, "b":{"c":3}}

        self.assertEqual((True, [3]), get_elements_by_path(data, "/b/c"))
        self.assertEqual((True, [3]), get_elements_by_path(data, "b/c"))

    def test_get_sub_elements_of_array(self):
        data = {"students":[{"id":1},{"id":2}]}

        self.assertEqual((True, [1,2]), get_elements_by_path(data, "students/id"))

    def test_get_sub_elements_for_base_array(self):
        data = [{'type':'students', 'records':[{"id":1},{"id":2}]},{'type':'teachers', 'records':[{"id":3},{"id":4}]}]

        self.assertEqual((True, [1,2,3,4]), get_elements_by_path(data, "records/id"))

    def test_root_array_with_subarray(self):
        f = open("sql4json/tests/test_data_files/root_array_with_subarray.json")
        json_str = f.read()
        f.close()

        found, elements = get_elements_by_path(json.loads(json_str), "records")

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
            }], elements)


    def test_get_nonexistent_element(self):
        data = {"a":1, "b":{"c":3}}

        self.assertEqual((False,[]), get_elements_by_path(data, "/d"))

    def test_split_on_any(self):
        string = "str1,str2 str3, str4\rstr5\nstr6\tstr7, \r\n\tstr8,"
        results = split_on_any(string, frozenset((',',' ','\r','\n','\t')))

        self.assertEqual(['str1','str2','str3','str4','str5','str6','str7','str8'], results)
