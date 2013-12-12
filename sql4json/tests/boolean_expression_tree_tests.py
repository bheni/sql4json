import unittest

from sql4json.tokenizer import Tokenizer

from sql4json.boolean_expressions.tree import BooleanExpressionTree
from sql4json.boolean_expressions.tree_nodes import *
from sql4json.boolean_expressions.evaluation_engine import *
from sql4json.boolean_expressions.exceptions import *

class TestEvaluationEngine(object):
    def evaluate(self, tokens, evaluation_param):
        return eval( ''.join(tokens) )

test_engine = TestEvaluationEngine()

class ExpressionNodeTests(unittest.TestCase):
    def test_evaluate_expression_node(self):
        tokenizer = Tokenizer("5 == 6")
        node = ExpressionNode( list(tokenizer),  test_engine)

        self.assertFalse( node.evaluate(None) )

        tokenizer = Tokenizer('"matching strings" == "matching strings"')
        node = ExpressionNode( list(tokenizer),  test_engine)

        self.assertTrue( node.evaluate(None) )

    def test_str(self):
        tokenizer = Tokenizer("5 == 6")
        node = ExpressionNode( list(tokenizer),  test_engine)

        self.assertEqual("5 == 6", str(node))

class BinaryOperatorNodeTests(unittest.TestCase):
    def test_expression_node_type(self):
        tokenizer = Tokenizer("5 == 6")
        node1 = ExpressionNode( list(tokenizer),  test_engine)

        tokenizer = Tokenizer('"matching strings" == "matching strings"')
        node2 = ExpressionNode( list(tokenizer),  test_engine)

        binary_node = BinaryOperatorNode("&&", node1, node2)

        self.assertFalse( binary_node.evaluate(None) )

        binary_node = BinaryOperatorNode("||", node1, node2)

        self.assertTrue( binary_node.evaluate(None) )                

    def test_str(self):
        tokenizer = Tokenizer("5 == 6")
        node1 = ExpressionNode( list(tokenizer),  test_engine)

        tokenizer = Tokenizer('"matching strings" == "matching strings"')
        node2 = ExpressionNode( list(tokenizer),  test_engine)

        binary_node = BinaryOperatorNode("&&", node1, node2)

        self.assertEqual('(5 == 6 && "matching strings" == "matching strings")', str(binary_node))

class UnaryOperatorNodeTests(unittest.TestCase):
    def test_evaluate_unary_node(self):
        tokenizer = Tokenizer("5 == 6")
        node = ExpressionNode( list(tokenizer),  test_engine)
        unary_node = UnaryOperatorNode("!", node)

        self.assertTrue( unary_node.evaluate(None) )

        tokenizer = Tokenizer('"matching strings" == "matching strings"')
        node = ExpressionNode( list(tokenizer),  test_engine)
        unary_node = UnaryOperatorNode("!", node)

        self.assertFalse( unary_node.evaluate(None) )

    def test_str(self):
        tokenizer = Tokenizer("5 == 6")
        node = ExpressionNode( list(tokenizer),  test_engine)
        unary_node = UnaryOperatorNode("!", node)

        self.assertEqual("!(5 == 6)", str(unary_node) )


class BooleanExpressionTreeTests(unittest.TestCase):
    def test_process_simple_expression(self):
        tree = BooleanExpressionTree(["x","==","7"], test_engine)

        self.assertEqual("x == 7", str(tree))
        
    def test_process_simple_function(self):
        tree = BooleanExpressionTree(["func","(","arg1",",","arg2",")"], test_engine)

        self.assertEqual("func ( arg1 , arg2 )", str(tree))
        

    def test_process_expression_with_paranthesis(self):
        tree = BooleanExpressionTree(["(","x","==","7",")"], test_engine)

        self.assertEqual("( x == 7 )", str(tree))

    def test_process_expression_preceeded_by_unary_not(self):
        tokenizer = Tokenizer("!(5 == 6)")
        tree = BooleanExpressionTree(list(tokenizer), test_engine)

        self.assertEqual("!( 5 == 6 )", str(tree))
        self.assertTrue( tree.evaluate(None) )

    def test_process_two_expressions_and_binary_and(self):
        tokenizer = Tokenizer("!(5 == 6) && abs(-1) == 1")
        tree = BooleanExpressionTree(list(tokenizer), test_engine)

        self.assertEqual("(!( 5 == 6 ) && abs ( - 1 ) == 1)", str(tree))
        self.assertTrue( tree.evaluate(None) )

    def test_process_two_expressions_and_binary_or(self):
        tokenizer = Tokenizer("!( 5 == 6 ) || abs(-1) == 1")
        tree = BooleanExpressionTree(list(tokenizer), test_engine)

        self.assertEqual("(!( 5 == 6 ) || abs ( - 1 ) == 1)", str(tree))
        self.assertTrue( tree.evaluate(None) )

    def test_only_necessary_conditions_evaluated(self):
        tokenizer = Tokenizer('!( 5 == 6 ) || unimplementedfunction("shouldnt get run because first condition passes")')
        tree = BooleanExpressionTree(list(tokenizer), test_engine)
        self.assertTrue( tree.evaluate(None) )

        tokenizer = Tokenizer('( 5 == 6 ) && unimplementedfunction("shouldnt get run because first condition passes")')
        tree = BooleanExpressionTree(list(tokenizer), test_engine)
        self.assertFalse( tree.evaluate(None) )

        try:
            tokenizer = Tokenizer('(5 == 6) || unimplementedfunction("shouldnt get run because first condition passes")')
            tree = BooleanExpressionTree(list(tokenizer), test_engine)
            tree.evaluate(None)
            self.fail()
        except Exception, e:
            pass

        try:
            tokenizer = Tokenizer('!(5 == 6) && unimplementedfunction("shouldnt get run because first condition passes")')
            tree = BooleanExpressionTree(list(tokenizer), test_engine)
            tree.evaluate(None)
            self.fail()
        except Exception, e:
            pass

    def test_parenthesis(self):
        try:
            tokenizer = Tokenizer('unimplementedfunction() || True || False')
            tree = BooleanExpressionTree(list(tokenizer), test_engine)
            tree.evaluate(None)
            self.fail()
        except Exception, e:
            pass

        tokenizer = Tokenizer('unimplementedfunction() || (True || False)')
        tree = BooleanExpressionTree(list(tokenizer), test_engine)
        self.assertTrue( tree.evaluate(None) )

    def test_complex_expression(self):
        tokenizer = Tokenizer('value == 2 && !(key in set or y == "some string" || myfunction(param1,"const param 2"))')
        tree = BooleanExpressionTree(list(tokenizer), test_engine)
        self.assertEqual('(value == 2 && !((key in set or y == "some string") || myfunction ( param1 , "const param 2" )))', str(tree))



