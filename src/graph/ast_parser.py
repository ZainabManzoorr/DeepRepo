import ast


class ASTParser(ast.NodeVisitor):

    def __init__(self, symbol_table=None):
        super().__init__()

        self.symbol_table = symbol_table
        self.current_class = None
        self.result = {}

    def parse(
        self,
        file_path,
        code
    ):

        self.result = {
            "file": file_path,
            "imports": [],
            "classes": [],
            "functions": [],
            "methods": [],
            "decorators": {},
            "inheritance": {},
            "docstrings": {}
        }

        self.current_class = None

        try:
            tree = ast.parse(code)

        except SyntaxError:
            return self.result

        module_doc = ast.get_docstring(tree)

        if module_doc:
            self.result["docstrings"]["module"] = module_doc

        self.visit(tree)

        return self.result

    # -----------------------------------
    # import os
    # import sqlite3
    # -----------------------------------

    def visit_Import(self, node):

        for alias in node.names:
            self.result["imports"].append(alias.name)

        self.generic_visit(node)

    # -----------------------------------
    # from flask import Flask
    # -----------------------------------

    def visit_ImportFrom(self, node):

        module = node.module or ""

        for alias in node.names:
            self.result["imports"].append(
                f"{module}.{alias.name}"
            )

        self.generic_visit(node)

    # -----------------------------------
    # class User(BaseUser)
    # -----------------------------------

    def visit_ClassDef(self, node):

        self.result["classes"].append(node.name)

        if self.symbol_table:
            self.symbol_table.add_symbol(
                name=node.name,
                file=self.result["file"],
                symbol_type="class",
                line=node.lineno
            )

        bases = []

        for base in node.bases:

            if isinstance(base, ast.Name):
                bases.append(base.id)

            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)

        self.result["inheritance"][node.name] = bases

        doc = ast.get_docstring(node)

        if doc:
            self.result["docstrings"][node.name] = doc

        previous = self.current_class
        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = previous

    # -----------------------------------
    # Functions / Methods
    # -----------------------------------

    def visit_FunctionDef(self, node):

        if self.current_class:

            method_name = (
                f"{self.current_class}.{node.name}"
            )

            self.result["methods"].append(
                method_name
            )

            if self.symbol_table:
                self.symbol_table.add_symbol(
                    name=method_name,
                    file=self.result["file"],
                    symbol_type="method",
                    line=node.lineno
                )

        else:

            self.result["functions"].append(
                node.name
            )

            if self.symbol_table:
                self.symbol_table.add_symbol(
                    name=node.name,
                    file=self.result["file"],
                    symbol_type="function",
                    line=node.lineno
                )

        decorators = []

        for dec in node.decorator_list:

            if isinstance(dec, ast.Name):
                decorators.append(dec.id)

            elif isinstance(dec, ast.Call):

                if isinstance(dec.func, ast.Attribute):
                    decorators.append(dec.func.attr)

                elif isinstance(dec.func, ast.Name):
                    decorators.append(dec.func.id)

        if decorators:
            self.result["decorators"][node.name] = decorators

        doc = ast.get_docstring(node)

        if doc:
            self.result["docstrings"][node.name] = doc

        self.generic_visit(node)