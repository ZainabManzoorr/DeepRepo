import ast


class ASTParser(ast.NodeVisitor):

    def __init__(self):

        self.result = {}

        self.current_class = None

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

        # Module docstring
        module_doc = ast.get_docstring(tree)

        if module_doc:

            self.result["docstrings"]["module"] = (
                module_doc
            )

        self.visit(tree)

        return self.result

    # -----------------------------------
    # import os
    # import sqlite3
    # -----------------------------------
    def visit_Import(
        self,
        node
    ):

        for alias in node.names:

            self.result["imports"].append(
                alias.name
            )

        self.generic_visit(node)

    # -----------------------------------
    # from flask import Flask
    # -----------------------------------
    def visit_ImportFrom(
        self,
        node
    ):

        module = node.module or ""

        for alias in node.names:

            self.result["imports"].append(
                f"{module}.{alias.name}"
            )

        self.generic_visit(node)

    # -----------------------------------
    # class User(BaseUser)
    # -----------------------------------
    def visit_ClassDef(
        self,
        node
    ):

        self.result["classes"].append(
            node.name
        )

        bases = []

        for base in node.bases:

            if isinstance(base, ast.Name):

                bases.append(
                    base.id
                )

            elif isinstance(
                base,
                ast.Attribute
            ):

                bases.append(
                    base.attr
                )

        self.result["inheritance"][
            node.name
        ] = bases

        doc = ast.get_docstring(node)

        if doc:

            self.result["docstrings"][
                node.name
            ] = doc

        previous = self.current_class

        self.current_class = node.name

        self.generic_visit(node)

        self.current_class = previous

    # -----------------------------------
    # Functions / Methods
    # -----------------------------------
    def visit_FunctionDef(
        self,
        node
    ):

        if self.current_class:

            self.result["methods"].append(
                f"{self.current_class}.{node.name}"
            )

        else:

            self.result["functions"].append(
                node.name
            )

        # Decorators
        decorators = []

        for dec in node.decorator_list:

            if isinstance(dec, ast.Name):

                decorators.append(
                    dec.id
                )

            elif isinstance(
                dec,
                ast.Call
            ):

                if isinstance(
                    dec.func,
                    ast.Attribute
                ):

                    decorators.append(
                        dec.func.attr
                    )

                elif isinstance(
                    dec.func,
                    ast.Name
                ):

                    decorators.append(
                        dec.func.id
                    )

        if decorators:

            self.result["decorators"][
                node.name
            ] = decorators

        # Function docstring
        doc = ast.get_docstring(node)

        if doc:

            self.result["docstrings"][
                node.name
            ] = doc

        self.generic_visit(node)