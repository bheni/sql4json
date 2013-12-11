from tokenizer import Tokenizer
from enums import CEnum
from exceptions import SQLStatementFormatException

'''
Organizes tokens into select, from, and where sections and provides accesssor
functions to get the tokens from these sections.
'''
class SQLStatement(object):
    SECTIONS = CEnum(("SELECT", "FROM", "WHERE"))
    SECTION_NAMES = ("select", "from", "where")

    def __init__(self, sql_statement_string):
        self.tokenizer = Tokenizer(sql_statement_string)

        self.init_empty_sections()
        self.init_sections()

    def init_empty_sections(self):
        self.sections = []
        for section in SQLStatement.SECTION_NAMES:
            self.sections.append([])

    def init_sections(self):
        current_section = -1

        for token in self.tokenizer:
            token_lower = token.lower()

            if token_lower in SQLStatement.SECTION_NAMES:
                current_section = SQLStatement.SECTION_NAMES.index(token_lower)
            else:
                if current_section == -1:
                    raise SQLStatementFormatException('%s found before "select"' % token)
                else:
                    self.sections[current_section].append( token )

    def get_select_tokens(self):
        return self.sections[SQLStatement.SECTIONS.SELECT]

    def get_from_tokens(self):
        return self.sections[SQLStatement.SECTIONS.FROM]

    def get_where_tokens(self):
        return self.sections[SQLStatement.SECTIONS.WHERE]
