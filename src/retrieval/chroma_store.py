import uuid
import chromadb

from src.embeddings.embedder import Embedder


class ChromaStore:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="data/vectordb"
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="code_chunks"
            )
        )

        self.embedder = Embedder()

    # -------------------------
    # Reset Collection
    # -------------------------
    def reset(self):

        try:

            self.client.delete_collection(
                name="code_chunks"
            )

            print(
                "Deleted existing collection"
            )

        except Exception:

            print(
                "No existing collection found"
            )

        self.collection = (
            self.client.get_or_create_collection(
                name="code_chunks"
            )
        )

    # -------------------------
    # Add Chunks
    # -------------------------
    def add_chunks(
        self,
        chunks
    ):

        documents = []
        metadatas = []
        ids = []

        for chunk in chunks:

            documents.append(
                chunk.chunk
            )

            metadatas.append(
                {
                    "file": chunk.file,

                    "function": (
                        chunk.function or ""
                    ),

                    "class_name": (
                        chunk.class_name or ""
                    )
                }
            )

            ids.append(
                str(uuid.uuid4())
            )

        embeddings = (
            self.embedder.embed_batch(
                documents
            )
        )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(
            f"Added {len(documents)} chunks to Chroma"
        )

    # -------------------------
    # Search
    # -------------------------
    def search(
        self,
        query: str,
        top_k: int = 5,
        file_filter: str = None
    ):

        query_embedding = (
            self.embedder.embed(
                query
            )
        )

        if file_filter:

            results = (
                self.collection.query(
                    query_embeddings=[
                        query_embedding
                    ],
                    n_results=top_k,
                    where={
                        "file": file_filter
                    }
                )
            )

        else:

            results = (
                self.collection.query(
                    query_embeddings=[
                        query_embedding
                    ],
                    n_results=top_k
                )
            )

        chunks = []

        documents = (
            results.get(
                "documents",
                [[]]
            )[0]
        )

        metadatas = (
            results.get(
                "metadatas",
                [[]]
            )[0]
        )

        distances = (
            results.get(
                "distances",
                [[]]
            )[0]
        )

        for doc, meta, distance in zip(
            documents,
            metadatas,
            distances
        ):

            chunks.append(
                {
                    "chunk": doc,

                    "file": meta.get(
                        "file",
                        ""
                    ),

                    "function": meta.get(
                        "function",
                        ""
                    ),

                    "class_name": meta.get(
                        "class_name",
                        ""
                    ),

                    "distance": distance
                }
            )

        return chunks

    # -------------------------
    # Collection Stats
    # -------------------------
    def count(self):

        return self.collection.count()