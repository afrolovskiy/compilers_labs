
class Node:
    def __init__(self, type, children=[]):
        self.type = type
        self.children = children
	self.value = None
	self.attrs = {}

class Type_node:
    def __init__(self, type, dim):
        self.type = type
        self.dim = dim

class Var_node:
    def __init__(self, type, name):
        self.type = type
        self.name = name

class Method_node:
    def __init__(self, type, name, args=[], vars=[]):
        self.type = type
        self.name = name
        self.args = args
        self.vars = vars

class Class_node:
    def __init__(self, name, fields = [], methods = []):
        self.name = name
        self.fields = fields
        self.methods = methods
    
class Table:
    def __init__ (self):
        self.classes = []
