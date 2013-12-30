"""
This class receives callbacks from the BooleanExpressionTree in order to determine if a condition,
is true or false for a specific node.  The BooleanExpressionTree takes care of combining the results
of each condition to determine the results of the entire boolean expression.
"""

from utils import *

from enums import CEnum
from exceptions import WhereClauseException

from boolean_expressions.evaluation_engine import EvaluationEngine


class WhereClauseEvaluationEngine(EvaluationEngine):
    OPERATORS = CEnum(("EQ", "NEQ", "GT", "LT", "GTE", "LTE", "IN"))
    OPERATOR_TOKENS = ("==", "!=", ">", "<", ">=", "<=", "in")
    OPERATOR_TOKENS_SET = frozenset(OPERATOR_TOKENS)

    OPERAND_TYPES = CEnum(("STRING", "INT", "FLOAT", "BOOL", "NULL", "DICTIONARY", "LIST"))
    NUMBER_TYPES = frozenset((OPERAND_TYPES.INT, OPERAND_TYPES.FLOAT))

    def get_operator_index(self, tokens):
        for i, token in enumerate(tokens):
            if token.lower() in WhereClauseEvaluationEngine.OPERATOR_TOKENS_SET:
                return i

        return -1

    def get_operand_type_and_value(self, node, operand):
        if len(operand) == 1:
            if operand[0].isdigit() or (operand[0][0] == '-' and operand[0][1:].isdigit()):
                return WhereClauseEvaluationEngine.OPERAND_TYPES.INT, int(operand[0])

            elif operand[0][0] == operand[0][-1] and (operand[0][0] == '"' or operand[0][0] == "'"):
                return WhereClauseEvaluationEngine.OPERAND_TYPES.STRING, operand[0][1:-1]

            elif operand[0].lower() == "true":
                return WhereClauseEvaluationEngine.OPERAND_TYPES.BOOL, True

            elif operand[0].lower() == "false":
                return WhereClauseEvaluationEngine.OPERAND_TYPES.BOOL, False

            elif operand[0].lower() == "null":
                return WhereClauseEvaluationEngine.OPERAND_TYPES.NULL, None

            else:
                try:
                    return WhereClauseEvaluationEngine.OPERAND_TYPES.FLOAT, float(operand[0])
                except ValueError:
                    pass

        return self.get_value_for_path_and_type(node, operand)

    def get_value_for_path_and_type(self, node, path_tokens):
        found, values = get_elements_by_path_tokens(node, path_tokens)

        if not found:
            return None, None

        value = values[0]

        if value is None:
            return WhereClauseEvaluationEngine.NULL, value

        elif isinstance(value, bool):
            return WhereClauseEvaluationEngine.OPERAND_TYPES.BOOL, value

        elif isinstance(value, float):
            return WhereClauseEvaluationEngine.OPERAND_TYPES.FLOAT, value

        elif isinstance(value, int):
            return WhereClauseEvaluationEngine.OPERAND_TYPES.INT, value

        elif isinstance(value, basestring):
            return WhereClauseEvaluationEngine.OPERAND_TYPES.STRING, value

        elif isinstance(value, dict):
            return WhereClauseEvaluationEngine.OPERAND_TYPES.DICTIONARY, value

        elif isinstance(value, list) or isinstance(value, tuple):
            return WhereClauseEvaluationEngine.OPERAND_TYPES.LIST, value

        raise Exception("Unknown type for %s" % '/'.join(path_tokens))

    def evaluate(self, tokens, node):
        operator_index = self.get_operator_index(tokens)

        if operator_index == -1:
            raise WhereClauseException('"%s" is not a valid expression' % ' '.join(tokens))
        elif operator_index == 0:
            raise WhereClauseException('"%s" missing loperand' % ' '.join(tokens))
        elif operator_index == len(tokens) - 1:
            raise WhereClauseException('"%s" missing roperand' % ' '.join(tokens))
        else:
            operator = WhereClauseEvaluationEngine.OPERATOR_TOKENS.index(tokens[operator_index].lower())
            loperand_tokens = tokens[0:operator_index]
            roperand_tokens = tokens[operator_index + 1:]

            return {
                WhereClauseEvaluationEngine.OPERATORS.EQ: self.evaluate_equality,
                WhereClauseEvaluationEngine.OPERATORS.NEQ: self.evaluate_inequality,
                WhereClauseEvaluationEngine.OPERATORS.GT: self.evaluate_greater_than,
                WhereClauseEvaluationEngine.OPERATORS.GTE: self.evaluate_greater_than_or_equal,
                WhereClauseEvaluationEngine.OPERATORS.LT: self.evaluate_less_than,
                WhereClauseEvaluationEngine.OPERATORS.LTE: self.evaluate_less_than_or_equal,
                WhereClauseEvaluationEngine.OPERATORS.IN: self.evaluate_key_exists
            }[operator](node, loperand_tokens, roperand_tokens)

    def evaluate_equality(self, node, loperand_tokens, roperand_tokens):
        loperand_type, loperand_value = self.get_operand_type_and_value(node, loperand_tokens)
        roperand_type, roperand_value = self.get_operand_type_and_value(node, roperand_tokens)

        if loperand_type == roperand_type or (
                loperand_type in WhereClauseEvaluationEngine.NUMBER_TYPES and roperand_type in WhereClauseEvaluationEngine.NUMBER_TYPES):
            return loperand_value == roperand_value
        else:
            return False

            #raise WhereClauseException("%s and %s are not comparable" % (''.join(loperand_tokens), ''.join(roperand_tokens)) )

    def evaluate_inequality(self, node, loperand_tokens, roperand_tokens):
        return not self.evaluate_equality(node, loperand_tokens, roperand_tokens)

    def evaluate_greater_than(self, node, loperand_tokens, roperand_tokens):
        loperand_type, loperand_value = self.get_operand_type_and_value(node, loperand_tokens)
        roperand_type, roperand_value = self.get_operand_type_and_value(node, roperand_tokens)

        if loperand_type in WhereClauseEvaluationEngine.NUMBER_TYPES and roperand_type in WhereClauseEvaluationEngine.NUMBER_TYPES:
            return loperand_value > roperand_value

        raise WhereClauseException(
            "%s > %s is an invalid operation for these types" % (''.join(loperand_tokens), ''.join(roperand_tokens)))

    def evaluate_greater_than_or_equal(self, node, loperand_tokens, roperand_tokens):
        return not self.evaluate_less_than(node, loperand_tokens, roperand_tokens)

    def evaluate_less_than(self, node, loperand_tokens, roperand_tokens):
        loperand_type, loperand_value = self.get_operand_type_and_value(node, loperand_tokens)
        roperand_type, roperand_value = self.get_operand_type_and_value(node, roperand_tokens)

        if loperand_type in WhereClauseEvaluationEngine.NUMBER_TYPES and roperand_type in WhereClauseEvaluationEngine.NUMBER_TYPES:
            return loperand_value < roperand_value

        raise WhereClauseException(
            "%s < %s is an invalid operation for these types" % (''.join(loperand_tokens), ''.join(roperand_tokens)))

    def evaluate_less_than_or_equal(self, node, loperand_tokens, roperand_tokens):
        return not self.evaluate_greater_than(node, loperand_tokens, roperand_tokens)

    def evaluate_key_exists(self, node, loperand_tokens, roperand_tokens):
        roperand_type, roperand_value = self.get_operand_type_and_value(node, roperand_tokens)

        if roperand_type is None:
            raise WhereClauseException("could not find node at sub path \"%s\"" % ' '.join(roperand_tokens))

        elif roperand_type != WhereClauseEvaluationEngine.OPERAND_TYPES.DICTIONARY:
            raise WhereClauseException(
                '"in" operator can only be used on objects. Item at path "%s"' % ' '.join(roperand_tokens))

        else:
            found, nodes = get_elements_by_path_tokens(roperand_value, loperand_tokens)
            return found

