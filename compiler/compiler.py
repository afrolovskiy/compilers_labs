from models import Node
from syntaxer import parse
from semantic import attribute, check_semantics
from generator import generate


def needle_node(node):
    if isinstance(node, Node):
        for children in node.children:
            if isinstance(children, Node):
                children.parent = node
                needle_node(children)

node = parse('test.java')
needle_node(node)
node = attribute(node)
check_semantics(node)
#code = generate(node)
#with open('output.a', 'w') as fout:
#    fout.write(str(code))
