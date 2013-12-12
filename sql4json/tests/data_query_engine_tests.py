import unittest

from sql4json.exceptions import *
from sql4json.data_query_engine import DataQueryEngine

class DataQueryEngineTests(unittest.TestCase):
    def test_select_star(self):
        data = {"a": 1, "b":2, "c":{"ba":"string", "bb":False, "bc":None, "bd":[]}}
        query_engine = DataQueryEngine(data, "SELECT *")

        self.assertEqual(data, query_engine.get_results())

    def test_select_property(self):
        data = {"a": 1, "b":2, "c":{"ba":"string", "bb":False, "bc":None, "bd":[]}}
        query_engine = DataQueryEngine(data, "SELECT a")

        self.assertEqual({"a":1}, query_engine.get_results())

    def test_select_on_array(self):
        data = [
            {"id":1, "name":"brian", "awesome":True},
            {"id":2,"name":"DRo", "awesome":True},
            {"id":3,"name":"Logan", "awesome":False}
        ]
        query_engine = DataQueryEngine(data, "SELECT id,name")

        self.assertEqual([{"id":1, "name":"brian"},{"id":2,"name":"DRo"},{"id":3,"name":"Logan"}], query_engine.get_results())

    def test_select_from(self):
        data = {
            "people":[
                {"id":1, "name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people")

        self.assertEqual([{"id":1, "name":"brian"},{"id":2,"name":"DRo"},{"id":3,"name":"Logan"}], query_engine.get_results())

    def test_select_from_where(self):
        data = {
            "people":[
                {"id":1, "name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE awesome==True")

        self.assertEqual([{"id":1, "name":"brian"},{"id":2,"name":"DRo"}], query_engine.get_results())

    # def test_where_equality(self):
    # def test_where_inequality(self):
    # def test_where_greater_than(self):
    # def test_where_less_than(self):
    # def test_where_greater_than_or_equal(self):
    # def test_where_less_than_or_equal(self):
    # def test_where_key_in_object(self):

    def test_where_operands_are_verified(self):
        try:
            data = {"a": 1, "b":2, "c":{"ba":"string", "bb":False, "bc":None, "bd":[]}}
            query_engine = DataQueryEngine(data, "SELECT * where no operand found")
            self.fail()
        except WhereClauseException, e:
            pass

        try:
            data = {"a": 1, "b":2, "c":{"ba":"string", "bb":False, "bc":None, "bd":[]}}
            query_engine = DataQueryEngine(data, "SELECT * where == no loperand")
            self.fail()
        except WhereClauseException, e:
            pass

        try:
            data = {"a": 1, "b":2, "c":{"ba":"string", "bb":False, "bc":None, "bd":[]}}
            query_engine = DataQueryEngine(data, "SELECT * where no roperand !=")
            self.fail()
        except WhereClauseException, e:
            pass
