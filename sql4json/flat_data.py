class FlatData(object):
    def __init__(self, data, order=None):
        self.data = data
        self.columns = []
        self.table = {}
        self.headers = []
        self.rows = []
        self.order = order

        self.flatten_data()

    def flatten_data(self):
        row_count = 0

        if isinstance(self.data, list) or isinstance(self.data, tuple):
            for node in self.data:
                self.flatten_node(node, row_count)
                row_count += 1
        else:
            self.flatten_node(self.data, 0)
            row_count = 1

        self.transpose_table(row_count)

    def flatten_node(self, node, row_count):
        self.extract_data_from_node('', node, '', row_count)

        for column in self.columns:
            if len(self.table[column]) != (row_count + 1):
                self.table[column].append(None)

    def extract_data_from_node(self, name, node, path, row_count):
        if isinstance(node, list) or isinstance(node, tuple):
            for i, child in enumerate(node):
                self.extract_data_from_node(name + '[' + str(i) + ']', child, path, row_count)
        elif isinstance(node, dict):
            for key, value in iter(sorted(node.iteritems())):
                if path == '' and name == '':
                    new_path = ''
                else:
                    new_path = path + name + '/'

                self.extract_data_from_node(key, value, new_path, row_count)
        else:
            column_name = path + name

            if column_name not in self.columns:
                self.add_new_colunm(column_name, row_count)

            self.table[column_name].append(node)

    def add_new_colunm(self, column_name, row_count):
        if row_count == 0:
            self.table[column_name] = []
        else:
            self.table[column_name] = [None] * row_count

        self.columns.append(column_name)

    def get_ordered_columns(self):
        if self.order is None:
            return self.columns
        else:
            ordered_columns = []

            for column in self.order:
                if column not in self.columns:
                    raise Exception('Unknown column ' + column)
                else:
                    ordered_columns.append(column)

            for column in self.columns:
                if column not in ordered_columns:
                    ordered_columns.append(column)

            return ordered_columns

    def transpose_table(self, row_count):
        for i in range(row_count):
            self.rows.append([])

        ordered_columns = self.get_ordered_columns()

        for column in ordered_columns:
            self.headers.append(column)
            column_data = self.table[column]

            for i, value in enumerate(column_data):
                self.rows[i].append(value)

    def get_headers(self):
        return self.headers

    def get_rows(self):
        return self.rows
