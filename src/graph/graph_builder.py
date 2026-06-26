import ast
import networkx as nx


class GraphBuilder:

    # Ignore common library/framework calls
    IGNORE_CALLS = {
        "route",
        "jsonify",
        "cursor",
        "execute",
        "executemany",
        "fetchone",
        "fetchall",
        "commit",
        "rollback",
        "close",
        "connect",
        "cursor",
        "add",
        "append",
        "print",
        "len",
        "open"
    }

    def __init__(self):
        self.graph = nx.DiGraph()

    def build_python_graph(
        self,
        file_path: str,
        code: str
    ):

        try:
            tree = ast.parse(code)

        except SyntaxError:
            return

        for node in ast.walk(tree):

            if not isinstance(node, ast.FunctionDef):
                continue

            function_name = node.name

            self.graph.add_node(
                function_name,
                file=file_path,
                type="function"
            )

            for child in ast.walk(node):

                if not isinstance(child, ast.Call):
                    continue

                called_function = None

                # -------------------------
                # foo()
                # -------------------------
                if isinstance(child.func, ast.Name):

                    called_function = child.func.id

                # -------------------------
                # db.get_user()
                # model.predict()
                # conn.commit()
                # -------------------------
                elif isinstance(child.func, ast.Attribute):

                    called_function = child.func.attr

                if not called_function:
                    continue

                # Ignore noisy framework/database calls
                if called_function in self.IGNORE_CALLS:
                    continue

                self.graph.add_node(
                    called_function,
                    type="function"
                )

                self.graph.add_edge(
                    function_name,
                    called_function
                )

    def get_graph(self):

        return self.graph