from exceptions import *
from sql_statement import SQLStatement
from where_clause_evaluation_engine import *

from boolean_expressions.tree import BooleanExpressionTree


class DataQueryEngine(object):
    where_evaluation_engine = WhereClauseEvaluationEngine()

    def __init__(self, data, sql_str):
        self.data = data
        self.sql_statement = SQLStatement(sql_str)
        self.results = None
        self.from_roots = None
        self.where_tree = None

        self.init_from_roots()
        self.init_where_boolean_tree()

        self.query()
        self.sort()
        self.apply_limit()

    def init_from_roots(self):
        from_section = self.sql_statement.get_from_section()

        if from_section is not None and len(from_section) > 0:
            exists, self.from_roots = get_elements_by_path(self.data, from_section)

            if not exists or len(self.from_roots) == 0:
                raise FromClauseException("Could not find path %s." % from_section)
        else:
            self.from_roots = [self.data]

    def init_where_boolean_tree(self):
        self.where_tree = None
        where_section = self.sql_statement.get_where_section()

        if where_section is not None and len(where_section) > 0:
            tokenizer = Tokenizer(where_section)
            where_tokens = list(tokenizer)

            if where_tokens is not None and len(where_tokens) > 0:
                self.where_tree = BooleanExpressionTree(where_tokens, DataQueryEngine.where_evaluation_engine)

    def query(self):
        select_section = self.sql_statement.get_select_section()
        select_items = split_on_any(select_section, frozenset((',', ' ', '\t', '\n', '\r')))

        self.results = []

        for root in self.from_roots:
            if isinstance(root, tuple) or isinstance(root, list):

                for node in root:
                    result_data = self.query_node(node, select_items)

                    if result_data is not None:
                        self.results.append(result_data)

            elif isinstance(root, dict):
                results = self.query_node(root, select_items)

                if results is not None:
                    self.results.append(results)

    def query_node(self, node, select_items):
        if self.matches_where(node):
            node_data = {}
            for item in select_items:
                if item.endswith('/'):
                    item += '*'

                selecet_path_elements = split_on_any(item, frozenset(('/', '\\', '.')))
                select_data = self.find_selected_items(node, selecet_path_elements)

                if select_data is not None:
                    node_data.update(select_data)

            return node_data

        else:
            return None

    def find_selected_items(self, node, select_path_elements):
        matching_data = {}

        current = node
        destination = matching_data
        parent_dest = matching_data
        current_key = None
        element = None

        num_elements = len(select_path_elements)
        for i, element in enumerate(select_path_elements):
            if i < num_elements - 1:
                if element not in current:
                    return None
                elif element not in destination:
                    destination[element] = {}

                current_key = element
                current = current[element]
                parent_dest = destination
                destination = destination[element]
            else:
                if element == '*':
                    if current_key is not None:
                        parent_dest[current_key] = current
                    else:
                        matching_data = current
                if element == '__key__':
                    parent_dest['__key__'] = current.keys()
                else:
                    if element in current:
                        destination[element] = current[element]
                    else:
                        destination[element] = None

        return matching_data

    def matches_where(self, node):
        if self.where_tree is None:
            return True
        else:
            return self.where_tree.evaluate(node)

    def sort(self):
        pass

    def apply_limit(self):
        limit = self.sql_statement.get_limit_section()

        if limit is not None:
            if len(limit) != 1 or not limit[0].isdigit():
                raise LimitClauseException('"%s" is not a valid limit' % ' '.join(limit))
            else:
                limit = int(limit)

                while len(self.results) > limit:
                    self.results.pop()

    def get_results(self):
        return self.results

    def get_sql_statement(self):
        return self.sql_statement

