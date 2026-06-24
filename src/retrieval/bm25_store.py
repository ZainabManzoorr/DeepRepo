from rank_bm25 import BM25Okapi


class BM25Store:

    def __init__(self):

        self.documents = []
        self.tokenized_docs = []

        self.bm25 = None

    def add_chunks(self, chunks):

        self.documents = chunks

        self.tokenized_docs = [
            chunk.chunk.split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_docs
        )

    def search(
        self,
        query,
        k=10
    ):

        tokens = query.split()

        scores = self.bm25.get_scores(
            tokens
        )

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            doc
            for doc, score in ranked[:k]
        ]