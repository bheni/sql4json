from evaluation_engine import *

'''
Base class for all nodes created and used by the binary expression
BooleanExpressionTree defines an interface used for evaluating the tree.
'''
class Node(object):
    def evaluate(self):
        raise NotImplementedError("evaluate not implemented")

    def add_child(self, node):
        raise NotImplementedError("add_child not implemented")

    def __str__(self):
        raise NotImplementedError("__str__ not implemented in base EvaluationEngine")

'''
ExpressionNodes contain the tokens of an expression to be evaluated by
the EvaluationEngine.
'''
class ExpressionNode(Node):
    def __init__(self, expression_tokens, evaluation_engine):
        self.expression_tokens = expression_tokens
        self.evaluation_engine = evaluation_engine

    def evaluate(self):
        return self.evaluation_engine.evaluate( self.expression_tokens )

    def __str__(self):
        return ' '.join(self.expression_tokens)

'''
UnaryOperatorNodes evaluate boolean operations on a single operand node
'''
class UnaryOperatorNode(Node):
    OPERATORS = ["!"]

    def __init__(self, operator, operand_node=None):
        self.operator = operator
        self.operand_node = operand_node

    def evaluate(self):
        if self.operator == "!":
            return not self.operand_node.evaluate()
        else:
            raise Exception("Unary operator %s not defined" % self.operator )

    def add_child(self, node):
        if self.operand_node != None:
            node.add_child(self.operand_node)
            
        self.operand_node = node

    def __str__(self):
        operand_str = str(self.operand_node)

        if operand_str.startswith('('):
            return self.operator + operand_str
        else:
            return self.operator + '(' + operand_str + ')'

'''
BinaryOperatorNodes evaluate boolean operations on two operand nodes
'''
class BinaryOperatorNode(Node):
    OPERATORS = ["and", "&&", "or", "||"]

    def __init__(self, operator, operand_node1=None, operand_node2=None):
        self.operator = operator.lower()
        self.operand_node1 = operand_node1
        self.operand_node2 = operand_node2

    def evaluate(self):
        if self.operator == "and" or self.operator == "&&":
            return self.operand_node1.evaluate() and self.operand_node2.evaluate()
        elif self.operator == "or" or self.operator == "||":
            return self.operand_node1.evaluate() or self.operand_node2.evaluate()
        else:
            raise Exception("Binary operator %s not defined" % self.operator)

    def add_child(self, node):
        if self.operand_node1 == None:
            self.operand_node1 = node
        else:
            if self.operand_node2 != None:
                node.add_child(self.operand_node2)

            self.operand_node2 = node

    def is_or_op(self):
        return self.operator in ("or","||")

    def is_and_op(self):
        return self.operator in ("and","&&")

    def insert_child(self):
        raise NotImplementedError("evaluate not implemented")

    def __str__(self):
        return "(" + str(self.operand_node1) + ' ' + self.operator + ' ' + str(self.operand_node2) + ")"