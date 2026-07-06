class GraphRetriever:

    def __init__(self, graph):
        self.graph = graph

    def get_related_nodes(self, node, depth=1):

        if node not in self.graph:
            return []

        related = set()
        current = {node}

        for _ in range(depth):
            next_nodes = set()

            for n in current:
                for neighbor in self.graph.successors(n):
                    related.add(neighbor)
                    next_nodes.add(neighbor)

            current = next_nodes

        return list(related)

    # -----------------------------
    # NEW: Resolve file locations
    # -----------------------------
    def resolve_node(self, node):

        if node not in self.graph:
            return {
                "name": node,
                "file": "external",
                "type": "unknown"
            }

        data = self.graph.nodes[node]

        return {
            "name": node,
            "file": data.get("file", "unknown"),
            "type": data.get("type", "function")
        }

    # -----------------------------
    # Show relationships WITH files
    # -----------------------------
    def explain_relationships(self, node):

        related = self.get_related_nodes(node)

        print(f"\n{node} calls:\n")

        internal = []
        external = []

        for r in related:

            info = self.resolve_node(r)

            if info["file"] == "external":
                external.append(info["name"])
            else:
                internal.append(info)

        print("Internal Functions:")
        for item in internal:
            print(f"  -> {item['name']} ({item['file']})")

        print("\nExternal/Library Calls:")
        for item in external:
            print(f"  -> {item}")

        return related

    # -----------------------------
    # NEW: Flow-aware output
    # -----------------------------
    def build_execution_flow(self, node, depth=3):

        visited = set()
        flow = []

        current = [(node, 0)]

        while current:
            func, level = current.pop(0)

            if func in visited or level > depth:
                continue

            visited.add(func)

            info = self.resolve_node(func)

            flow.append({
                "function": func,
                "file": info["file"],
                "level": level
            })

            for child in self.graph.successors(func):
                current.append((child, level + 1))

        return flow

    # -----------------------------
    # Pretty print flow
    # -----------------------------
    def print_flow(self, node, depth=3):

        flow = self.build_execution_flow(node, depth)

        print("\nEXECUTION FLOW\n")

        for item in flow:
            indent = "  " * item["level"]
            print(f"{indent}→ {item['function']} ({item['file']})")

        return flow