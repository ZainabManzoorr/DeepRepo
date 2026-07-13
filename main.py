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
from src.graph.symbol_table import SymbolTable
from src.graph.graph_retriever import GraphRetriever
from src.graph.flow_retriever import FlowRetriever
from src.graph.ast_parser import ASTParser

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
   
    
    symbol_table = SymbolTable()
    
    ast_parser = ASTParser(
    symbol_table=symbol_table
    )

    for document in documents:

        if document.path.endswith(
            ".py"
        ):

            ast_parser.parse(
                document.path,
                document.content
            )
    print("\nSYMBOL TABLE\n")
    print(symbol_table.all_symbols())

    for name, info in symbol_table.all_symbols().items():
      print(name)
      print(f"  File : {info['file']}")
      print(f"  Type : {info['type']}")
      print(f"  Line : {info['line']}\n")
    
    
    graph_builder = GraphBuilder(
    symbol_table=symbol_table
)
    for document in documents:
        if document.path.endswith(".py"):

          graph_builder.build_python_graph(
            document.path,
            document.content
        )

    graph = graph_builder.get_graph()

      
    print("\nDEPENDENCY GRAPH\n")

    for source, target in graph.edges():
        
        node = graph.nodes[target]
        
        symbol_type = node.get("type", "external")
        file_path = node.get("file", "External")
        
    print(
        f"{source} ---> {target}"
        f" [{symbol_type}]"
        f" ({file_path})"
        )
    
        

    graph_retriever = GraphRetriever(
       graph=graph,
       symbol_table=symbol_table
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
    
    flow_retriever = FlowRetriever(
        graph_retriever=graph_retriever,
        hybrid_retriever=hybrid_retriever,
        symbol_table=symbol_table
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
        
        filters = metadata_filter.resolve_file_filter(filters, symbol_table)

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
        # Graph Augmentation
        # -------------------------
        
        if "function" in filters:
            
            function_name = filters["function"]
            
            print("\nGRRAPH RELATIONSHIPS\n")
            
            graph_retriever.explain_relationships(
                function_name
            )
            
            flow_chunks = (
                flow_retriever.retrieve_flow(
                    entry_function=function_name,
                    depth=3,
                    chunks_per_node=2
                )
            )
            
            print(f"\nAdded {len(flow_chunks)} graph chunks")
            
            retrieved_chunks.extend(
                flow_chunks
            )
        # -------------------------
        # Deduplicate
        # -------------------------
        
        seen = set()
        
        unique_chunks = []
        
        for chunk in retrieved_chunks:
            
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
        retrieved_chunks = (
            unique_chunks
        )
        print(f"Final Context Chunks:{len(retrieved_chunks)}")
            
        # -------------------------
        # Empty Results
        # -------------------------
        if not retrieved_chunks:

            print(
                "\nNo relevant code found."
            )

            continue

        

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