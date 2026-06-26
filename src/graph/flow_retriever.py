class FlowRetriever:

    def __init__(
        self,
        graph_retriever,
        hybrid_retriever
    ):
        self.graph_retriever = graph_retriever
        self.hybrid_retriever = hybrid_retriever

    def retrieve_flow(
        self,
        entry_function,
        depth=3,
        chunks_per_node=2
    ):
        """
        Retrieve the execution flow beginning
        from an entry function.

        Example:

        login
            ↓
        get_user
            ↓
        get_connection
        """

        # -------------------------
        # Find all related functions
        # -------------------------
        flow_nodes = (
            self.graph_retriever.get_related_nodes(
                entry_function,
                depth=depth
            )
        )

        # Include the starting function
        flow_nodes.insert(
            0,
            entry_function
        )

        print("\nEXECUTION FLOW\n")

        for node in flow_nodes:

            print(f" -> {node}")

        # -------------------------
        # Retrieve chunks
        # -------------------------
        all_chunks = []

        seen = set()

        for node in flow_nodes:

            results = (
                self.hybrid_retriever.search(
                    node,
                    k=chunks_per_node
                )
            )

            for chunk in results:

                key = (
                    chunk["file"],
                    chunk.get("function", ""),
                    chunk["chunk"]
                )

                if key not in seen:

                    seen.add(key)
                    all_chunks.append(chunk)

        print(
            f"\nRetrieved {len(all_chunks)} flow chunks"
        )

        return all_chunks