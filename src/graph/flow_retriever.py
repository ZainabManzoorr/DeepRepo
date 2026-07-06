class FlowRetriever:

    def __init__(self, graph_retriever, hybrid_retriever, symbol_table=None):
        self.graph_retriever = graph_retriever
        self.hybrid_retriever = hybrid_retriever
        self.symbol_table = symbol_table or {}

    # -----------------------------
    # Resolve function → real symbol
    # -----------------------------
    def resolve_symbol(self, function_name):

        if not self.symbol_table:
            return None

        return self.symbol_table.get(function_name)

    # -----------------------------
    # Core flow builder
    # -----------------------------
    def retrieve_flow(self, entry_function, depth=3, chunks_per_node=2):

        visited = set()
        flow_chunks = []

        queue = [(entry_function, 0)]

        while queue:

            func, level = queue.pop(0)

            if func in visited or level > depth:
                continue

            visited.add(func)

            # -----------------------------
            # 1. Resolve symbol across files
            # -----------------------------
            symbol_info = self.resolve_symbol(func)

            # fallback if not in symbol table
            if symbol_info:
                file_path = symbol_info["file"]
                symbol_type = symbol_info["type"]
            else:
                file_path = "unknown"
                symbol_type = "external"

            # -----------------------------
            # 2. Retrieve code chunks for this node
            # -----------------------------
            query = f"{func} {file_path}"

            retrieved = self.hybrid_retriever.search(
                query,
                k=chunks_per_node
            )

            for chunk in retrieved:
                chunk["flow_level"] = level
                chunk["flow_node"] = func
                chunk["resolved_file"] = file_path
                chunk["symbol_type"] = symbol_type

                flow_chunks.append(chunk)

            # -----------------------------
            # 3. Expand graph neighbors
            # -----------------------------
            neighbors = self.graph_retriever.get_related_nodes(
                func,
                depth=1
            )

            for n in neighbors:
                queue.append((n, level + 1))

        return flow_chunks

    # -----------------------------
    # Debug view (very important)
    # -----------------------------
    def debug_flow(self, entry_function, depth=3):

        flow = self.retrieve_flow(entry_function, depth)

        print("\nFLOW RETRIEVAL (SYMBOL-AWARE)\n")

        for c in flow:

            print(
                f"[{c.get('flow_level')}] "
                f"{c.get('flow_node')} → "
                f"{c.get('resolved_file')} → "
                f"{c.get('symbol_type')}"
            )

        return flow