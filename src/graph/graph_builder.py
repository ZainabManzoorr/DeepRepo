import ast
import networkx as nx


class GraphBuilder:

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

            # ------------------------
            # Function Definitions
            # ------------------------
            if isinstance(node, ast.FunctionDef):

                function_name = node.name

                self.graph.add_node(
                    function_name,
                    file=file_path,
                    type="function"
                )

                # ------------------------
                # Function Calls
                # ------------------------
                for child in ast.walk(node):

                    if isinstance(child, ast.Call):

                        if isinstance(
                            child.func,
                            ast.Name
                        ):

                            called_function = (
                                child.func.id
                            )

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