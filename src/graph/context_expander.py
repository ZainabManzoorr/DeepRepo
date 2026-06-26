class GraphContextExpander:

    def __init__(
        self,
        graph_retriever,
        hybrid_retriever
    ):
        self.graph_retriever = (
            graph_retriever
        )

        self.hybrid_retriever = (
            hybrid_retriever
        )

    def expand(
        self,
        function_name
    ):

        related_nodes = (
            self.graph_retriever
            .get_internal_nodes(
                function_name
            )
        )

        extra_chunks = []

        for node in related_nodes:

            results = (
                self.hybrid_retriever.search(
                    node,
                    k=2
                )
            )

            extra_chunks.extend(
                results
            )

        return extra_chunks