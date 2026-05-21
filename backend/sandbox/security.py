import ast

FORBIDDEN_MODULES = {
    "os", "subprocess", "shutil", "socket", "requests",
    "urllib", "http", "ftplib", "smtplib", "telnetlib",
    "ctypes", "multiprocessing", "signal", "sys",
}

FORBIDDEN_FUNCTIONS = {
    "eval", "exec", "compile", "open", "__import__",
    "globals", "locals", "vars", "getattr", "setattr",
    "delattr", "hasattr",
}

FORBIDDEN_ATTRS = {
    "__class__", "__bases__", "__mro__", "__subclasses__",
    "__init__", "__new__", "__del__", "__dict__",
    "__globals__", "__code__", "__closure__",
}


class SecurityError(Exception):
    pass


def check_code(code: str) -> None:
    """Scan code AST for dangerous operations. Raises SecurityError if found."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return  # Syntax errors handled by Python at runtime

    checker = _SecurityVisitor()
    checker.visit(tree)


class _SecurityVisitor(ast.NodeVisitor):
    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name.split(".")[0] in FORBIDDEN_MODULES:
                raise SecurityError(f"禁止导入模块: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and node.module.split(".")[0] in FORBIDDEN_MODULES:
            raise SecurityError(f"禁止导入模块: {node.module}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_FUNCTIONS:
            raise SecurityError(f"禁止调用函数: {node.func.id}()")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr in FORBIDDEN_ATTRS:
            raise SecurityError(f"禁止访问属性: {node.attr}")
        self.generic_visit(node)
