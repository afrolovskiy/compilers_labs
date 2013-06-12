import json
from ply import yacc
from lexer import tokens
#import ipdb
from models import (
    JSONEncoder, Programm, Class, Method, Variable, Type, ArrayType,
    Argument, IFStatement, WhileStatement, PrintStatement, AssignmentStatement,
    ArrayElementExpression, LengthExpression, CallMethodExpression,
    BinaryArithmeticExpression, ParenthesisExpression, UnaryArithmeticExpression,
    NewExpression, NewArrayExpression, IdentifierExpression, IntegerExpression,
    BooleanExpression, NullExpression, ThisExpression)


start = 'programm'

def p_programm(p):
    'programm : main_class class_list'
    p[0] = Programm()
    p[0].main_class = p[1]
    p[0].classes = p[2]

def p_empty(p):
    'empty :'

def p_empty_class_list(p):
    '''
    class_list : empty 
    '''
    p[0] = []

def p_class_list(p):
    '''
    class_list : class class_list
    '''
    p[0] = p[2]
    p[0].append(p[1])

def p_main_class(p):
    '''
    main_class : CLASS IDENTIFIER LEFT_BRACE main_method RIGHT_BRACE
    '''
    p[0] = Class()
    p[0].name = p[2]
    p[0].methods.append(p[4])

def p_main_method(p):
    '''
    main_method : PUBLIC STATIC VOID MAIN LEFT_PARENTHESIS STRING LEFT_BRACKET RIGHT_BRACKET IDENTIFIER RIGHT_PARENTHESIS LEFT_BRACE var_list statement_list RIGHT_BRACE
    '''
    arg = Argument()
    arg.type = ArrayType()
    arg.type.name = 'String'
    arg.name = p[9]

    p[0] = Method()
    p[0].name = p[4]
    p[0].args.append(arg)
    p[0].variables = p[12]
    p[0].statements = p[13]
    p[0].return_type = Type()
    p[0].return_type.name = 'void'

def p_class(p):
    '''
    class : CLASS IDENTIFIER extends LEFT_BRACE declaration_list RIGHT_BRACE
    '''
    p[0] = Class()
    p[0].name = p[2]
    for field in p[5]:
        if isinstance(field, Variable):
            p[0].variables.append(field)
        elif isinstance(field, Method):
            p[0].methods.append(field)
    p[0].extends = p[3]

def p_empty_extends(p):
    '''
    extends : empty
    '''
    p[0] = None

def p_extends(p):
    '''
    extends : EXTENDS IDENTIFIER
    '''
    p[0] = p[2]

def p_empty_declaration_list(p):
    """
    declaration_list : empty
    """
    p[0] = []

def p_declaration_list(p):
    """
    declaration_list : field declaration_list
                           | method declaration_list
    """
    p[0] = p[2]
    p[0].append(p[1])    

def p_field(p):
    """
    field : type IDENTIFIER SEMICOLON
    """
    p[0] = Variable()
    p[0].type = p[1]
    p[0].name = p[2]

def p_method(p):
    """
    method : PUBLIC type IDENTIFIER LEFT_PARENTHESIS params_list RIGHT_PARENTHESIS LEFT_BRACE var_list statement_list RETURN expression SEMICOLON RIGHT_BRACE
    """
    p[0] = Method()
    p[0].return_type = p[2]
    p[0].name = p[3]
    p[0].args = p[5]
    p[0].variables= p[8]
    p[0].statements = p[9]

def p_empty_params_list(p):
    """
    params_list : empty
    """
    p[0] = []

def p_params_list(p):
    """
    params_list : args_list
    """
    p[0] = p[1]

def p_single_args_list(p):
    """
    args_list : arg
    """
    p[0] = [p[1], ]

def p_args_list(p):
    """
    args_list : arg COMMA args_list
    """
    p[0] = p[3]
    p[0].append(p[1])

def p_arg(p):
    '''
    arg : type IDENTIFIER
    '''
    p[0] = Argument()
    p[0].type = p[1]
    p[0].name = p[2]

def p_empty_var_list(p):
    """
    var_list : empty
    """
    p[0] = []

def p_var_list(p):
    """
    var_list : var var_list
    """
    p[0] = p[2]
    p[0].append(p[1])

def p_var(p):
    """
    var : type IDENTIFIER SEMICOLON
    """
    p[0] = Variable()
    p[0].type = p[1]
    p[0].name = p[2]

def p_var_with_value(p):
    """
    var : type IDENTIFIER ASSIGNMENT expression SEMICOLON
    """
    p[0] = Variable()
    p[0].type = p[1]
    p[0].name = p[2]
    p[0].value = p[3]

def p_empty_statement_list(p):
    """
    statement_list : empty
    """
    p[0] = []

def p_statement_list(p):
    """
    statement_list : statement statement_list
    """
    p[0] = p[2]
    p[0].append(p[1])

def p_simple_type(p):
    '''
    type : BOOLEAN 
           | INT
           | IDENTIFIER
    '''
    p[0] = Type()
    p[0].name = p[1]

def p_array_type(p):
    '''
    type : BOOLEAN LEFT_BRACKET RIGHT_BRACKET
           | INT LEFT_BRACKET RIGHT_BRACKET
           | IDENTIFIER LEFT_BRACKET RIGHT_BRACKET
    '''
    p[0] = ArrayType()
    p[0].name = p[1]

def p_block_statement(p):
    '''
    statement : LEFT_BRACE statement_list RIGHT_BRACE
    '''
    p[0] = p[2]

def p_statement(p):
    '''
    statement : if_statement 
                    | while_statement 
                    | print_statement 
                    | assignment_statement 
    '''
    p[0] = p[1]

