import unittest

from sql4json.tokenizer import *

class TokenizerTests(unittest.TestCase):
    def test_tokenizer_init(self):
        tokenizer = Tokenizer('test')
        
        self.assertEqual("test", tokenizer.unparsed_string)
        self.assertEqual(["test"], tokenizer.tokens)

    def test_add_tokens(self):
        tokenizer = Tokenizer('')

        tokenizer.unparsed_string = 'this is a test'
        
        self.assertEqual( 4, tokenizer._add_token(0, 4) )
        self.assertEqual( 7, tokenizer._add_token(5, 7) )
        self.assertEqual( 9, tokenizer._add_token(7, 9) )
        self.assertEqual( 14, tokenizer._add_token(9, 14) )
        self.assertEqual( ["this", "is", "a", "test"], tokenizer )

    def test_tokenizer_is_iterable(self):
        tokenizer = Tokenizer("test 1 2 test1234 a b ab_12")

        expected = ["test","1","2","test1234","a","b","ab_12"]

        for i,token in enumerate(tokenizer):
            self.assertEqual(expected[i], token)

    def test_chars_classified_properly(self):
        for i in range(ord(' '), 126):
            char = chr(i)
            token_type = Tokenizer.get_token_type(char)

            if char.isdigit() or char.isalpha() or char == '_':
                self.assertEqual(Tokenizer.TOKEN_TYPES.ALPHANUM, token_type)
            elif char == ' ' or char == '\t' or char == '\n' or char == '\n':
                self.assertEqual(Tokenizer.TOKEN_TYPES.WHITESPACE, token_type)
            elif char == '"' or char == "'":
                self.assertEqual(Tokenizer.TOKEN_TYPES.QUOTEDSTRING, token_type)
            elif char == '(':
                self.assertEqual(Tokenizer.TOKEN_TYPES.PARENOPEN, token_type)
            elif char == ')':
                self.assertEqual(Tokenizer.TOKEN_TYPES.PARENCLOSE, token_type)
            else:
                self.assertEqual(Tokenizer.TOKEN_TYPES.SYMBOL, token_type)

    def test_len(self):
        tokenizer = Tokenizer("test 1 2 test1234 a b ab_12")
        self.assertEqual(7, len(tokenizer))

    def test_tokenize_words(self):
        tokenizer = Tokenizer("test 1 2 test1234 a b ab_12")

        self.assertEqual(["test","1","2","test1234","a","b","ab_12"], tokenizer)

    def test_tokenize_operators(self):
        tokenizer = Tokenizer("test!=12&&test!=14 and other_test == 8")

        self.assertEqual(["test","!=","12","&&","test","!=","14","and","other_test","==","8"], tokenizer)

    def test_tokenize_quoted_strings(self):
        tokenizer = Tokenizer('''test == 'blue ball' or test =="123+123 == 246"''');

        self.assertEqual(["test","==","'blue ball'","or","test","==",'"123+123 == 246"'], tokenizer)

    def test_tokenize_strings_with_parenthesis(self):
        tokenizer = Tokenizer('''test==1&&(test2==3 or testA=="b") && (x ==3)''');

        self.assertEqual(["test","==","1","&&","(","test2","==","3","or","testA","==",'"b"',")","&&","(","x","==","3",")"], tokenizer)

    def test_tokenize_full_sql_query(self):
        tokenizer = Tokenizer('''
            SELECT *
            FROM data
            WHERE (id in / or time>0) and test == "value"
        ''')

        self.assertEqual(["SELECT", "*", "FROM", "data", "WHERE", "(", "id", "in", "/", "or", "time", ">", "0", ")", "and", "test", "==", '"value"'], tokenizer)