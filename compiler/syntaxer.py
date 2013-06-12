from ply import yacc
from lexer import tokens


start = 'goal'

def p_goal(p):
	'goal : main_class class_declaration_list'

def p_class_declaration_list(p):
	'''class_declaration_list : 
									   | class_declaration class_declaration_list
	'''

def p_main_class(p):
	'''
	main_class : 	CLASS IDENTIFIER LEFT_BRACE PUBLIC STATIC VOID MAIN LEFT_PARENTHESIS STRING LEFT_BRACKET RIGHT_BRACKET IDENTIFIER RIGHT_PARENTHESIS LEFT_BRACE 	statement RIGHT_BRACE
	'''

def p_class_declaration(p):
	'''
	class_declaration : CLASS IDENTIFIER extends_list LEFT_BRACE var_declaration_list method_declaration_list 	RIGHT_BRACE
	'''

def p_extends_list(p):
	'''
	extends_list : 
				 | EXTENDS IDENTIFIER
	'''

def p_var_declaration_list(p):
	'''
	var_declaration_list : 
								 | var_declaration var_declaration_list
	'''

def p_method_delaration_list(p):
	'''
	method_declaration_list :
									   | method_declaration method_declaration_list
	'''


def p_var_declaration(p):
	'var_declaration : type IDENTIFIER SEMICOLON'

def p_method_declaration(p):
	'''
	method_declaration : PUBLIC type IDENTIFIER LEFT_PARENTHESIS params_list RIGHT_PARENTHESIS LEFT_BRACE var_declaration_list statement_list RETURN expression SEMICOLON RIGHT_BRACE
	'''

def p_params_list(p):
	'''
	params_list : type IDENTIFIER
					  | type IDENTIFIER COMMA params_list
	'''

def p_statement_list(p):
	"""
	statement_list : 
						  | statement statement_list
    """

def p_type(p):
	'''type : int_array_type 
		   	 | boolean_type 
			 | int_type 
			 | identifier_type
	'''

def p_int_array_type(p):
	'int_array_type : INT LEFT_BRACKET RIGHT_BRACKET'

def p_boolean_type(p):
	'boolean_type : BOOLEAN'

def p_int_type(p):
	'int_type : INT'

def p_identifier_type(p):
	'identifier_type : IDENTIFIER'

def p_statement(p):
	'''statement : block_statement 
					  | if_statement 
					  | while_statement 
					  | print_statement 
					  | 	assignment_statement 
					  | array_element_assignment_statement'''

def p_block_statement(p):
	'block_statement : LEFT_BRACE statement_list RIGHT_BRACE'

def p_if_statement(p):
	'if_statement : IF LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement ELSE statement'

def p_while_statement(p):
	'while_statement : WHILE LEFT_PARENTHESIS expression RIGHT_PARENTHESIS statement'

def p_print_statement(p):
	'print_statement : SYSTEM POINT OUT POINT PRINTLN LEFT_PARENTHESIS expression RIGHT_PARENTHESIS SEMICOLON'

def p_assignment_statement(p):
	'assignment_statement : IDENTIFIER ASSIGNMENT expression SEMICOLON'

def p_array_element_assignment_statement(p):
	'array_element_assignment_statement : IDENTIFIER LEFT_BRACKET expression RIGHT_BRACKET ASSIGNMENT expression SEMICOLON'

def p_expression(p):
	'''expression : operator_expression 
					   | array_element_expression 
					   | length_expression 
					   | call_expression
					   | integer_literal_expression 
					   | true_expression 
					   | false_expression 
					   | identifier_expression 
					   | this_expression 
					   | new_array_expression 
					   |  new_expression 
					   | not_expression 
					   | parenthesis_expression'''

def p_operator_expression(p):
	'operator_expression : expression BINARY_OPERATOR expression'

def p_array_element_expression(p):
	'array_element_expression : expression LEFT_BRACKET expression RIGHT_BRACKET'

def p_length_expression(p):
	'length_expression : expression POINT LENGTH'

def p_call_expression(p):
	'call_expression : expression POINT IDENTIFIER LEFT_PARENTHESIS expression_list RIGHT_PARENTHESIS'

def p_expression_list(p):
	'''expression_list : 
							| expression COMMA expression_list
	'''

def p_integer_literal_expression(p):
	'integer_literal_expression : INTEGER_LITERAL'

def p_true_expression(p):
	'true_expression : TRUE'

def p_false_expression(p):
	'false_expression : FALSE'

def p_identifier_expression(p):
	'identifier_expression : IDENTIFIER'

def p_this_expression(o):
	'this_expression : THIS'

def p_new_array_expression(p):
	'new_array_expression : NEW INT LEFT_BRACKET expression RIGHT_BRACKET'

def p_new_expression(p):
	'new_expression : NEW IDENTIFIER LEFT_PARENTHESIS RIGHT_PARENTHESIS'

def p_not_expression(p):
	'not_expression : NOT expression'

def p_parenthesis_expression(p):
	'parenthesis_expression : LEFT_PARENTHESIS expression RIGHT_PARENTHESIS'	

def p_error(p):
	print "Syntax error in input!"


if __name__ == '__main__':
	parser = yacc.yacc()
	with open('test.java') as fin:
		result = parser.parse(fin.read())
		print result
