import json


class Cornerstone(object):
    pass


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Cornerstone):
            return super(JSONEncoder, self).default(obj)
        return obj.__dict__


class Programm(Cornerstone):
    def __init__(self):
        self.exemplar = 'programm'
        self.main_class = None
        self.classes = []


class Class(Cornerstone):
    def __init__(self):
        self.exemplar = 'class'
        self.name = None
        self.variables = []
        self.methods = []        
        self.extends = None


class Method(Cornerstone):
    def __init__(self): 
        self.exemplar = 'method'
        self.return_type = None
        self.name = None
        self.args = []
        self.variables = []
        self.statements = []


class Variable(Cornerstone):
    def __init__(self):
        self.exemplar = 'variable'
        self.type = None
        self.name = None
        self.value = None


class Argument(Cornerstone):
    def __init__(self): 
        self.exemplar = 'argument'
        self.type = None
        self.name = None


class Type(Cornerstone):
    def __init__(self):
        self.exemplar = 'type'
        self.name = None

class ArrayType(Type):
    def __init__(self):
        super(ArrayType, self).__init__()
        self.exemplar = 'array-type'


class Statement(Cornerstone):
    def __init__(self):
        self.exemplar = 'statement'


class IFStatement(Statement):
        def __init__(self):
            self.exemplar = 'if-statement'
            self.condition = None
            self.success_expression = None
            self.failed_expression = None


class WhileStatement(Statement):
        def __init__(self):
            self.exemplar = 'while-statement'
            self.condition = None
            self.expression = None


class PrintStatement(Statement):
    def __init__(self): 
        self.exemplar = 'print-statement'
        self.expression = None


class AssignmentStatement(Statement):
    def __init__(self):
        self.exemplar = 'assignment-statement'
        self.left_part = None
        self.right_part = None


class Expression(Cornerstone):
    def __init__(self):
        self.exemplar = 'expression'


class ArrayElementExpression(Expression):
    def __init__(self):
        self.exemplar = 'array-element-expression'
        self.array = None
        self.index = None


class FieldExpression(Expression):
    def __init__(self):
        self.exemplar = 'field-expression'
        self.expression = None
        self.identifier = None


class CallMethodExpression(Expression):
    def __init__(self):
        self.exemplar = 'call-expression'
        self.expression = None
        self.method_name = None
        self.args = []


class BinaryArithmeticExpression(Expression):
    def __init__(self):
        self.exemplar = 'binary-arithmetic-expression'
        self.operator = None
        self.operand1 = None
        self.operand2 = None


class ParenthesisExpression(Expression):
    def __init__(self):
        self.exemplar = 'parenthesis-expression'
        self.operand = None


class UnaryArithmeticExpression(Expression):
    def __init__(self):
        self.exemplar = 'unary-arithmetic-expression'
        self.operator = None
        self.operand = None


class NewExpression(Expression):
    def __init__(self): 
        self.exemplar = 'new-expression'
        self.type_name = None


class NewArrayExpression(NewExpression):
    def __init__(self): 
        super(NewExpression, self).__init__()
        self.exemplar = 'new-array-expression'


class ValueExpression(Expression):
    def __init__(self):
        self.exemplar = 'value-expression'
        self.value = None


class BooleanExpression(ValueExpression):
    def __init__(self):
        super(BooleanExpression, self).__init__()
        self.exemplar = 'boolean-expression'


class NullExpression(ValueExpression):
    def __init__(self):
        super(NullExpression, self).__init__()
        self.exemplar = 'value-expression'


class ThisExpression(Expression):
    def __init__(self):
        super(ThisExpression, self).__init__()
        self.exemplar = 'this-expression'


class IdentifierExpression(Expression):
    def __init__(self):
        self.exemplar = 'identifier-expression'
        self.name = None


class IntegerExpression(ValueExpression):
    def __init__(self):
        super(IntegerExpression, self).__init__()
        self.exemplar = 'integer-expression'






