import unittest

from sql4json.utils import *

class DictionaryPathTests(unittest.TestCase):
    def test_get_root(self):
        data = {"a":1, "b":2, "c":3}

        self.assertEqual((True,data), get_element_by_path(data, "/"))
        self.assertEqual((True, data), get_element_by_path(data, "."))
        self.assertEqual((True, data), get_element_by_path(data, "\\"))

    def test_get_element(self):
        data = {"a":1, "b":2, "c":3}

        self.assertEqual((True,1), get_element_by_path(data, "a"))
        self.assertEqual((True,1), get_element_by_path(data, "/a"))

    def test_get_sub_element(self):
        data = {"a":1, "b":{"c":3}}

        self.assertEqual((True,3), get_element_by_path(data, "/b/c"))
        self.assertEqual((True,3), get_element_by_path(data, "b/c"))

    def test_get_nonexistent_element(self):
        data = {"a":1, "b":{"c":3}}

        self.assertEqual((False,None), get_element_by_path(data, "/d"))

    def test_split_on_any(self):
        string = "str1,str2 str3, str4\rstr5\nstr6\tstr7, \r\n\tstr8,"
        results = split_on_any(string, frozenset((',',' ','\r','\n','\t')))

        self.assertEqual(['str1','str2','str3','str4','str5','str6','str7','str8'], results)
