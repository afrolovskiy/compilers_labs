import json
from ply import yacc
from lexer import tokens
#import ipdb
from models import JSONEncoder, Node


start = 'programm'

def p_programm(p):
    '''
    programm : main_class class_list
    '''
    p[0] = Node('programm', children=[p[1], p[2]])

def p_empty(p):
    '''
    empty :
    '''

def p_empty_class_list(p):
    '''
    class_list : empty 
    '''
    
def p_class_list(p):
    '''
    class_list : class_list class 
    '''
    children = p[1].children if p[1] else []
    children.append(p[2])
    p[0] = Node('class_list', children=children)
    
def p_main_class(p):
    '''
    main_class : CLASS IDENTIFIER LEFT_BRACE main_method RIGHT_BRACE
    '''
    p[0] = Node('main_class', children=[p[4], ], leaf=[p[1], p[2], p[3], p[5]])
    
def p_main_method(p):
    '''
    main_method : PUBLIC STATIC VOID MAIN LEFT_PARENTHESIS STRING LEFT_BRACKET RIGHT_BRACKET IDENTIFIER RIGHT_PARENTHESIS LEFT_BRACE statements_list RIGHT_BRACE
    '''
    p[0] = Node('main_method', children=[p[12]], leaf=[p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[13]])

def p_class(p):
    '''
    class : CLASS IDENTIFIER extends LEFT_BRACE declaration_list RIGHT_BRACE
    '''
    p[0] = Node('class', children=[p[3], p[5]], leaf=[p[1], p[2], p[4], p[6]])

def p_empty_extends(p):
    '''
    extends : empty
    '''
    
def p_extends(p):
    '''
    extends : EXTENDS IDENTIFIER
    '''
    p[0] = Node('extends', children=[], leaf=[p[1], p[2]])

def p_empty_declaration_list(p):
    """
    declaration_list : empty
    """
   
def p_declaration_list(p):
    """
    declaration_list : declaration_list field 
                           | declaration_list method 
    """
    children = p[1].children if p[1] else []
    children.append(p[2])
    p[0] = Node('declaration_list', children=children)

def p_field(p):
    """
    field : single_or_array_var SEMICOLON
    """
    p[0] = Node('field', children=[p[1]], leaf=[p[2]])

def p_single_or_array_var(p):
    '''
    single_or_array_var : INT identifier_or_brackets
                                 | BOOLEAN IDENTIFIER
    '''
    p[0] = Node('variable', children=[p[2]], leaf=[p[1]])

def p_single_or_array_var_ref(p):
    '''
    single_or_array_var : IDENTIFIER IDENTIFIER
    '''
    p[0] = Node('variable', children=[p[1], p[2]])

def p_method(p):
    """
    method : PUBLIC single_or_array_var LEFT_PARENTHESIS params_list RIGHT_PARENTHESIS LEFT_BRACE statements_list RETURN expression SEMICOLON RIGHT_BRACE
    """
    p[0] = Node('method', children=[p[2], p[4], p[7], p[9]], leaf=[p[1], p[3], p[5], p[6], p[8], p[10], p[11]])

def p_empty_params_list(p):
    """
    params_list : empty
    """
#    #p[0] = []

def p_params_list(p):
    """
    params_list : args_list
    """
    p[0] = Node('args', children=[p[1]])

def p_single_args_list(p):
    """
    args_list : arg
    """
    p[0] = Node('args', children=[p[0]])

def p_args_list(p):
    """
    args_list : args_list COMMA arg
    """
    children = p[1].children if p[1] else []
    children.append(p[3])
    leafs = p[1].leafs
    leafs.append(p[2])
    p[0] = Node('args', children=children, leaf=leafs)

def p_arg(p):
    '''
    arg : single_or_array_var
    '''
    p[0] = Node('arg', children=[p[1]])

def p_empty_statements_list(p):
    '''
    statements_list : empty
    '''

def p_statements_list(p):
    '''
    statements_list : statements_list statement
    '''
    children = p[1].children if p[1] else []
    children.append(p[2])
    p[0] = Node('statements_list', children=children)    

def p_statement(p):
    '''
    statement : INT identifier_or_brackets SEMICOLON
                   | BOOLEAN IDENTIFIER SEMICOLON
    '''
    p[0] = Node('statement', children=[p[2]], leaf=[p[1], p[3]])
    #children = p[2][0]
    #children.insert(0, p[2])
    #leaf = p[2][1]
    #leaf.extend([p
    #p[0] = Node('variable-statement', children=children, 

def p_complex_statement(p):
    '''
    statement : IDENTIFIER identifier_or_assignment SEMICOLON
    '''
    p[0] = Node('statement', children=[p[1], p[2]], leaf=[p[3]])
    #p[0] = ([p[1]. p[2]], [p[3]])

def p_identifier_or_brackets_id(p):
    '''
    identifier_or_brackets : IDENTIFIER
    '''
    p[0] = Node('variable', children=[p[0]])

def p_identifier_or_brackets_br(p):
    '''
    identifier_or_brackets : LEFT_BRACKET RIGHT_BRACKET IDENTIFIER
    '''
    p[0] = Node('array_variable', children=[p[3]], leaf=[p[1],p[2]])

def p_identifier_or_assignment(p):
    '''
    identifier_or_assignment : IDENTIFIER
                                        | ASSIGNMENT expression
                                        | LEFT_BRACKET expression RIGHT_BRACKET ASSIGNMENT expression
    '''

