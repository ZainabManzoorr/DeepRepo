# DeepRepo

> An AI-powered Code Intelligence System that understands repositories beyond keyword search.

DeepRepo is a Retrieval-Augmented Generation (RAG) system designed specifically for software repositories. Instead of treating code as plain text, it combines semantic search, lexical search, AST-based code understanding, and dependency graphs to retrieve contextually relevant code across an entire project.

The goal is to move from **"searching code"** to **"understanding code."**

---

## Features

### Repository Ingestion

* Load local Git repositories
* Automatically traverse project structure
* Ignore unnecessary files and directories
* Extract source code for indexing

### Smart Code Chunking

* Language-aware chunking
* Function-level and class-level chunks
* Metadata preservation
* Overlapping chunks for better retrieval

### Hybrid Retrieval

DeepRepo combines multiple retrieval techniques:

* Vector Search (ChromaDB)
* BM25 Lexical Search
* Hybrid score fusion

This improves retrieval quality compared to semantic search alone.

### Metadata Filtering

Retrieve code by:

* File name
* Language
* Directory
* Module
* Custom metadata

### AST-Based Code Understanding

Instead of viewing code as plain text, DeepRepo parses source files into an Abstract Syntax Tree (AST) and extracts:

* Classes
* Functions
* Methods
* Imports
* Decorators
* Inheritance
* Function calls
* Docstrings

### Dependency Graph

Build relationships across the repository:

* File → Imports
* Function → Calls
* Class → Methods
* Module → Dependencies

This enables repository-wide understanding.

### Cross-File Retrieval

Retrieve connected code from multiple files instead of isolated chunks.

Example:

```
Login Route
      ↓
Authentication Service
      ↓
JWT Utility
      ↓
Database Layer
```

The LLM receives the entire execution flow instead of a single file.

---

## Project Structure

```
DeepRepo/
│
├── src/
│   ├── ingestion/
│   ├── chunking/
│   ├── retrieval/
│   ├── embeddings/
│   ├── graph/
│   │   ├── ast_parser.py
│   │   ├── graph_builder.py
│   │   ├── graph_retriever.py
│   │   └── main.py
│   └── utils/
│
├── chroma_db/
├── repositories/
├── tests/
├── requirements.txt
├── main.py
└── README.md
```

---

## Technology Stack

* Python
* ChromaDB
* Sentence Transformers
* Rank-BM25
* LangChain (optional)
* AST (Python Standard Library)
* NetworkX
* FAISS (optional)

---

## How It Works

```
Repository
      │
      ▼
Repository Loader
      │
      ▼
Smart Chunker
      │
      ▼
Embeddings
      │
      ▼
Vector Database
      │
      ├───────────────┐
      ▼               ▼
 BM25 Index      AST Parser
      │               │
      └──────┬────────┘
             ▼
     Dependency Graph
             ▼
    Hybrid Retrieval
             ▼
 Related Code Context
             ▼
        LLM Response
```

---

## Example Queries

DeepRepo can answer repository-level questions such as:

* Explain the login flow.
* Where is JWT generated?
* Which files depend on `auth.py`?
* Show every function that calls `verify_token()`.
* Explain how authentication works across the project.
* Which modules import the database layer?
* Trace the execution path from API endpoint to database.

---

## Why DeepRepo?

Traditional RAG systems retrieve isolated text chunks, often missing the relationships between files and functions.

DeepRepo enhances retrieval by:

* Understanding repository structure
* Parsing code into syntax trees
* Building dependency graphs
* Retrieving connected files
* Providing richer context to Large Language Models

This results in more accurate explanations, better debugging assistance, and improved repository navigation.

---

## Future Improvements

* Multi-language AST support
* Tree-sitter integration
* Knowledge Graph generation
* Agentic repository exploration
* Automatic documentation generation
* Code summarization
* Call graph visualization
* VS Code extension
* GitHub integration
* CI/CD analysis

---

## Installation

```bash
git clone https://github.com/yourusername/DeepRepo.git

cd DeepRepo

pip install -r requirements.txt
```

---

## Run

```bash
python main.py
```

---

## Future Vision

DeepRepo aims to evolve from a retrieval system into an **AI Software Engineering Assistant** capable of understanding large codebases, tracing execution flows, answering architectural questions, generating documentation, and assisting developers with debugging, refactoring, and code exploration.
