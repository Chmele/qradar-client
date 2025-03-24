import inspect
import ast
from qradar import QRadar


def unparse(ast_obj):
    unparser = ast._Unparser()
    return unparser.visit(ast.fix_missing_locations(ast_obj))


class Stubgen:
    def __init__(self, cls, scheme):
        module = ast.parse(inspect.getsource(cls))
        class_def = module.body[0]
        module.body.insert(
            0,
            ast.ImportFrom(
                "typing",
                [
                    ast.alias(name="Optional"),
                    ast.alias(name="Dict"),
                    ast.alias(name="Any"),
                ],
            ),
        )
        for endpoint in scheme:
            class_def.body.append(self.prepare_method(endpoint))
        with open("qradar.pyi", "w") as file:
            file.write(unparse(module))

    def prepare_method(self, scheme):
        return ast.FunctionDef(
            name=f"""{
                scheme.get("http_method").lower()}{scheme.get("path")
                .translate({ord('{'):None, ord('}'): None, ord('/'): ord('_')})}""",
            args=ast.arguments(
                posonlyargs=[],
                args=[
                    ast.arg(arg="self", annotation=None),
                    ast.arg(
                        arg="path",
                        annotation=ast.Subscript(
                            value=ast.Name(id="Optional", ctx=ast.Load()),
                            slice=ast.Index(value=ast.Name(id="str", ctx=ast.Load())),
                            ctx=ast.Load(),
                        ),
                    ),
                    ast.arg(
                        arg="json",
                        annotation=ast.Subscript(
                            value=ast.Name(id="Optional", ctx=ast.Load()),
                            slice=ast.Index(value=ast.Name(id="Dict", ctx=ast.Load())),
                            ctx=ast.Load(),
                        ),
                    ),
                ],
                vararg=ast.arg(arg="params", annotation=None),
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
                kwarg=None,
            ),
            body=[
                ast.Expr(value=ast.Constant(value=f"""{scheme.get('description')}""")),
                ast.Expr(value=ast.Constant(value=...)),
            ],
            decorator_list=[],
            returns=ast.Name(id="Any", ctx=ast.Load()),
        )


from key import KEY
import requests

q = QRadar("https://qradar.is.local", KEY, "22.0", requests.Session(), False)

scheme = q.get_help_endpoints()
s = Stubgen(QRadar, scheme)
