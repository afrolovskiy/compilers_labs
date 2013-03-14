from recursive_descent import RecursiveDescent

expr = '&123'
print expr
print RecursiveDescent(expr).parse()
