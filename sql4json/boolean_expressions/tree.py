"""
BooleanExpressionTree takes a tokenized binary expression such as:

    value == 2 && !(key in set or y == "some string" || myfunction(param1,"const param 2"))

and generates a tree of nodes used to evaluate the expression.  The EvaluationEngine which
is passed as a parameter to the constructor is used in evaluating each condition.  Example
condition tokens which would be passed to the evaluation engine include:

    ['value', '==', '2']
    ['key', 'in', 'set']
    ['y', '==', '"some string"']
    ['myfunction','(','param1','const param 2', ')']
"""

from tree_nodes import *
from exceptions import *


class BooleanExpressionTree(Node):
    def __init__(self, expression_tokens, evaluation_engine):
        self.expression_tokens = expression_tokens
        self.evaluation_engine = evaluation_engine

        self.root = self._build_tree(self.expression_tokens)

    def _build_tree(self, tokens):
        token_index = 0
        num_tokens = len(tokens)
        root_node = None
        last_operator = None
        should_read_operand = True

        while token_index < num_tokens:
            current = tokens[token_index]

            if should_read_operand:
                token_index, new_node = self._read_operand(tokens, token_index)
            else:
                token_index, new_node = self._read_binary_operator(tokens, token_index)

            if new_node is not None:
                root_node, last_operator = self._add_new_node_to_tree(new_node, root_node, last_operator)

            should_read_operand = not should_read_operand
            token_index += 1

        return root_node

    def _read_operand(self, tokens, token_index):
        new_node = None
        current_token = tokens[token_index]

        if current_token in UnaryOperatorNode.OPERATORS:
            new_node = UnaryOperatorNode(current_token)
        else:
            if current_token == '(':
                end_enclosed_index, enclosed_tokens = self._parse_out_tokens_between_parenthesis(tokens, token_index)

                if any(token.lower() in BinaryOperatorNode.OPERATORS for token in enclosed_tokens):
                    new_node = self._build_tree(enclosed_tokens)
                    token_index = end_enclosed_index

            if new_node is None:
                token_index, new_node = self._parse_expression_node(token_index, tokens)

        if isinstance(new_node, UnaryOperatorNode):
            token_index, child_node = self._read_operand(tokens, token_index + 1)
            new_node.add_child(child_node)

        return token_index, new_node

    def _read_binary_operator(self, tokens, token_index):
        current = tokens[token_index]

        if current not in BinaryOperatorNode.OPERATORS:
            raise Exception()
        else:
            return token_index, BinaryOperatorNode(current)


    def _parse_out_tokens_between_parenthesis(self, tokens, starting_index=0):
        if tokens[starting_index] != '(':
            raise Exception("_parse_out_tokens_between_parenthesis should be called with openning paren '('")

        paren_count = 0

        for i in range(starting_index, len(tokens)):
            current = tokens[i]

            if current == '(':
                paren_count += 1
            elif current == ')':
                paren_count -= 1

            if paren_count == 0:
                num_tokens = i - (starting_index + 1)

                if num_tokens > 0:
                    return i, tokens[starting_index + 1: i]
                else:
                    raise BooleanExpressionException(
                        "Empty expression () in:\r\n\t%s" % ''.join(self.expression_tokens))

        raise BooleanExpressionException("Parenthesis mismatch in:\r\n\t%s" % ''.join(self.expression_tokens))


    def _parse_expression_node(self, token_index, tokens):
        num_tokens = len(tokens)
        expression_tokens = []
        paren_count = 0
        done = False

        while token_index < num_tokens:
            current_token = tokens[token_index]

            if current_token in BinaryOperatorNode.OPERATORS:
                done = True
                token_index -= 1
            elif token_index == num_tokens - 1:
                done = True
            elif current_token == '(':
                paren_count += 1
            elif current_token == ')':
                paren_count -= 1

            if paren_count < 0:
                raise BooleanExpressionException("Parenthesis mismatch in:\r\n\t%s" % ''.join(self.expression_tokens))

            if not done or token_index == num_tokens - 1:
                expression_tokens.append(current_token)
                token_index += 1

            if done:
                break

        if expression_tokens[0] == '(' and expression_tokens[-1] == ')' and len(expression_tokens) > 2:
            expression_tokens = expression_tokens[1:-1]

        return token_index, ExpressionNode(expression_tokens, self.evaluation_engine)

    def _add_new_node_to_tree(self, new_node, root_node, last_operator):
        is_binary_op = isinstance(new_node, BinaryOperatorNode)
        is_sub_tree = is_binary_op and (new_node.operand_node1 is not None and new_node.operand_node2 is not None)

        if root_node is None:
            root_node = new_node

        elif is_binary_op and last_operator is None:
            new_node.add_child(root_node)
            root_node = new_node
        elif last_operator is not None:
            if is_binary_op and new_node.is_and_op():
                last_operator.add_child(new_node)
            elif is_binary_op:
                new_node.add_child(root_node)
                root_node = new_node
            else:
                last_operator.add_child(new_node)
        else:
            new_node.add_child(root_node)
            root_node = new_node

        if is_binary_op and not is_sub_tree:
            last_operator = new_node

        return root_node, last_operator

    def evaluate(self, evaluation_param):
        if self.root is not None:
            return self.root.evaluate(evaluation_param)
        else:
            raise BooleanExpressionException('empty expressions can not be evaluated')

    def __str__(self):
        return str(self.root)

