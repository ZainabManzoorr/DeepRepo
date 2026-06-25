class HybridRetriever:

    def __init__(
        self,
        chroma_store,
        bm25_store
    ):
        self.chroma = chroma_store
        self.bm25 = bm25_store

    def search(
        self,
        query,
        k=20
    ):

        # -------------------------
        # Vector Search
        # -------------------------
        vector_results = (
            self.chroma.search(
                query=query,
                top_k=10
            )
        )

        # -------------------------
        # BM25 Search
        # -------------------------
        bm25_results = (
            self.bm25.search(
                query=query,
                k=10
            )
        )

        combined = []

        # -------------------------
        # Chroma Results
        # Already normalized
        # -------------------------
        combined.extend(
            vector_results
        )

        # -------------------------
        # BM25 Results
        # -------------------------
        for chunk in bm25_results:

            combined.append(
                {
                    "chunk": chunk.chunk,
                    "file": chunk.file,
                    "function": (
                        chunk.function
                        or ""
                    ),
                    "class_name": (
                        chunk.class_name
                        or ""
                    )
                }
            )

        # -------------------------
        # Deduplicate
        # -------------------------
        seen = set()

        unique_chunks = []

        for chunk in combined:

            key = (
                chunk.get(
                    "file",
                    ""
                ),
                chunk.get(
                    "function",
                    ""
                ),
                chunk.get(
                    "chunk",
                    ""
                )
            )

            if key not in seen:

                seen.add(
                    key
                )

                unique_chunks.append(
                    chunk
                )

        return unique_chunks[:k]