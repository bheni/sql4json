import json as regular_json

try:
    import ujson as json_loader
except ImportError:
    json_loader = regular_json

from data_query_engine import DataQueryEngine


class Sql4Json(object):
    def __init__(self, json_str, sql_str):
        self.data = json_loader.loads(json_str)
        self.query_engine = DataQueryEngine(self.data, sql_str)

    def get_results(self):
        return self.query_engine.get_results()

    def __str__(self):
        return regular_json.dumps(self.query_engine.get_results(), sort_keys=True, indent=4, separators=(',', ': '))