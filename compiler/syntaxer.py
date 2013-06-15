import json
from ply import yacc
from lexer import tokens
#import ipdb
from models import JSONEncoder, Node
from utils import NodeDrawer


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
    leaf = []
    leaf.extend(p[1].leaf)
    leaf.append(p[2])
    p[0] = Node('field', children=p[1].children, leaf=leaf)

def p_int_single_or_array_var(p):
    '''
    single_or_array_var : INT identifier_or_brackets 
    '''
    leaf = [p[1], ]
    leaf.extend(p[2].leaf)
    p[0] = Node('single_or_array_var', children=p[2].children, leaf=leaf)

def p_boolean_single_or_array_var(p):
    '''
    single_or_array_var : BOOLEAN IDENTIFIER
    '''
    p[0] = Node('single_or_array_var', children=[p[2], ], leaf=[p[1], ])

def p_single_or_array_var_ref(p):
    '''
    single_or_array_var : IDENTIFIER IDENTIFIER
    '''
    p[0] = Node('single_or_array_var', children=[p[1], p[2]])

def p_method(p):
    """
    method : PUBLIC return_type_and_name LEFT_PARENTHESIS params_list RIGHT_PARENTHESIS LEFT_BRACE statements_list RETURN expression SEMICOLON RIGHT_BRACE
    """
    children = p[2].children
    children.extend([p[4], p[7], p[9]])
    leaf = [p[1], ]
    leaf.extend(p[2].leaf)
    leaf.extend([p[3], p[5], p[6], p[8], p[10], p[11]])
    p[0] = Node('method', children=children, leaf=leaf)

def p_int_return_type_and_name(p):
    '''
    return_type_and_name : INT identifier_or_brackets
    '''
    leaf = [p[1], ]
    leaf.extend(p[2].leaf)
    type_node = Node('type', leaf=leaf)
    id_node = Node('identifier', children=p[2].children)
    children = [type_node, id_node]
    p[0] = Node('return_type_and_name', children=children)

def p_boolean_return_type_and_name(p):
    '''
    return_type_and_name : BOOLEAN IDENTIFIER
    '''
    type_node = Node('type', leaf=[p[1], ])
    id_node = Node('identifier', children=[p[2], ])
    children = [type_node, id_node]
    p[0] = Node('return_type_and_name', children=children)

def p_id_return_type_and_name(p):
    '''
    return_type_and_name : IDENTIFIER IDENTIFIER
    '''
    type_node = Node('type', children=[p[1], ])
    id_node = Node('identifier', children=[p[2], ])
    children = [type_node, id_node]
    p[0] = Node('return_type_and_name', children=children)

def p_empty_params_list(p):
    """
    params_list : empty
    """
    p[0] = Node('args')

def p_params_list(p):
    """
    params_list : args_list
    """
    p[0] = Node('args', children=[p[1], ])

def p_single_args_list(p):
    """
    args_list : arg
    """
    p[0] = Node('args', children=[p[1], ])

def p_args_list(p):
    """
    args_list : args_list COMMA arg
    """
    children = p[1].children if p[1] else []
    children.append(p[3])
    leaf = p[1].leaf
    leaf.append(p[2])
    p[0] = Node('args', children=children, leaf=leaf)

def p_arg(p):
    '''
    arg : single_or_array_var
    '''
    p[0] = Node('arg', children=p[1].children, leaf=p[1].leaf)

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

def p_bool_statement(p):
    '''
    statement : BOOLEAN IDENTIFIER SEMICOLON
    '''
    p[0] = Node('variable', children=[p[2]], leaf=[p[1], p[3]])

def p_int_statement(p):
    '''
    statement : INT identifier_or_brackets SEMICOLON
    '''
    leaf = [p[1], ]
    leaf.extend(p[2].leaf)
    leaf.append(p[3])
    if p[2].type == 'identifier_or_brackets_1':
        p[0] = Node('variable', children=p[2].children, leaf=leaf)
    elif p[2].type == 'identifier_or_brackets_2':
        p[0] = Node('array_variable', children=p[2].children, leaf=leaf)

def p_identifier_or_brackets_id(p):
    '''
    identifier_or_brackets : IDENTIFIER
    '''
    p[0] = Node('identifier_or_brackets_1', children=[p[1], ])

def p_identifier_or_brackets_br(p):
    '''
    identifier_or_brackets : LEFT_BRACKET RIGHT_BRACKET IDENTIFIER
    '''
    p[0] = Node('identifier_or_brackets_2', children=[p[3], ], leaf=[p[1], p[2]])

def p_complex_statement(p):
    '''
    statement : IDENTIFIER identifier_or_assignment SEMICOLON
    '''
    identifier_or_assignment = p[2]
    if identifier_or_assignment[0] == 'identifier_or_assignment_1':
        children = [p[1], identifier_or_assignment[1]]
        leaf = [p[3], ]
        p[0] = Node('variable', children=children, leaf=leaf)
    elif identifier_or_assignment[0] == 'identifier_or_assignment_2':
        children = [p[1], identifier_or_assignment[2]]
        leaf = [identifier_or_assignment[1], p[3]]
        p[0] = Node('assignment', children=children, leaf=leaf)
    elif identifier_or_assignment[0] == 'identifier_or_assignment_3':
        children = [p[1], identifier_or_assignment[2], identifier_or_assignment[5]]
        leaf = [identifier_or_assignment[1], identifier_or_assignment[3], idenitfier_or_assignment[4], p[3]]
        p[0] = Node('array_element_assignment', children=children, leaf=leaf)

