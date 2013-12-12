import unittest

from sql4json.sql_statement import SQLStatement
from sql4json.exceptions import SQLStatementFormatException

class SQLStatementTests(unittest.TestCase):
    def test_parse_empty_statement(self):
        try:
            sql_statement = SQLStatement('')
            self.fail()
        except SQLStatementFormatException:
            pass

    def test_select(self):
        sql_statement = SQLStatement("select *")
        
        self.assertEqual("*", sql_statement.get_select_section())
        self.assertEqual(None, sql_statement.get_from_section())
        self.assertEqual(None, sql_statement.get_where_section())

    def test_select_from(self):
        sql_statement = SQLStatement("select * from some/path")
        
        self.assertEqual("*", sql_statement.get_select_section())
        self.assertEqual("some/path", sql_statement.get_from_section())
        self.assertEqual(None, sql_statement.get_where_section())

    def test_from_where(self):
        sql_statement = SQLStatement("SELECT id, key3 FROM somewhere WHERE key1==1 or (key2 == 'string value'&&key3>4")
        
        self.assertEqual("id, key3", sql_statement.get_select_section())
        self.assertEqual("somewhere", sql_statement.get_from_section())
        self.assertEqual("key1==1 or (key2 == 'string value'&&key3>4", sql_statement.get_where_section())

    def test_sql_statements_not_starting_with_a_section_name_throw_an_exception(self):
        try:
            sql_statement = SQLStatement("WORST sql statement.... EVER.")
            self.fail()
        except SQLStatementFormatException:
            pass