def p_if_statement(p):
    '''
    if_statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement
    '''
    p[0] = IFStatement()
    p[0].condition = p[3]
    p[0].success_expression = p[5]

def p_if_else_statement(p):
    '''
    if_statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement ELSE statement
    '''
    p[0] = IFStatement()
    p[0].condition = p[3]
    p[0].success_expression = p[5]
    p[0].failed_expression = p[7]

def p_while_statement(p):
    '''
    while_statement : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement
    ''' 
    p[0] = WhileStatement()
    p[0].condition = p[3]
    p[0].expression = p[5]

def p_print_statement(p):
    '''
    print_statement : SYSTEM POINT OUT POINT PRINTLN LEFT_PARENTHESIS expression RIGHT_PARENTHESIS SEMICOLON
    '''
    p[0] = PrintStatement()
    p[0].expression = p[7]

def p_assignment_statement(p):
    '''
    assignment_statement : expression ASSIGNMENT expression SEMICOLON
    '''
    p[0] = AssignmentStatement()
    p[0].left_part = p[1]
    p[0].right_part = p[3]

def p_expression(p):
    '''
    expression : array_element_expression 
                     | length_expression
                     | call_method_expression
                     | binary_expression
                     | parenthesis_expression
                     | unary_expression
                     | new_expression
                     | new_array_expression
                     | identifier_expression
                     | integer_literal_expression
                     | boolean_expression
                     | this_expression
                     | null_expression
    '''
    p[0] = p[1]

def p_array_element_expression(p):
    '''
    array_element_expression : expression LEFT_BRACKET expression RIGHT_BRACKET
    '''
    p[0] = ArrayElementExpression()
    p[0].array = p[1]
    p[0].index = p[3]

def p_lenght_expression(p):
    '''
    length_expression : expression POINT LENGTH
    '''
    p[0] = LengthExpression()
    p[0].expression = p[1]

def p_call_method_expression(p):
    '''
    call_method_expression : expression POINT IDENTIFIER LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
    '''
    p[0] = CallMethodExpression()
    p[0].expression = p[1]
    p[0].method_name = p[3]
    p[0].args = p[5]

def p_single_expression_list(p):
    '''
    expression_list : expression
    '''
    p[0] = [p[1], ]

def p_expression_list(p):
    '''
    expression_list : expression COMMA expression_list
    '''
    p[0] = p[3]
    p[0].append(p[1])

def p_binary_expression(p):
    '''
    binary_expression : expression OR expression
                               | expression AND expression
                               | expression EQUAL expression
                               | expression NOT_EQUAL expression
                               | expression GREATER expression
                               | expression LESS expression
                               | expression PLUS expression
                               | expression MINUS expression
                               | expression TIMES expression
                               | expression DIVIDE expression
    '''
    p[0] = BinaryArithmeticExpression()
    p[0].operator = p[2]
    p[0].operand1 = p[1]
    p[0].operand2 = p[3]

def p_parenthesis_expression(p):
    '''
    parenthesis_expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
    '''	
    p[0] = ParenthesisExpression()
    p[0].operand = p[2]

def p_unary_expression(p):
    '''
    unary_expression : MINUS expression %prec UMINUS
                               | NOT expression
    '''
    p[0] = UnaryArithmeticExpression()
    p[0].operator = p[1]
    p[0].operand = p[2]

def p_new_expression(p):
    '''
    new_expression : NEW type LEFT_PARENTHESIS RIGHT_PARENTHESIS
    '''
    p[0] = NewExpression()
    p[0].type_name = p[2]

def p_new_array_expression(p):
    '''
    new_array_expression : NEW type LEFT_BRACKET expression RIGHT_BRACKET
    '''
    p[0] = NewArrayExpression()
    p[0].type_name = p[2]


def p_identifier_expression(p):
    '''
    identifier_expression : IDENTIFIER
    '''
    p[0] = IdentifierExpression()
    p[0].name = p[1]

def p_integer_literal_expression(p):
    '''
    integer_literal_expression : INTEGER_LITERAL
    '''
    p[0] = IntegerExpression()
    p[0].value = p[1]

def p_boolean_expression(p):
    '''
    boolean_expression : TRUE
                                  |  FALSE
    '''
    p[0] = BooleanExpression()
    p[0].value = p[1]
    
def p_this_expression(p):
    '''
    this_expression : THIS
    '''
    p[0] = ThisExpression()

def p_null_expression(p):
    '''
    null_expression : NULL
    '''
    p[0] = NullExpression()

def p_error(p):
	print "Syntax error in input! %s" % p

precedence = (
    ('right', 'ASSIGNMENT'),
    #('left', 'RIGHT_BRACE'),
    #('right', 'LEFT_BRACE'),
   # ('left', 'SEMICOLON'),
    ('left', 'COMMA'),
    ('left', 'OR', 'AND'),
    ('nonassoc', 'LESS', 'GREATER', 'EQUAL', 'NOT_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT'),
    ('left', 'POINT'),
    #('nonassoc', 'IDENTIFIER', 'INTEGER_LITERAL'),
    #('left', 'RIGHT_PARENTHESIS'),
    #('right', 'LEFT_PARENTHESIS'),
    #('left', 'RIGHT_BRACKET'),
    #('right', 'LEFT_BRACKET'),
)



if __name__ == '__main__':
    parser = yacc.yacc()
    with open('test.java') as fin:
        result = parser.parse(fin.read())
        #ipdb.set_trace()
        print json.dumps(result, cls=JSONEncoder)