def p_identifier_or_assignment_id(p):
    '''
    identifier_or_assignment : IDENTIFIER
    '''
    p[0] = ('identifier_or_assignment_1', p[1])

def p_identifier_or_assignment_assign(p):
    '''
    identifier_or_assignment : ASSIGNMENT expression
    '''
    p[0] = ('identifier_or_assignment_2', p[1], p[2])

def p_identifier_or_assignment_array_element_assign(p):
    '''
    identifier_or_assignment : LEFT_BRACKET expression RIGHT_BRACKET ASSIGNMENT expression
    '''
    p[0] = ('identifier_or_assignment_3', p[1], p[2], p[3], p[4], p[5])

def p_if_statement(p):
    '''
    statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement else_statement
    '''
    children = [p[3], p[5]]
    if p[6]:
        children.append(p[6])
    leaf = [p[1], p[2], p[4]]
    p[0] = Node('if', children=children, leaf=leaf)

def p_empty_else_statement(p):
    '''
    else_statement : empty
    '''

def p_else_statement(p):
    '''
    else_statement : ELSE statement
    '''
    p[0] = Node('else', children=[p[2]], leaf=[p[1]])

def p_while_statement(p):
    '''
    statement : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement
    ''' 
    p[0] = Node('while', children=[p[3], p[5]], leaf=[p[1], p[2], p[4]])

def p_print_statement(p):
    '''
    statement : SYSTEM POINT OUT POINT PRINTLN LEFT_PARENTHESIS expression RIGHT_PARENTHESIS SEMICOLON
    '''
    p[0] = Node('print', children=[p[7]], leaf=[p[1], p[2], p[3], p[4], p[5], p[6], p[8], p[9]])

def p_block_statement(p):
    '''
    statement : LEFT_BRACE statements_list RIGHT_BRACE
    '''
    p[0] = Node('block', children=[p[2], ], leaf=[p[1], p[3]])

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
    p[0] = p[1]

def p_array_element_expression(p):
    '''
    array_element_expression : expression LEFT_BRACKET expression RIGHT_BRACKET
    '''
    p[0] = Node('array_element', children=[p[1], p[3]], leaf=[p[2], p[4]])

def p_field_expression(p):
    '''
    field_expression : expression POINT IDENTIFIER
    '''
    p[0] = Node('field', children=[p[1], p[3]], leaf=[p[2]])    

def p_call_method_expression(p):
    '''
    call_method_expression : expression POINT IDENTIFIER LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
    '''
    p[0] = Node('method_call', children=[p[1], p[3], p[5]], leaf=[p[2], p[4], p[6]])

def p_empty_expression_list(p):
    '''
    expression_list : empty
    '''
    p[0] = Node('expressions')
    
def p_nonempty_expression_list(p):
    '''
    expression_list : nonempty_expression_list 
    '''
    p[0] = p[1]

def p_single_expression_list(p):
    '''
    nonempty_expression_list : expression
    '''
    p[0] = Node('expressions', children=[p[1], ])

def p_expression_list_head(p):
    '''
    nonempty_expression_list : expression_list COMMA expression
    '''
    children=p[1].children
    children.append(p[3])
    leaf = p[1].leaf
    leaf.append(p[2])
    p[0] = Node('expressions', children=children, leaf=leaf)

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
    p[0] = Node('binary_expression', children=[p[1], p[3], ], leaf=[p[2],])

def p_parenthesis_expression(p):
    '''
    parenthesis_expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
    '''	
    p[0] = Node('parenthesis_expression', children=[p[2],], leaf=[p[1], p[3],] )

def p_unary_expression(p):
    '''
    unary_expression : MINUS expression %prec UMINUS
                               | NOT expression
    '''
    p[0] = Node('unary_expression', children=[p[2],], leaf=[p[1],])

def p_new_array_expression(p):
    '''
    new_expression : NEW INT LEFT_BRACKET expression RIGHT_BRACKET 
    '''
    p[0] = Node('new_array_expression', children=[p[4],], leaf=[p[1], p[2], p[3], p[5]])

def p_new_identifier_expression(p):
    '''
    new_expression : NEW IDENTIFIER LEFT_PARENTHESIS RIGHT_PARENTHESIS
    '''
    p[0] = Node('new_identifier_expression', children=[p[2], ], leaf=[p[1], p[3], p[4]])

def p_identifier_expression(p):
    '''
    identifier_expression : IDENTIFIER
    '''
    p[0] = p[1]

def p_integer_literal_expression(p):
    '''
    integer_literal_expression : INTEGER_LITERAL
    '''
    p[0] = p[1]

def p_boolean_expression(p):
    '''
    boolean_expression : TRUE
                                  |  FALSE
    '''
    p[0] = p[1]
    
def p_this_expression(p):
    '''
    this_expression : THIS
    '''
    p[0] = p[1]

def p_null_expression(p):
    '''
    null_expression : NULL
    '''
    p[0] = p[1]

def p_error(p):
    print "Syntax error in input! %s" % p

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
        print json.dumps(result, cls=JSONEncoder)
        drawer = NodeDrawer()
        drawer.draw(result)
