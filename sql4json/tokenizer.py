"""
Basic class for splitting a string up into tokens.
"""

from enums import CEnum


class Tokenizer(object):
    TOKEN_TYPES = CEnum(("NONE", "ALPHANUM", "SYMBOL", "WHITESPACE", "QUOTEDSTRING", "PARENOPEN", "PARENCLOSE"))

    QUOTE_CHARS = frozenset(('"', "'"))

    EMPTY_STIRNG_TYPES = frozenset((TOKEN_TYPES.WHITESPACE, TOKEN_TYPES.NONE))

    @staticmethod
    def get_token_type(char):
        if char.isalpha() or char.isdigit() or char == '_':
            return Tokenizer.TOKEN_TYPES.ALPHANUM
        elif char.isspace():
            return Tokenizer.TOKEN_TYPES.WHITESPACE
        elif char in Tokenizer.QUOTE_CHARS:
            return Tokenizer.TOKEN_TYPES.QUOTEDSTRING
        elif char == '(':
            return Tokenizer.TOKEN_TYPES.PARENOPEN
        elif char == ')':
            return Tokenizer.TOKEN_TYPES.PARENCLOSE
        else:
            return Tokenizer.TOKEN_TYPES.SYMBOL

    @staticmethod
    def is_paren_type(token_type):
        return token_type in (Tokenizer.TOKEN_TYPES.PARENOPEN, Tokenizer.TOKEN_TYPES.PARENCLOSE)

    def __init__(self, str_to_parse):
        self.unparsed_string = str_to_parse
        self.tokens = []

        self._parse()

    def _add_token(self, start, end):
        token = self.unparsed_string[start:end].strip()

        if len(token) > 0:
            self.tokens.append(token)

        return end

    def _parse(self):
        start = 0
        current_quote_char = None
        current_token_type = Tokenizer.TOKEN_TYPES.NONE

        for i, char in enumerate(self.unparsed_string):
            if current_quote_char is not None:
                if current_quote_char == char:
                    start = self._add_token(start, i + 1)

                    current_quote_char = None
                    current_token_type = Tokenizer.TOKEN_TYPES.NONE

            else:
                token_type = Tokenizer.get_token_type(char)

                if (token_type != current_token_type or Tokenizer.is_paren_type(
                        token_type)) and current_token_type not in Tokenizer.EMPTY_STIRNG_TYPES:
                    start = self._add_token(start, i)

                if token_type == Tokenizer.TOKEN_TYPES.QUOTEDSTRING:
                    current_quote_char = char

                current_token_type = token_type

        if start != len(self.unparsed_string):
            self._add_token(start, len(self.unparsed_string))

    def __getitem__(self, index):
        return self.tokens[index]

    def __len__(self):
        return len(self.tokens)

    def __eq__(self, other):
        if isinstance(other, Tokenizer):
            return self.tokens == other.tokens
        elif isinstance(other, list) or isinstance(other, tuple):
            return self.tokens == other
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.tokens)
