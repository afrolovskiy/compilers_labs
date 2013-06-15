import json


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Node):
            return super(JSONEncoder, self).default(obj)
        return obj.__dict__


class Node:
    def __init__(self, type, children=[]):
        self.type = type
        self.children = children

