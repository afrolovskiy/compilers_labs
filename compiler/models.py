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
        self.type = 'statement'


class IFStatement(Statement):
        def __init__(self):
            self.type = 'if-statement'
            self.condition = None
            self.success_expression = None
            self.failed_expression = None


class WhileStatement(Statement):
        def __init__(self):
            self.type = 'while-statement'
            self.condition = None
            self.expression = None


class PrintStatement(Statement):
    def __init__(self): 
        self.type = 'print-statement'
        self.expression = None


class AssignmentStatement(Statement):
    def __init__(self):
        self.type = 'assignment-statement'
        self.left_part = None
        self.right_part = None


class Expression(Cornerstone):
    def __init__(self):
        self.type = 'expression'


class ArrayElementExpression(Expression):
    def __init__(self):
        self.type = 'array-element-expression'
        self.array = None
        self.index = None


class LengthExpression(Expression):
    def __init__(self):
        self.type = 'length-expression'
        self.class_name = None


class CallMethodExpression(Expression):
    def __init__(self):
        self.type = 'call-expression'
        self.class_name = None
        self.method_name = None
        self.args = []


class BinaryArithmeticExpression(Expression):
    def __init__(self):
        self.type = 'binary-arithmetic-expression'
        self.operator = None
        self.operand1 = None
        self.operand2 = None


class ParenthesisExpression(Expression):
    def __init__(self):
        self.type = 'parenthesis-expression'
        self.operand = None


class UnaryArithmeticExpression(Expression):
    def __init__(self):
        self.type = 'unary-arithmetic-expression'
        self.operator = None
        self.operand = None


class NewExpression(Expression):
    def __init__(self): 
        self.type = 'new-expression'
        self.type_name = None


class NewArrayExpression(NewExpression):
    def __init__(self): 
        super(NewExpression, self).__init__()
        self.type = 'new-array-expression'


class ValueExpression(Expression):
    def __init__(self):
        self.type = 'value-expression'
        self.value = None


class BooleanExpression(ValueExpression):
    def __init__(self):
        super(BooleanExpression, self).__init__()
        self.type = 'boolean-expression'


class NullExpression(ValueExpression):
    def __init__(self):
        super(NullExpression, self).__init__()
        self.type = 'value-expression'


class ThisExpression(Expression):
    def __init__(self):
        super(ThisExpression, self).__init__()
        self.type = 'this-expression'


class IdentifierExpression(ValueExpression):
    def __init__(self):
        super(IdentifierExpression, self).__init__()
        self.type = 'identifier-expression'


class IntegerExpression(ValueExpression):
    def __init__(self):
        super(IntegerExpression, self).__init__()
        self.type = 'integer-expression'






