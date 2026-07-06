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
        "add",
        "append",
        "print",
        "len",
        "open"
    }

    def __init__(
        self,
        symbol_table=None
    ):
        self.graph = nx.DiGraph()
        self.symbol_table = symbol_table

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

            if not isinstance(
                node,
                ast.FunctionDef
            ):
                continue

            function_name = node.name

            self.graph.add_node(
                function_name,
                file=file_path,
                type="function"
            )

            # -------------------------
            # Inspect every function call
            # -------------------------
            for child in ast.walk(node):

                if not isinstance(
                    child,
                    ast.Call
                ):
                    continue

                called_function = None

                # foo()
                if isinstance(
                    child.func,
                    ast.Name
                ):

                    called_function = (
                        child.func.id
                    )

                # db.get_user()
                elif isinstance(
                    child.func,
                    ast.Attribute
                ):

                    called_function = (
                        child.func.attr
                    )

                if not called_function:
                    continue

                if called_function in self.IGNORE_CALLS:
                    continue

                # -------------------------
                # Resolve through Symbol Table
                # -------------------------
                symbol = None

                if self.symbol_table:

                    symbol = (
                        self.symbol_table.lookup(
                            called_function
                        )
                    )

                if symbol:

                    self.graph.add_node(
                        called_function,
                        file=symbol["file"],
                        type=symbol["type"],
                        line=symbol["line"]
                    )

                else:

                    self.graph.add_node(
                        called_function,
                        type="external"
                    )

                self.graph.add_edge(
                    function_name,
                    called_function
                )

    def get_graph(self):

        return self.graph