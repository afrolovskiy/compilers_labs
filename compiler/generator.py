#!/usr/bin/python
import sys
 
# sys.path.append('path/to/llvm-py') # you may need to setup the path to llvm-py explicitly.
 
from llvm.core import *
import copy
 


# base class for traversing an AST. Implements dispatch for the above defined node types
class ASTWalker(object):
    def __init__(self):
            pass
 
    def walkAST(self, ast):
        raise NotImplementedError('subclasses must implement walkAST')
  
    def _dispatch(self, node):
        callee = None
        if node.type == 'programm':
            callee = self._onProgramm
        elif node.type == 'statements':
            callee = self._onStatementsList
        elif node.type == 'statement':
            callee = self._onStatement
        elif node.type == 'print':
            callee = self._onPrint
        elif node.type == 'expression':
            callee = self._onExpression
        elif node.type == 'integer':
            callee = self._onInteger
           
        
        if callee:
            callee(node)
  
 
class CodeGen(ASTWalker):
    def __init__(self, *k, **kw):
        ASTWalker.__init__(self, *k, **kw)
  
    def walkAST(self, ast):
        self._dispatch(ast)
        return self._module
  
    def _addHelpers(self):
        # you might want to skip this function on a first read. It adds essentially a function to print integers to stdout.
 
        # add a prototype for printf
        # int printf(char*, ...)
        funcType = Type.function(Type.int(32), [Type.pointer(Type.int(8))], True)
        printf = self._module.add_function(funcType, 'printf')
 
         # add a function to print integers to stdout using printf
        # void printInt(int x) { printf("%d\n", x); }
        funcType = Type.function(Type.void(), [Type.int(32)])
        printInt = self._module.add_function(funcType, 'printInt')
        self._printInt = printInt # save for later use in _onModule
 
        # create a block and a builder for printInt
        bb = printInt.append_basic_block('bb')
        b = Builder.new(bb)
 
        # create a global constant to hold the first argument of printf
        stringConst = Constant.stringz('%d\n') # zero terminated --> stringz instead of string
        string = self._module.add_global_variable(stringConst.type, '__internalGlobalConst')
        string.initializer = stringConst
        string.global_constant = True
        string.linkage = LINKAGE_INTERNAL # not strictly necessary here, but this global should only be available during link time in the current module
 
        # address calculation
        # every index traverses a pointer without derefencing.
        # gep (get element pointer) does only address calculation, no memony accesses!
        idx = [Constant.int(Type.int(32), 0), Constant.int(Type.int(32), 0)] # the first index get's us past the global variable (which is a pointer) to the string; the second index is the offset inside the string we want to access
        realAddr = string.gep(idx) # get real address
 
        # call printf
        b.call(printf, [realAddr, printInt.args[0]])
        b.ret_void()
 
    def _onProgramm(self, node):
        print '_onProgramm'
        self._module = Module.new('mainmodule')
        self._addHelpers()
        
        main_class = node.children[0]
        main_method = main_class.children[1]
        self._onMainMethod(main_method)

        self._module.verify()

    def _onMainMethod(self, node):
        print '_onMainMethod'
        funcType = Type.function(Type.int(32), [])
        func = self._module.add_function(funcType, 'main')
        self._currentFunction = func
 
        entryBB = func.append_basic_block('entry')
        entryBuilder = Builder.new(entryBB)
        bb = func.append_basic_block('bb')
        entryBuilder.branch(bb)

        self._currentBuilder = Builder.new(bb)
        statements = node.children[1]
        self._dispatch(statements)
        self._currentBuilder.ret(Constant.int(Type.int(32), 0))

    def _onStatementsList(self, node):
        print '_onStatementsList'
        for children in node.children:
            self._dispatch(children)

    def _onStatement(self, node):   
        print '_onStatement'
        self._dispatch(node.children[0])

    def _onPrint(self, node):
        print '_onPrint'
        expression = node.children[0]
        self._dispatch(expression)
        value = expression.value
        if isinstance(value, ConstantInt):
            self._currentBuilder.call(self._printInt, [value])
        else:
            pass

    def _onExpression(self, node):
        children = node.children[0]
        self._dispatch(children)
        node.value = children.value

    def _onInteger(self, node):
        value = int(node.children[0])
        node.value = Constant.int(Type.int(32), value)
        
        
         
def generate(ast):
    codegen = CodeGen()
    module = codegen.walkAST(ast)
    print module
    return module

