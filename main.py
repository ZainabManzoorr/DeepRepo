from dotenv import load_dotenv
import os

from src.ingestion.loader import RepositoryLoader
from src.chunking.chunker import CodeChunker

from src.retrieval.chroma_store import ChromaStore
from src.retrieval.bm25_store import BM25Store
from src.retrieval.hybrid_retriever import HybridRetriever
from src.retrieval.metadata_filter import MetadataFilter

from src.query.query_expander import QueryExpander
from src.reranking.reranker import Reranker

from src.prompt.prompt_builder import PromptBuilder
from src.llm.llm import LLM

from src.graph.graph_builder import GraphBuilder
from src.graph.graph_retriever import GraphRetriever


def main():

    # -------------------------
    # Environment
    # -------------------------
    load_dotenv()

    api_key = os.getenv(
        "GROQ_API_KEY"
    )

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in environment"
        )

    # -------------------------
    # Load Repository
    # -------------------------
    repo_path = "repo"

    loader = RepositoryLoader(
        repo_path
    )

    documents = loader.load()

    print(
        f"Loaded {len(documents)} files"
    )

    # -------------------------
    # Build Dependency Graph
    # -------------------------
    graph_builder = GraphBuilder()

    for document in documents:

        if document.path.endswith(
            ".py"
        ):

            graph_builder.build_python_graph(
                document.path,
                document.content
            )

    graph = graph_builder.get_graph()

    print(
        f"\nGraph Nodes: {graph.number_of_nodes()}"
    )

    print(
        f"Graph Edges: {graph.number_of_edges()}"
    )

    print(
        "\nDEPENDENCY GRAPH\n"
    )

    for source, target in graph.edges():

        print(
            f"{source} ---> {target}"
        )

    graph_retriever = (
        GraphRetriever(graph)
    )

    # -------------------------
    # Chunking
    # -------------------------
    chunker = CodeChunker()

    all_chunks = []

    for document in documents:

        chunks = chunker.chunk_file(
            document.path,
            document.content
        )

        all_chunks.extend(
            chunks
        )

    print(
        f"\nGenerated {len(all_chunks)} chunks"
    )

    # -------------------------
    # Chroma Index
    # -------------------------
    chroma_store = ChromaStore()

    chroma_store.reset()

    chroma_store.add_chunks(
        all_chunks
    )

    # -------------------------
    # BM25 Index
    # -------------------------
    bm25_store = BM25Store()

    bm25_store.add_chunks(
        all_chunks
    )

    print(
        "\nIndexes built successfully"
    )

    # -------------------------
    # Retrieval Components
    # -------------------------
    expander = QueryExpander()

    hybrid_retriever = (
        HybridRetriever(
            chroma_store=chroma_store,
            bm25_store=bm25_store
        )
    )

    reranker = Reranker()

    metadata_filter = (
        MetadataFilter()
    )

    # -------------------------
    # LLM
    # -------------------------
    llm = LLM(
        api_key=api_key
    )

    prompt_builder = (
        PromptBuilder()
    )

    # -------------------------
    # Query Loop
    # -------------------------
    while True:

        query = input(
            "\nAsk a question about the codebase (or type 'exit'): "
        )

        if query.lower() == "exit":
            break

        print(
            f"\nOriginal Query: {query}"
        )

        # -------------------------
        # Query Expansion
        # -------------------------
        expanded_query = (
            expander.expand(
                query
            )
        )

        print(
            f"Expanded Query: {expanded_query}"
        )

        # -------------------------
        # Retrieval
        # -------------------------
        retrieved_chunks = (
            hybrid_retriever.search(
                expanded_query,
                k=20
            )
        )

        print(
            f"\nRetrieved {len(retrieved_chunks)} chunks"
        )

        # -------------------------
        # Metadata Filtering
        # -------------------------
        filters = (
            metadata_filter.detect(
                query
            )
        )

        print(
            f"Detected Filters: {filters}"
        )

        retrieved_chunks = (
            metadata_filter.apply(
                retrieved_chunks,
                filters
            )
        )

        print(
            f"After Filtering: {len(retrieved_chunks)} chunks"
        )

        # -------------------------
        # Empty Results
        # -------------------------
        if not retrieved_chunks:

            print(
                "\nNo relevant code found."
            )

            continue

        # -------------------------
        # Graph Context
        # -------------------------
        if (
            "function"
            in filters
        ):

            print(
                "\nGRAPH RELATIONSHIPS\n"
            )

            graph_retriever.explain_relationships(
                filters[
                    "function"
                ]
            )

        # -------------------------
        # Reranking
        # -------------------------
        top_chunks = (
            reranker.rerank(
                query=query,
                chunks=retrieved_chunks,
                top_k=5
            )
        )

        print(
            f"Reranked to {len(top_chunks)} chunks"
        )

        # -------------------------
        # Debug Chunks
        # -------------------------
        print(
            "\nTOP RERANKED CHUNKS\n"
        )

        for chunk in top_chunks:

            print(
                "=" * 60
            )

            print(
                f"FILE: {chunk.get('file', '')}"
            )

            print(
                f"FUNCTION: {chunk.get('function', '')}"
            )

            if (
                "distance"
                in chunk
            ):

                print(
                    f"DISTANCE: {chunk['distance']:.4f}"
                )

            print(
                chunk["chunk"][:200]
            )

        # -------------------------
        # Prompt
        # -------------------------
        prompt = (
            prompt_builder.build(
                query=query,
                chunks=top_chunks
            )
        )

        # -------------------------
        # LLM Answer
        # -------------------------
        answer = llm.generate(
            prompt
        )

        print(
            "\nAI ANSWER\n"
        )

        print(answer)


if __name__ == "__main__":
    main()