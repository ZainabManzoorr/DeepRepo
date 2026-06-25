from sentence_transformers import CrossEncoder
import re


class Reranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query,
        chunks,
        top_k=5
    ):

        pairs = [
            (
                query,
                chunk["chunk"]
            )
            for chunk in chunks
        ]

        scores = self.model.predict(
            pairs
        )

        # -------------------------
        # Filename Boosting
        # -------------------------
        file_match = re.findall(
            r"\w+\.py",
            query.lower()
        )

        if file_match:

            target_file = file_match[0]

            boosted_scores = []

            for chunk, score in zip(chunks, scores):

                file_name = chunk.get(
                    "file",
                    ""
                ).lower()

                if target_file in file_name:
                    score += 10

                boosted_scores.append(score)

            scores = boosted_scores

        # -------------------------
        # Ranking
        # -------------------------
        ranked = sorted(
            zip(chunks, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            chunk
            for chunk, score in ranked[:top_k]
        ]