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

        # Chroma results
        docs = vector_results["documents"][0]
        metas = vector_results["metadatas"][0]

        for doc, meta in zip(
            docs,
            metas
        ):
            combined.append(
                {
                    "chunk": doc,
                    **meta
                }
            )

        # BM25 results
        for chunk in bm25_results:

            combined.append(
                chunk.__dict__
            )

        return combined[:k]