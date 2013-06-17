import json
from ply import yacc
from lexer import tokens
from models import Node
from utils import NodeDrawer,JSONEncoder


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
    p[0] = Node('class_list')
    
def p_class_list(p):
    '''
    class_list : class_list class 
    '''
    children = p[1].children[:] if p[1] else []
    children.append(p[2])
    p[0] = Node('class_list', children=children)
    
def p_main_class(p):
    '''
    main_class : CLASS IDENTIFIER LEFT_BRACE main_method RIGHT_BRACE
    '''
    id_node = Node('identifier', children=[p[2]])
    p[0] = Node('main_class', children=[id_node, p[4]])
    
def p_main_method(p):
    '''
    main_method : PUBLIC STATIC VOID MAIN LEFT_PARENTHESIS STRING LEFT_BRACKET RIGHT_BRACKET IDENTIFIER RIGHT_PARENTHESIS LEFT_BRACE statements_list RIGHT_BRACE
    '''
    dim_node = Node('dim', children=[1])
    type_node = Node('type', children=[dim_node, p[6]])
    id_node = Node('identifier', children=[p[9]])
    arg_node = Node('arg', children=[type_node, id_node])
    p[0] = Node('main_method', children=[arg_node, p[12]])

def p_class(p):
    '''
    class : CLASS IDENTIFIER extends LEFT_BRACE declaration_list RIGHT_BRACE
    '''
    id_node = Node('identifier', children=[p[2]])
    p[0] = Node('class', children=[id_node, p[3], p[5]])

def p_empty_extends(p):
    '''
    extends : empty
    '''
    p[0] = Node('extends')
    
def p_extends(p):
    '''
    extends : EXTENDS IDENTIFIER
    '''
    id_node = Node('identifier', children=[p[2]])    
    p[0] = Node('extends', id_node)

def p_empty_declaration_list(p):
    """
    declaration_list : empty
    """
   
def p_declaration_list(p):
    """
    declaration_list : declaration_list field 
                           | declaration_list method 
    """
    children = p[1].children[:] if p[1] else []
    children.append(p[2])
    p[0] = Node('declaration_list', children=children)

def p_field(p):
    """
    field : single_or_array_var SEMICOLON
    """
    p[0] = Node('field', children=[p[1]])

def p_int_single_or_array_var(p):
    '''
    single_or_array_var : INT identifier_or_brackets 
    '''
    type_node = Node('type', children=[p[2][0], p[1]])
    p[0] = Node('variable', children=[type_node, p[2][1]])

def p_boolean_single_or_array_var(p):
    '''
    single_or_array_var : BOOLEAN IDENTIFIER
    '''
    dim_node = Node('dim', children=[0])
    type_node = Node('type', children=[dim_node, p[1]])
    id_node = Node('identifier', children=[p[2]])
    p[0] = Node('variable', children=[type_node, id_node])

def p_single_or_array_var_ref(p):
    '''
    single_or_array_var : IDENTIFIER IDENTIFIER
    '''
    dim_node = Node('dim', children=[0])
    type_id_node = Node('identifier', children=[p[1]])
    type_node = Node('type', children=[dim_node, type_id_node])
    id_node = Node('identifier', children=[p[2]])
    p[0] = Node('variable', children=[type_node, id_node])

def p_method(p):
    """
    method : PUBLIC return_type_and_name LEFT_PARENTHESIS params_list RIGHT_PARENTHESIS LEFT_BRACE statements_list RETURN expression SEMICOLON RIGHT_BRACE
    """
    return_node = Node('return', children=[p[9]])
    children = [p[4], p[7], return_node]
    children.extend(p[2])
    p[0] = Node('method', children=children)

def p_int_return_type_and_name(p):
    '''
    return_type_and_name : INT identifier_or_brackets
    '''
    type_node = Node('type', children=[p[2][0], p[1]])
    id_node = p[2][1]    
    p[0] = [type_node, id_node]

def p_boolean_return_type_and_name(p):
    '''
    return_type_and_name : BOOLEAN IDENTIFIER
    '''
    dim_node = Node('dim', children=[0])
    type_node = Node('type', children=[dim_node, p[1]])
    id_node = Node('identifier', children=[p[2]])
    p[0] = [type_node, id_node]
    
def p_id_return_type_and_name(p):
    '''
    return_type_and_name : IDENTIFIER IDENTIFIER
    '''
    dim_node = Node('dim', children=[0])
    type_id_node = Node('identifier', children=[p[1]])
    type_node = Node('type', children=[dim_node, type_id_node])
    id_node = Node('identifier', children=[p[2]])
    p[0] = [type_node, id_node]
    
