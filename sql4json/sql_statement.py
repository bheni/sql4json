"""
Organizes tokens into select, from, and where sections and provides accesssor
functions to get the tokens from these sections.
"""

from enums import CEnum
from exceptions import SQLStatementFormatException


class SQLStatement(object):
    SECTIONS = CEnum(("SELECT", "FROM", "WHERE", "LIMIT"))
    SECTION_NAMES = ("select", "from", "where", "limit")
    SECTION_NAMES_SET = frozenset(SECTION_NAMES)

    def __init__(self, sql_statement_string):
        self.sections = None

        self.sql_statement_string = sql_statement_string.strip()

        if not self.sql_statement_string.lower().startswith("select"):
            raise SQLStatementFormatException(
                '"%s" does not begin with a valid select statement.' % self.sql_statement_string)

        section_start_indices = self.get_start_of_each_section()
        self.parse_sections(section_start_indices)

    def get_start_of_each_section(self):
        lower = self.sql_statement_string.lower()
        quote_char = None
        section_start_indices = [-1] * SQLStatement.SECTIONS.COUNT
        current_chars = []
        current_word = None
        start_index = 0

        for i in range(len(self.sql_statement_string)):
            lower_char = lower[i]

            if quote_char == lower_char:
                quote_char = None
                current_chars = []
                start_index = i

            elif lower_char in ('"', "'"):
                quote_char = lower_char
                current_chars = [lower_char]
                start_index = i

            elif lower_char.isspace():
                current_word = ''.join(current_chars)
                if current_word in SQLStatement.SECTION_NAMES_SET:
                    section_index = SQLStatement.SECTION_NAMES.index(current_word)

                    if section_start_indices[section_index] != -1:
                        raise SQLStatementFormatException("Multiple %s sections found" % current_word)

                    section_start_indices[section_index] = start_index

                current_chars = []
                start_index = i

            else:
                current_chars.append(lower_char)

        if quote_char is not None:
            raise SQLStatementFormatException('" mismatch in %s' % self.sql_statement_string)
        elif ''.join(current_chars) in SQLStatement.SECTION_NAMES_SET:
            raise SQLStatementFormatException('Invalid %s section' % current_word)

        return section_start_indices

    def parse_sections(self, start_indices):
        self.sections = [None] * SQLStatement.SECTIONS.COUNT
        sorted_start_indices = sorted(start_indices)

        for i in range(len(sorted_start_indices)):
            index = sorted_start_indices[i]

            if index != -1:
                section_index = start_indices.index(index)
                index += len(SQLStatement.SECTION_NAMES[section_index]) + 1

                if i < len(sorted_start_indices) - 1:
                    self.sections[section_index] = self.sql_statement_string[index:sorted_start_indices[i + 1]].strip()
                else:
                    self.sections[section_index] = self.sql_statement_string[index:].strip()

    def get_select_section(self):
        return self.sections[SQLStatement.SECTIONS.SELECT]

    def get_from_section(self):
        return self.sections[SQLStatement.SECTIONS.FROM]

    def get_where_section(self):
        return self.sections[SQLStatement.SECTIONS.WHERE]

    def get_limit_section(self):
        return self.sections[SQLStatement.SECTIONS.LIMIT]
