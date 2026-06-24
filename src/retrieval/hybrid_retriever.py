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

        vector_results = self.chroma.search(
            query,
            top_k=10
        )

        bm25_results = self.bm25.search(
            query,
            k=10
        )

        combined = []

        # Chroma Results
        docs = vector_results["documents"][0]
        metas = vector_results["metadatas"][0]

        for doc, meta in zip(
            docs,
            metas
        ):
            combined.append(
                {
                    "chunk": doc,
                    "file": meta.get("file", ""),
                    "function": meta.get("function", ""),
                    "class_name": meta.get("class_name", "")
                }
            )

        # BM25 Results
        for chunk in bm25_results:

            combined.append(
                {
                    "chunk": chunk.chunk,
                    "file": chunk.file,
                    "function": chunk.function,
                    "class_name": chunk.class_name
                }
            )

        # Deduplicate
        seen = set()
        unique_chunks = []

        for chunk in combined:

            key = (
                chunk["file"],
                chunk.get("function", ""),
                chunk["chunk"]
            )

            if key not in seen:

                seen.add(key)

                unique_chunks.append(
                    chunk
                )

        return unique_chunks[:k]