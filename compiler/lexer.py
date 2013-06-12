from  ply import lex


reserved = {
	'class': 'CLASS',
	'public': 'PUBLIC',
	'static': 'STATIC',
	'void': 'VOID',
	'main': 'MAIN',
	'String': 'STRING',
	'extends': 'EXTENDS',
	'return': 'RETURN',
	'int': 'INT',
	'boolean': 'BOOLEAN',
	'if': 'IF',
	'else': 'ELSE',
	'while': 'WHILE',
	'lenght': 'LENGTH',
	'true': 'TRUE',
	'false': 'FALSE',
	'this': 'THIS',
	'new': 'NEW',
	'System': 'SYSTEM',
	'out': 'OUT',
	'println': 'PRINTLN',
}

tokens = [
	'LEFT_PARENTHESIS',
	'RIGHT_PARENTHESIS',
	'LEFT_BRACKET',
	'RIGHT_BRACKET',
	'LEFT_BRACE',
	'RIGHT_BRACE',
	'POINT',
	'COMMA',
	'SEMICOLON',
	'NOT',
	'ASSIGNMENT',
	'BINARY_OPERATOR',
	'INTEGER_LITERAL',
	'IDENTIFIER',		
] + list(reserved.values())

def t_IDENTIFIER(t):
	r'[A-Za-z][\d\w]*'
	t.type = reserved.get(t.value, 'IDENTIFIER')
	return t

def t_INTEGER_LITERAL(t):
	r'\d+'
	t.value = int(t.value)
	return t

t_LEFT_PARENTHESIS = r'\('
t_RIGHT_PARENTHESIS = r'\)'
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'
t_LEFT_BRACE = r'{'
t_RIGHT_BRACE = r'}'
t_POINT = r'\.'
t_COMMA = r','
t_SEMICOLON = r';'
t_NOT = r'!'
t_ASSIGNMENT = r'='
t_BINARY_OPERATOR = r'&&|<|\+|-|\*'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
	print "Illegal character '%s'" % t.value[0]
	t.lexer.skip(1)

lexer = lex.lex()

def test(data):
	lexer.input(data)
	while True:
		 tok = lexer.token()
		 if not tok: break
		 print tok

if __name__ == '__main__':
	with open('test.java', 'r') as fin:
		test(fin.read())
