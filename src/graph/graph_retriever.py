class GraphRetriever:

    def __init__(
        self,
        graph
    ):
        self.graph = graph

    def get_neighbors(
        self,
        function_name: str
    ):

        if function_name not in self.graph:

            return []

        return list(
            self.graph.neighbors(
                function_name
            )
        )

    def explain_relationships(
        self,
        function_name: str
    ):

        neighbors = self.get_neighbors(
            function_name
        )

        print(
            f"\n{function_name} calls:\n"
        )

        for n in neighbors:

            print(
                f" -> {n}"
            )