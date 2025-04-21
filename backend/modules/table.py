"""Tabular data module

Provide basic functionalities for tabular data.
"""

from . import RecordContentHandler

class TableModel:
    def __init__(self, data: list[dict]):
        self.data = data
    
    def to_json(self):
        pass

class TableHandler(RecordContentHandler):
    def __init__(self, module_name: str):
        self.module_name = module_name

    def register_api(self, blueprint):
        @blueprint.route(f"/modules/{self.module_name}/data/<path:filename>", methods=['GET'])
        def get_data(filename):
            # non-default methods for specific data
            pass