def p_empty_params_list(p):
    """
    params_list : empty
    """
    p[0] = Node('args')

def p_params_list(p):
    """
    params_list : args_list
    """
    p[0] = p[1]

def p_single_args_list(p):
    """
    args_list : arg
    """
    p[0] = Node('args', children=[p[1]])

def p_args_list(p):
    """
    args_list : args_list COMMA arg
    """
    children = p[1].children[:] if p[1] else []
    children.append(p[3])
    p[0] = Node('args', children=children)

def p_arg(p):
    '''
    arg : single_or_array_var
    '''
    p[0] = Node('arg', children=[p[1]])

def p_empty_statements_list(p):
    '''
    statements_list : empty
    '''
    p[0] = Node('statements')

def p_statements_list(p):
    '''
    statements_list : statements_list statement
    '''
    children = p[1].children[:] if p[1] else []
    children.append(p[2])
    p[0] = Node('statements', children=children)    

def p_bool_statement(p):
    '''
    statement : BOOLEAN IDENTIFIER SEMICOLON
    '''
    dim_node = Node('dim', children=[0])
    type_node = Node('type', children=[dim_node, p[1]])
    id_node = Node('identifier', children=[p[2]])
    var_node = Node('variable', children=[type_node, id_node])
    p[0] = Node('statement', children = [var_node])

def p_int_statement(p):
    '''
    statement : INT identifier_or_brackets SEMICOLON
    '''
    type_node = Node('type', children=[p[2][0], p[1]])    
    var_node = Node('variable', children=[type_node, p[2][1]])
    p[0] = Node('statement', children = [var_node])     

def p_identifier_or_brackets_id(p):
    '''
    identifier_or_brackets : IDENTIFIER
    '''    
    dim_node = Node('dim', children=[0])
    id_node = Node('identifier', children=[p[1]])
    p[0] = [dim_node, id_node]

def p_identifier_or_brackets_br(p):
    '''
    identifier_or_brackets : LEFT_BRACKET RIGHT_BRACKET IDENTIFIER
    '''
    dim_node = Node('dim', children=[1])
    id_node = Node('identifier', children=[p[3]])
    p[0] = [dim_node, id_node]

def p_complex_statement(p):
    '''
    statement : IDENTIFIER identifier_or_assignment SEMICOLON
    '''
    st_type = p[2]
    if st_type[0] == 'var':
        dim_node = Node('dim', children=[0])
        type_id_node = Node('identifier', children=[p[1]])
        type_node = Node('type', children=[dim_node, type_id_node])
        id_node = st_type[1]
        var_node = Node('variable', children=[type_node, id_node])
        statement_node = Node('statement', children=[var_node])
    elif st_type[0] == 'assign':
        id_node = Node('identifier', children=[p[1]])        
        left_part_children = [id_node]
        if st_type[1]:
            left_part_children.append(st_type[1]) 
        left_part_node = Node('left_part', children=left_part_children)
        right_part_node = st_type[2]
        assignment_node = Node('assignment', children=[left_part_node, right_part_node])
        statement_node = Node('statement', children=[assignment_node])
    p[0] = statement_node

def p_identifier_or_assignment_id(p):
    '''
    identifier_or_assignment : IDENTIFIER
    '''
    id_node = Node('identifier', children=[p[1]])
    p[0] = ('var', id_node)

def p_identifier_or_assignment_assign(p):
    '''
    identifier_or_assignment : ASSIGNMENT expression
    '''
    right_part_node = Node('rignt_part', children=[p[2]])
    p[0] = ('assign', None, right_part_node)

def p_identifier_or_assignment_array_element_assign(p):
    '''
    identifier_or_assignment : LEFT_BRACKET expression RIGHT_BRACKET ASSIGNMENT expression
    '''
    index_node = Node('index', children=[p[2]])
    right_part_node = Node('rignt_part', children=[p[5]])
    p[0] = ('assign',index_node, right_part_node)

def p_if_statement(p):
    '''
    statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement else_statement
    '''
    condition_node = Node('condition', children=[p[3]])
    children = [condition_node, p[5]]
    if p[6]:
        children.append(p[6])
    if_node = Node('if', children=children) 
    p[0] = Node('statement', children=[if_node])

