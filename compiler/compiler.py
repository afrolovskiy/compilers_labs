from syntaxer import parse
from semantic import attribute, check_semantics
from generator import generate

node = parse('test.java')
node = attribute(node)
check_semantics(node)
#code = generate(node)
#with open('output.a', 'w') as fout:
#    fout.write(str(code))
