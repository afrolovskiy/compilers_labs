#!/usr/bin/python
import sys
 
# sys.path.append('path/to/llvm-py') # you may need to setup the path to llvm-py explicitly.
 
from llvm.core import *
import copy
 
 
# Tree is used for AST storage
class Tree(object):
    def __init__(self, type, text, children=None):
        self.type = type
        self.text = text
 
        if children:
            self.children = children
        else:
            self.children = [] # do not use a default value of children = [] in the function param list!
 
    def copy(self, withChildren):
        if withChildren:
            return copy.deepcopy(self)
        else:
            c = copy.copy(self)
            c.children = []
            return c
 
 
# IDs for the different AST types
class TreeType(object):
    MODULE = 1
 
    PLUS = 10
    MINUS = 11
    STAR = 12
    SLASH = 13
 
    INTEGER_CONSTANT = 100
 
 
# base class for traversing an AST. Implements dispatch for the above defined node types
class ASTWalker(object):
    def __init__(self):
            pass
 
    def walkAST(self, ast):
        raise NotImplementedError('subclasses must implement walkAST')
 
 
        # dispatch the node to the right method after unpacking it
    def _dispatch(self, ast):
        tt = TreeType
 
        kwargs = {}
        kwargs['ast'] = ast
 
        if ast.type == tt.MODULE:
            callee = self._onModule
            kwargs['statements'] = ast.children
        elif ast.type in [tt.PLUS, tt.MINUS, tt.STAR, tt.SLASH]:
            callee = self._onOperator
 
            op = ast.type
            if len(ast.children) == 1:
                arg1 = ast.children[0]
                arg2 = None
            elif len(ast.children) == 2:
                arg1 = ast.children[0]
                arg2 = ast.children[1]
            else:
                assert(0 and 'dead code path')
 
            kwargs['op'] = op
            kwargs['arg1'] = arg1
            kwargs['arg2'] = arg2
        elif ast.type == tt.INTEGER_CONSTANT:
            callee = self._onIntegerConstant
            kwargs['value'] = int(ast.text)
        else:
            assert(0 and 'dead code path')
 
        callee(**kwargs)
 
 
 
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
 
 
 
    def _onModule(self, ast, statements):
        # create a new LLVM module, a container for global variables and functions
        self._module = Module.new('mymodule')
 
        # add some helpers
        self._addHelpers()
 
        # add a function: 'int main()'
        funcType = Type.function(Type.int(32), [])
        func = self._module.add_function(funcType, 'main')
 
 
        # create an 'entry' basic block, if we want to introduce variables we'll need it anyway
        # execution of the function starts here
        entryBB = func.append_basic_block('entry')
        entryBuilder = Builder.new(entryBB)
 
        # normal code should be inserted into the second block
        bb = func.append_basic_block('bb')
 
        # also jump to this block from the entry block
        entryBuilder.branch(bb)
 
        # add the code of the function
        self._currentBuilder = Builder.new(bb)
        for x in statements:
            self._dispatch(x)
            self._currentBuilder.call(self._printInt, [x.llvmValue])
 
        # main should return 0
        self._currentBuilder.ret(Constant.int(Type.int(32), 0))
 
        # verify the module
        self._module.verify()
 
 
 
    def _onOperator(self, ast, op, arg1, arg2):
        tt = TreeType
 
        self._dispatch(arg1)
        if arg2:# some operators are unary
            self._dispatch(arg2)
 
 
        cb = self._currentBuilder
        if op == TreeType.PLUS:
            if arg2:
                ast.llvmValue = cb.add(arg1.llvmValue, arg2.llvmValue)
            else:
                ast.llvmValue = arg1.llvmValue # +NUMBER == NUMBER
        elif op == TreeType.MINUS:
            if arg2:
                ast.llvmValue = cb.sub(arg1.llvmValue, arg2.llvmValue)
            else:
                ast.llvmValue = cb.sub(Constant.int(Type.int(32), 0), arg1.llvmValue) # -NUMBER == 0 - NUMBER
        elif op == TreeType.STAR:
            ast.llvmValue = cb.mul(arg1.llvmValue, arg2.llvmValue)
        elif op == TreeType.SLASH:
            ast.llvmValue = cb.sdiv(arg1.llvmValue, arg2.llvmValue)
        else:
            assert(0 and 'dead code path')
 
 
    def _onIntegerConstant(self, ast, value):
        ast.llvmValue = Constant.int(Type.int(32), value)
 
 
 
def createSampleAST():
    # do not reuse any variables! overwrite them first!
    exprs = []
 
    # 9 - 3 * 3
    int9 = Tree(TreeType.INTEGER_CONSTANT, '9')
    int3a = Tree(TreeType.INTEGER_CONSTANT, '3')
    int3b = Tree(TreeType.INTEGER_CONSTANT, '3')
 
    star = Tree(TreeType.STAR, '*', [int3a, int3b])
    minus = Tree(TreeType.MINUS, '-', [int9, star])
    exprs.append(minus)
 
 
    # 4 + 76 / 2
    int4 = Tree(TreeType.INTEGER_CONSTANT, '4')
    int76 = Tree(TreeType.INTEGER_CONSTANT, '76')
    int2 = Tree(TreeType.INTEGER_CONSTANT, '2')
 
    slash = Tree(TreeType.SLASH, '/', [int76, int2])
    plus = Tree(TreeType.PLUS, '+', [int4, slash])
    exprs.append(plus)
 
    # ---21
    int21 = Tree(TreeType.INTEGER_CONSTANT, '21')
    minus = Tree(TreeType.MINUS, '-', [int21])
    minus = Tree(TreeType.MINUS, '-', [minus])
    minus = Tree(TreeType.MINUS, '-', [minus])
    exprs.append(minus)
 
 
    module = Tree(TreeType.MODULE, '', exprs)
 
    return module
 
 
 
def main():
    # get an AST, should be replaced by a lexer + parser frontend
    ast = createSampleAST()
 
    codegen = CodeGen()
    module = codegen.walkAST(ast)
    print module
 
    # to run the generated code do:
    #     ./minicompiler.py | llvm-as | lli
    # or
    #     ./minicompiler.py > out.ll
    #     llvm-as out.ll
    #     lli out.bc
    # and to generate native code skip the lli above and then
    #     llc out.bc
    #     gcc out.s
 
    #     ./a.out
 
 
if __name__ == '__main__':
    main()
