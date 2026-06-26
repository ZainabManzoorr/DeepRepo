class GraphRetriever:

    def __init__(self, graph):
        self.graph = graph

    def get_related_nodes(
        self,
        node,
        depth=1
    ):

        if node not in self.graph:
            return []

        visited = set()
        current = {node}

        for _ in range(depth):

            next_nodes = set()

            for n in current:

                for neighbor in self.graph.successors(n):

                    if neighbor not in visited:

                        visited.add(neighbor)
                        next_nodes.add(neighbor)

            current = next_nodes

        return list(visited)

    def get_internal_nodes(
        self,
        node,
        depth=1
    ):
        """
        Return only functions that are defined
        inside the repository.
        """

        related = self.get_related_nodes(
            node,
            depth
        )

        internal = []

        for func in related:

            data = self.graph.nodes.get(
                func,
                {}
            )

            if data.get("file"):

                internal.append(func)

        return internal

    def get_callers(
        self,
        node
    ):
        """
        Functions that call the given node.
        """

        if node not in self.graph:
            return []

        return list(
            self.graph.predecessors(node)
        )

    def explain_relationships(
        self,
        node
    ):

        if node not in self.graph:

            print(
                f"\n'{node}' not found in graph."
            )

            return []

        print(f"\n{node} calls:\n")

        internal = self.get_internal_nodes(
            node
        )

        external = []

        for func in self.get_related_nodes(node):

            if func not in internal:

                external.append(func)

        if internal:

            print("Internal Functions:")

            for func in internal:

                file = self.graph.nodes[func].get(
                    "file",
                    ""
                )

                print(
                    f"  -> {func} ({file})"
                )

        if external:

            print("\nExternal/Library Calls:")

            for func in external:

                print(
                    f"  -> {func}"
                )

        callers = self.get_callers(node)

        if callers:

            print("\nCalled By:")

            for caller in callers:

                print(
                    f"  <- {caller}"
                )

        return internal