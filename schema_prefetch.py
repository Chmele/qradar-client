import ast
from qradar import QRadar



def unparse(ast_obj):
    unparser = ast._Unparser()
    return unparser.visit(ast.fix_missing_locations(ast_obj))


class Stubgen:
    def __init__(self, class_name, version, scheme):
        class_def = ast.ClassDef(
            name=class_name,
            bases=[],
            keywords=[],
            body=[],
            decorator_list=[]
        )
        for endpoint in scheme:
            class_def.body.append(self.prepare_method(endpoint))
        with open("qradar.pyi", "w") as file:
            file.write(unparse(class_def))


    def prepare_method(self, scheme):
        http_method = scheme.get("http_method")
        path = scheme.get("path")
        method_name = f"{http_method.lower()}{path.replace('/', '_')}"

        args = [
            ast.arg(arg='self', annotation=None),
            ast.arg(arg='path', annotation=ast.Subscript(
                value=ast.Name(id='Optional', ctx=ast.Load()),
                slice=ast.Index(value=ast.Name(id='str', ctx=ast.Load())),
                ctx=ast.Load()
            )),
            ast.arg(arg='json', annotation=ast.Subscript(
                value=ast.Name(id='Optional', ctx=ast.Load()),
                slice=ast.Index(value=ast.Name(id='Dict', ctx=ast.Load())),
                ctx=ast.Load()
            )),
        ]
        
        func_args = ast.arguments(
            posonlyargs=[],
            args=args,
            vararg=ast.arg(arg='params', annotation=None),
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
            kwarg=None
        )
        docstring = f"""{scheme.get('description')}"""

        doc_expr = ast.Expr(
            value=ast.Constant(value=docstring)
        )
        
        body = [
            doc_expr,
            ast.Expr(value=ast.Constant(value=...))
        ]
        
        returns = ast.Name(id='Any', ctx=ast.Load())
        
        func_def = ast.FunctionDef(
            name=method_name,
            args=func_args,
            body=body,
            decorator_list=[],
            returns=returns
        )
        return func_def
    
from key import KEY
import requests

q = QRadar("https://10.1.12.222", KEY, "22.0", requests.Session(), False)

scheme = q.get_help_endpoints()
s = Stubgen("QRadar", '22.0', scheme)