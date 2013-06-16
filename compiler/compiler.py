from syntaxer import parse
from generator import generate

node = parse('test.java')
code = generate(node)
with open('output.a', 'w') as fout:
    fout.write(str(code))
