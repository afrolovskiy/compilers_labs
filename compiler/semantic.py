from models import *

def attribute(node):
    return node

def check_semantics(ast):
    check_class_duplicates(ast)
    class_list = ast.children[1]
    table = Table()    
    for c in class_list.children:
        class_node = check_duplicate_fields_and_methods(c)
        table.classes.append(class_node)     
    #check_no_undefined(class_list)    
    print table

def check_class_duplicates(ast):
    class_names = []
    classes = ast.children
    main_class = classes[0]
    main_class_id = main_class.children[0]
    class_names.append(main_class_id.children[0])
    class_list = classes[1]
    for c in class_list.children:
        class_id = c.children[0]
        class_name = class_id.children[0]
        c.attrs['name'] = class_name
        if class_name in class_names:
            raise Exception ('Two classes with the same name are detected: ' + class_name)
        else:
            class_names.append(class_name)
    class_list.attrs['class_names'] = class_names
    print class_names
  
def create_type_node(var_node):
    type = var_node.children[0]
    dim = type.children[0].children[0]
    
    if isinstance(type.children[1], Node) and type.children[1].type == 'identifier':
        name = type.children[1].children[0]
    else:
        name = type.children[1]
    type_node = Type_node(name, dim)
    return type_node

def create_var_node(var):
    type = create_type_node(var)
    name = var.children[1].children[0]
    var_node = Var_node(type, name)
    return var_node
        
def check_duplicate_fields_and_methods(node):
    field_names = []
    method_names = []
    class_elements = node.children[2].children
    flg = True
    class_node = Class_node(name=node.attrs['name'])
    for ce in class_elements:
        ce.attrs['class_name'] = node.attrs['name']
        if ce.type == 'field':
            class_node.fields.append(create_var_node(ce.children[0]))
            field_id = ce.children[0].children[1]
            field_name = field_id.children[0]
            ce.attrs['name'] = field_name
            if field_name in field_names:
                raise Exception ('Two fields with the same name are detected in class ' + node.attrs['name'] + ': ' + field_name)
            else:
                field_names.append(field_name)
            if not flg:
                raise Exception ('Field declaration after methods in class ' + node.attrs['class_name'] + ': ' + field_name)
        elif ce.type == 'method':
            method_id = ce.children[4]
            method_name = method_id.children[0]
            ce.attrs['name'] = method_name
            if method_name in method_names:
                raise Exception ('Two methods with the same name are detected in class ' + node.attrs['name'], + ': ' +  method_name)
            else:
                method_names.append(method_name)
            flg = False
            method_type = ce.children[0]
            dim = method_type.children[0].children[0]
            if isinstance(method_type.children[1], Node) and method_type.children[1].type == 'identifier':
                name = method_type.children[1].children[0]
            else:
                name = method_type.children[1]
            type = Type_node(name, dim)
            arg_nodes = check_method_args(ce)
            var_nodes = check_method_variables(ce)
            class_node.methods.append(Method_node(type, method_name, arg_nodes, var_nodes))
    node.attrs['field_names'] = field_names
    node.attrs['method_names'] = method_names    
    print field_names
    print method_names
    return class_node

def check_method_variables(node):
    var_names = []
    var_nodes = []
    statements = node.children[1]
    flg = True
    for st in statements.children:
        st_body = st.children[0]
        if st_body.type == 'variable':
            var_id = st_body.children[1]
            var_name = var_id.children[0]
            st_body.attrs['name'] = var_name
            if var_name in var_names:
                raise Exception ('Two variables with the same name are detected in method ' + node.attrs['name'] + 'in class ' + node.attrs['class_name'] + ': ' + var_name)
            else:
                var_names.append(var_name)
            if not flg:
                raise Exception ('Variable declaration after code statements is detected in method ' + node.attrs['name'] + 'in class ' + node.attrs['class_name'] + ': ' + var_name)
            var_nodes.append(create_var_node(st_body))
        else:
            flg = False
    node.attrs['var_names'] = var_names
    print 'vars'    
    print var_names
    return var_nodes

def check_method_args(node):
    arg_names = []
    arg_nodes = []
    args=node.children[0]
    for arg in args.children:
        arg_id = arg.children[0].children[1]
        arg_name = arg_id.children[0]
        arg.attrs['name'] = arg_name
        if arg_name in arg_names:
            raise Exception('Two args with the same name are detected in method ' + node.attrs['name'] + 'in class ' + node.attrs['class_name'] + ': ' + arg_name)
        else:
            arg_names.append(arg_name)
        arg_nodes.append(create_var_node(arg.children[0]))
    node.attrs['arg_names'] = arg_names
    print 'args'
    print arg_names
    return arg_nodes

def check_no_undefined(node, table):
    pass

    

    
