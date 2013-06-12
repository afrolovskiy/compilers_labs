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
	'true': 'TRUE',
	'false': 'FALSE',
	'this': 'THIS',
	'null': 'NULL',
	'new': 'NEW',
	'System': 'SYSTEM',
	'out': 'OUT',
	'println': 'PRINTLN',
	'length': 'LENGTH',
}

tokens = list(reserved.values()) + [
	'INTEGER_LITERAL',
	'IDENTIFIER',		
	'LEFT_PARENTHESIS',
	'RIGHT_PARENTHESIS',
	'LEFT_BRACKET',
	'RIGHT_BRACKET',
	'LEFT_BRACE',
	'RIGHT_BRACE',
	'POINT',
	'COMMA',
	'SEMICOLON',
	'OR',
	'AND',
	'EQUAL',
	'NOT_EQUAL',
	'GREATER',
	'LESS',
	'PLUS',
	'MINUS',
	'TIMES',
	'DIVIDE',
	'ASSIGNMENT',
	'NOT',
]

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
t_OR = r'\|\|'
t_AND = r'&&'
t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGNMENT = r'='
t_NOT = r'!'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

t_ignore_COMMENT = r'//.*'

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