def p_if_statement(p):
    '''
    statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement else_statement
    '''

def p_empty_else_statement(p):
    '''
    else_statement : empty
    '''

def p_else_statement(p):
    '''
    else_statement : ELSE statement
    '''



def p_while_statement(p):
    '''
    statement : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement
    ''' 
    #p[0] = WhileStatement()
    #p[0].condition = #p[3]
    #p[0].expression = #p[5]

def p_print_statement(p):
    '''
    statement : SYSTEM POINT OUT POINT PRINTLN LEFT_PARENTHESIS expression RIGHT_PARENTHESIS SEMICOLON
    '''
    #p[0] = PrintStatement()
    #p[0].expression = #p[7]

#def p_assignment_statement(p):
#    '''
#    assignment_statement : IDENTIFIER ASSIGNMENT expression SEMICOLON %prec VASSIGN
#    '''
    #p[0] = AssignmentStatement()
    #p[0].left_part = #p[1]
    #p[0].right_part = #p[3]

def p_block_statement(p):
    '''
    statement : LEFT_BRACE statements_list RIGHT_BRACE
    '''
    #p[0] = #p[2]

def p_expression(p):
    '''
    expression : array_element_expression 
                     | field_expression
                     | call_method_expression
                     | binary_expression
                     | parenthesis_expression
                     | unary_expression
                     | new_expression
                     | identifier_expression
                     | integer_literal_expression
                     | boolean_expression
                     | this_expression
                     | null_expression
    '''
    #p[0] = #p[1]

def p_array_element_expression(p):
    '''
    array_element_expression : expression LEFT_BRACKET expression RIGHT_BRACKET
    '''
    #p[0] = ArrayElementExpression()
    #p[0].array = #p[1]
    #p[0].index = #p[3]

def p_field_expression(p):
    '''
    field_expression : expression POINT IDENTIFIER
    '''
    #p[0] = FieldExpression()
    #p[0].expression = #p[1]
    #p[0].identifier = #p[3]

def p_call_method_expression(p):
    '''
    call_method_expression : expression POINT IDENTIFIER LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
    '''
    #p[0] = CallMethodExpression()
    #p[0].expression = #p[1]
    #p[0].method_name = #p[3]
    #p[0].args = #p[5]

def p_empty_expression_list(p):
    '''
    expression_list : empty
    '''
    #p[0] = []
    
def p_nonempty_expression_list(p):
    '''
    expression_list : nonempty_expression_list 
    '''
    #p[0] = #p[1]

def p_single_expression_list(p):
    '''
    nonempty_expression_list : expression
    '''
    #p[0] = [#p[1], ]

def p_expression_list_head(p):
    '''
    nonempty_expression_list : expression_list COMMA expression
    '''
    #p[0] = #p[1]
    #p[0].append(#p[2])

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
    #p[0] = BinaryArithmeticExpression()
    #p[0].operator = #p[2]
    #p[0].operand1 = #p[1]
    #p[0].operand2 = #p[3]

def p_parenthesis_expression(p):
    '''
    parenthesis_expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
    '''	
    #p[0] = ParenthesisExpression()
    #p[0].operand = #p[2]

def p_unary_expression(p):
    '''
    unary_expression : MINUS expression %prec UMINUS
                               | NOT expression
    '''
    #p[0] = UnaryArithmeticExpression()
    #p[0].operator = #p[1]
    #p[0].operand = #p[2]

def p_new_expression(p):
    '''
    new_expression : NEW INT LEFT_BRACKET expression RIGHT_BRACKET 
                             | NEW IDENTIFIER LEFT_PARENTHESIS RIGHT_PARENTHESIS
    '''
    #p[0] = NewExpression()
    #p[0].type_name = #p[2]

def p_identifier_expression(p):
    '''
    identifier_expression : IDENTIFIER
    '''
    #p[0] = IdentifierExpression()
    #p[0].name = #p[1]

def p_integer_literal_expression(p):
    '''
    integer_literal_expression : INTEGER_LITERAL
    '''
    #p[0] = IntegerExpression()
    #p[0].value = #p[1]

def p_boolean_expression(p):
    '''
    boolean_expression : TRUE
                                  |  FALSE
    '''
    #p[0] = BooleanExpression()
    #p[0].value = #p[1]
    
def p_this_expression(p):
    '''
    this_expression : THIS
    '''
    #p[0] = ThisExpression()

def p_null_expression(p):
    '''
    null_expression : NULL
    '''
    #p[0] = NullExpression()

def p_error(p):
    print "Syntax error in input! %s" % p
    #yacc.errok()
    #while 1:
    #    tok = yacc.token()             # Get the next token
    #    if not tok or tok.type == 'ASSIGNMENT': break
    #yacc.restart()
    #yacc.errok()
    #return tok

precedence = (
    ('left', 'OR', 'AND'),
    ('nonassoc', 'LESS', 'GREATER', 'EQUAL', 'NOT_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS', 'NOT'),
    ('right', 'POINT'),
)



if __name__ == '__main__':
    import logging
    logging.basicConfig(
        level = logging.DEBUG,
        filename = "parselog.txt",
        filemode = "w",
        format = "%(filename)10s:%(lineno)4d:%(message)s"
    )
    log = logging.getLogger()
    parser = yacc.yacc(debug=True)
    with open('test.java') as fin:
        result = parser.parse(fin.read(), debug=log)
        #ipdb.set_trace()
        print json.dumps(result, cls=JSONEncoder)