def p_empty_else_statement(p):
    '''
    else_statement : empty
    '''

def p_else_statement(p):
    '''
    else_statement : ELSE statement
    '''
    p[0] = Node('else', children=[p[2]])

def p_while_statement(p):
    '''
    statement : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement
    ''' 
    while_node = Node('while', children=[p[3], p[5]])
    p[0] = Node('statement', children=[while_node])

def p_print_statement(p):
    '''
    statement : SYSTEM POINT OUT POINT PRINTLN LEFT_PARENTHESIS expression RIGHT_PARENTHESIS SEMICOLON
    '''
    print_node = Node('print', children=[p[7]])
    p[0] = Node('statement', children=[print_node])

def p_block_statement(p):
    '''
    statement : LEFT_BRACE statements_list RIGHT_BRACE
    '''
    block_node = Node('block', children=[p[2]])
    p[0] = Node('statement', children=[block_node])

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
    p[0] = Node('expression', children=[p[1]])

def p_array_element_expression(p):
    '''
    array_element_expression : expression LEFT_BRACKET expression RIGHT_BRACKET
    '''
    p[0] = Node('array_element', children=[p[1], p[3]])

def p_field_expression(p):
    '''
    field_expression : expression POINT IDENTIFIER
    '''
    id_node = Node('identifier', children=[p[3]])
    p[0] = Node('field', children=[p[1], id_node])    

def p_call_method_expression(p):
    '''
    call_method_expression : expression POINT IDENTIFIER LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
    '''
    id_node = Node('identifier', children=[p[3]])
    p[0] = Node('method_call', children=[p[1], id_node, p[5]])

def p_empty_expression_list(p):
    '''
    expression_list : empty
    '''
    #p[0] = Node('expressions')
    
def p_nonempty_expression_list(p):
    '''
    expression_list : nonempty_expression_list 
    '''
    p[0] = p[1]

def p_single_expression_list(p):
    '''
    nonempty_expression_list : expression
    '''
    p[0] = Node('expressions', children=[p[1]])

def p_expression_list_head(p):
    '''
    nonempty_expression_list : nonempty_expression_list COMMA expression
    '''
    children=p[1].children[:]
    children.append(p[3])
    p[0] = Node('expressions', children=children)

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
    operand1_node = Node('operand1', children=[p[1]])
    operand2_node = Node('operand2', children=[p[3]])
    operation_node = Node('operation', children=[p[2]])
    p[0] = Node('binary_expression', children=[operand1_node, operation_node, operand2_node])

def p_parenthesis_expression(p):
    '''
    parenthesis_expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
    '''	
    p[0] = Node('parenthesis_expression', children=[p[2]])

def p_unary_expression(p):
    '''
    unary_expression : MINUS expression %prec UMINUS
                               | NOT expression
    '''
    operation_node = Node('operation', children=[p[1]])
    operand_node = Node('operand', children=[p[2]])
    p[0] = Node('unary_expression', children=[operation_node, operand_node])

def p_new_array_expression(p):
    '''
    new_expression : NEW INT LEFT_BRACKET expression RIGHT_BRACKET 
    '''
    type_node = Node('type', children=[p[2]])
    p[0] = Node('new_array_expression', children=[type_node, p[4]])

def p_new_identifier_expression(p):
    '''
    new_expression : NEW IDENTIFIER LEFT_PARENTHESIS RIGHT_PARENTHESIS
    '''
    id_node = Node('identifier', children=[p[2]])
    p[0] = Node('new_expression', children=[id_node])

def p_identifier_expression(p):
    '''
    identifier_expression : IDENTIFIER
    '''
    p[0] = Node('identifier', children=[p[1]])

def p_integer_literal_expression(p):
    '''
    integer_literal_expression : INTEGER_LITERAL
    '''
    p[0] = Node('integer', children=[p[1]])

def p_boolean_expression(p):
    '''
    boolean_expression : TRUE
                                  |  FALSE
    '''
    p[0] = Node('boolean', children=[p[1]])
    
def p_this_expression(p):
    '''
    this_expression : THIS
    '''
    p[0] = Node('this')

def p_null_expression(p):
    '''
    null_expression : NULL
    '''
    p[0] = Node('null')

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


def parse(filename):
    parser = yacc.yacc()
    with open(filename) as fin:
        result = parser.parse(fin.read())
        print json.dumps(result, cls=JSONEncoder)
        drawer = NodeDrawer()
        drawer.draw(result)	
        return result


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
