from ply import yacc
from lexer import tokens


start = 'goal'

def p_goal(p):
    'goal : main_class class_list'

def p_class_list(p):
    '''
    class_list : 
                   | class class_list
    '''

def p_main_class(p):
    '''
    main_class : 	CLASS IDENTIFIER LEFT_BRACE PUBLIC STATIC VOID MAIN LEFT_PARENTHESIS STRING LEFT_BRACKET RIGHT_BRACKET IDENTIFIER RIGHT_PARENTHESIS LEFT_BRACE var_list statement_list RIGHT_BRACE RIGHT_BRACE
    '''

def p_class(p):
    '''
    class : CLASS IDENTIFIER extends LEFT_BRACE declaration_list RIGHT_BRACE
    '''

def p_extends(p):
    '''
    extends : 
                | EXTENDS IDENTIFIER
    '''

def p_declaration_list(p):
    """
    declaration_list : 
                           | field
                           | method
                           | declaration_list
    """

def p_field(p):
    """
    field : type IDENTIFIER SEMICOLON
    """

def p_method(p):
    """
    method : PUBLIC type IDENTIFIER LEFT_PARENTHESIS params_list RIGHT_PARENTHESIS LEFT_BRACE var_list statement_list RETURN expression SEMICOLON RIGHT_BRACE
    """

def p_params_list(p):
    """
    params_list :
                      | args_list
    """

def p_args_list(p):
    """
    args_list : arg
                 | arg COMMA args_list
    """

def p_arg(p):
    '''
    arg : type IDENTIFIER
    '''

def p_var_list(p):
    """
    var_list :
                | var var_list
    """

def p_var(p):
    """
    var : type IDENTIFIER SEMICOLON
          | type IDENTIFIER ASSIGNMENT expression SEMICOLON
    """

def p_statement_list(p):
    """
    statement_list :
                         | statement statement_list
    """

def p_type(p):
    '''
    type : array_type 
           | boolean_type 
           | int_type 
           | identifier_type
    '''

def p_array_type(p):
    '''
    array_type : type LEFT_BRACKET RIGHT_BRACKET
    '''

def p_boolean_type(p):
    '''
    boolean_type : BOOLEAN
    '''

def p_int_type(p):
    '''
    int_type : INT
    '''

def p_identifier_type(p):
    '''
    identifier_type : IDENTIFIER
    '''

def p_statement(p):
    '''
    statement : block_statement 
                    | if_statement 
                    | while_statement 
                    | print_statement 
                    | assignment_statement 
    '''
def p_block_statement(p):
    '''
    block_statement : LEFT_BRACE statement_list RIGHT_BRACE
    '''

def p_if_statement(p):
    '''
    if_statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement ELSE statement
    '''

def p_while_statement(p):
    '''
    while_statement : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement
    '''

def p_print_statement(p):
    '''
    print_statement : SYSTEM POINT OUT POINT PRINTLN LEFT_PARENTHESIS expression RIGHT_PARENTHESIS SEMICOLON
    '''

def p_assignment_statement(p):
    '''
    assignment_statement : expression ASSIGNMENT expression SEMICOLON
    '''

def p_expression(p):
    '''
    expression : array_element_expression 
                     | class_field_expression
                     | class_method_expression
                     | or_expression
                     | and_expression
                     | equal_expression
                     | not_equal_expression
                     | greater_expression
                     | less_expression
                     | plus_expression
                     | minus_expression
                     | multiply_expression
                     | divide_expression
                     | parenthesis_expression
                     | unary_minus_expression
                     | not_expression
                     | new_expression
                     | new_array_expression
                     | identifier_expression
                     | integer_literal_expression
                     | true_expression
                     | false_expression
                     | this_expression
                     | null_expression
    '''

def p_array_element_expression(p):
    '''
    array_element_expression : expression LEFT_BRACKET expression RIGHT_BRACKET
    '''

def p_class_field_expression(p):
    '''
    class_field_expression : expression POINT accessed_field
    '''

def p_accessed_field(p):
    '''
    accessed_field : IDENTIFIER
                           | IDENTIFIER POINT accessed_field
    '''

def p_class_method_expression(p):
    '''
    class_method_expression : expression POINT IDENTIFIER LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS
    '''

def p_expression_list(p):
    '''
    expression_list : expression
                           | expression COMMA expression_list
    '''

def p_or_expression(p):
    '''
    or_expression : expression OR expression
    '''

def p_and_expression(p):
    '''
    and_expression : expression AND expression
    '''

def p_equal_expression(p):
    '''
    equal_expression : expression EQUAL expression
    '''

def p_not_equal_expression(p):
    '''
    not_equal_expression : expression NOT_EQUAL expression
    '''

def p_greater_expression(p):
    '''
    greater_expression : expression GREATER expression
    '''

def p_less_expression(p):
    '''
    less_expression : expression LESS expression
    '''

def p_plus_expression(p):
    '''
    plus_expression : expression PLUS expression
    '''

def p_minus_expression(p):
    '''
    minus_expression : expression MINUS expression
    '''

def p_multiply_expression(p):
    '''
    multiply_expression : expression MULTIPLY expression
    '''

def p_divide_expression(p):
    '''
    divide_expression : expression DIVIDE expression
    '''

def p_parenthesis_expression(p):
    '''
    parenthesis_expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
    '''	

def p_unary_minus_expression(p):
    '''
    unary_minus_expression : MINUS expression
    '''	

def p_not_expression(p):
    '''
    not_expression : NOT expression
    '''

def p_new_expression(p):
    '''
    new_expression : NEW type LEFT_PARENTHESIS RIGHT_PARENTHESIS
    '''

def p_new_array_expression(p):
    '''
    new_array_expression : NEW type LEFT_BRACKET expression RIGHT_BRACKET brackets
    '''

def p_brackets(p):
    '''
    brackets : 
                  | LEFT_BRACKET RIGHT_BRACKET brackets
    '''

def p_identifier_expression(p):
    '''
    identifier_expression : IDENTIFIER
    '''

def p_integer_literal_expression(p):
    '''
    integer_literal_expression : INTEGER_LITERAL
    '''

def p_true_expression(p):
    '''
    true_expression : TRUE
    '''

def p_false_expression(p):
    '''
    false_expression : FALSE
    '''
    
def p_this_expression(p):
    '''
    this_expression : THIS
    '''

def p_null_expression(p):
    '''
    null_expression : NULL
    '''

def p_error(p):
	print "Syntax error in input!"


if __name__ == '__main__':
	parser = yacc.yacc()
	with open('test.java') as fin:
		result = parser.parse(fin.read())
		print result
