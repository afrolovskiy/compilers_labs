import ply.lex as lex


class MiniJavaLexer:
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

	def t_INTEGER_LITERAL(self, t):
		r'\d+'
		t.value = int(t.value)
		return t

	def t_IDENTIFIER(self, t):
		r'[A-Za-z][\d\w]*'
		t.type = self.reserved.get(t.value, 'IDENTIFIER')
		return t

	def t_newline(self, t):
		r'\n+'
		t.lexer.lineno += len(t.value)

	t_ignore  = ' \t'

	def t_error(self, t):
		print "Illegal character '%s'" % t.value[0]
		t.lexer.skip(1)

	def build(self,**kwargs):
		self.lexer = lex.lex(module=self, **kwargs)

	def test(self,data):
		self.lexer.input(data)
		while True:
			 tok = self.lexer.token()
			 if not tok: break
			 print tok


if __name__ == '__main__':
	m = MiniJavaLexer()
	m.build()
	m.test(
		"""
		class Factorial {
			public static void main(String[] a) {
				System.out.println(new Fac().ComputeFac(10));
			}
		}

		class Fac {
			public int ComputeFac(int num) {
				int num_aux;
			if (num < 1)
				num_aux = 1;
			else
				num_aux = num * (this.ComputeFac(num - 1));
			return num_aux;
			}
		}
		"""
	)

