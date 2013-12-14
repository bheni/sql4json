import unittest

from sql4json.exceptions import *
from sql4json.data_query_engine import DataQueryEngine

class DataQueryEngineTests(unittest.TestCase):
    def test_select_star(self):
        data = {"a": 1, "b":2, "c":{"ba":"string", "bb":False, "bc":None, "bd":[]}}
        query_engine = DataQueryEngine(data, "SELECT *")

        self.assertEqual([data], query_engine.get_results())

    def test_select_property(self):
        data = {"a": 1, "b":2, "c":{"ba":"string", "bb":False, "bc":None, "bd":[]}}
        query_engine = DataQueryEngine(data, "SELECT a")

        self.assertEqual([{"a":1}], query_engine.get_results())

    def test_select_on_array(self):
        data = [
            {"id":1,"name":"brian", "awesome":True},
            {"id":2,"name":"DRo", "awesome":True},
            {"id":3,"name":"Logan", "awesome":False}
        ]
        query_engine = DataQueryEngine(data, "SELECT id,name")

        self.assertEqual([{"id":1,"name":"brian"},{"id":2,"name":"DRo"},{"id":3,"name":"Logan"}], query_engine.get_results())

    def test_select_from(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people")

        self.assertEqual([{"id":1,"name":"brian"},{"id":2,"name":"DRo"},{"id":3,"name":"Logan"}], query_engine.get_results())

    def test_where_equality(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE awesome==True")

        self.assertEqual([{"id":1,"name":"brian"},{"id":2,"name":"DRo"}], query_engine.get_results())

    def test_where_inequality(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE awesome!=False")

        self.assertEqual([{"id":1,"name":"brian"},{"id":2,"name":"DRo"}], query_engine.get_results())

    def test_where_greater_than(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE id>1")

        self.assertEqual([{"id":2,"name":"DRo"},{"id":3,"name":"Logan"}], query_engine.get_results())
    
    def test_where_less_than(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE id<3")

        self.assertEqual([{"id":1,"name":"brian"},{"id":2,"name":"DRo"}], query_engine.get_results())

    def test_where_greater_than_or_equal(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE id>=2")

        self.assertEqual([{"id":2,"name":"DRo"},{"id":3,"name":"Logan"}], query_engine.get_results())

    def test_where_less_than_or_equal(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE id<=2")

        self.assertEqual([{"id":1,"name":"brian"},{"id":2,"name":"DRo"}], query_engine.get_results())

    def test_where_key_in_object(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True, "extra_key":None},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }
        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE extra_key IN /")

        self.assertEqual([{"id":1,"name":"brian"}], query_engine.get_results())

    def test_not_in_where_clause(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True, "extra_key":None},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }

        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE !(extra_key IN /)")

        self.assertEqual([{"id":2,"name":"DRo"},{"id":3,"name":"Logan"}], query_engine.get_results())

    def test_where_clause_with_boolean_or(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True, "extra_key":None},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }

        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE id==1 or id!=3")

        self.assertEqual([{"id":1,"name":"brian"},{"id":2,"name":"DRo"}], query_engine.get_results())

    def test_where_clause_with_boolean_and(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True, "extra_key":None},
                {"id":2,"name":"DRo", "awesome":True},
                {"id":3,"name":"Logan", "awesome":False}
            ], 
            "other":68
        }

        query_engine = DataQueryEngine(data, "SELECT id,name FROM people WHERE !(extra_key IN /) and awesome == TRUE")

        self.assertEqual([{"id":2,"name":"DRo"}], query_engine.get_results())

    def test_where_against_sub_field(self):
        data = {
            "people":[
                {"id":1,"name":"brian", "awesome":True,"employer":{"id":1,"name":"employer 1"}},
                {"id":2,"name":"DRo", "awesome":True,"employer":{"id":2,"name":"employer 2"}},
                {"id":3,"name":"Logan", "awesome":False,"employer":None}
            ], 
            "other":68
        }

        query_engine = DataQueryEngine(data, 'SELECT name FROM people WHERE employer/name=="employer 1"')

        self.assertEqual([{"name":"brian"}], query_engine.get_results())


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
