import chromadb
import uuid
from src.embeddings.embedder import Embedder

class ChromaStore:
  def __init__(self):
    self.client = chromadb.PersistentClient(
      path = "data/vectordb"
    )
    self.collection = self.client.get_or_create_collection(
      name = "code_chunks"
    )
    
    self.embedder = Embedder()
  
  def add_chunks(self,chunks):
    documents = []
    metadatas = []
    ids = []
    
    for idx, chunk in enumerate(chunks):
      documents.append(
        chunk.chunk
      )
      metadatas.append(
       {
         "file":chunk.file,
         "function":(
           chunk.function or ""
         ),
         "class_name": (
           chunk.class_name or ""
         )
       } 
      )
      
      ids.append(str(uuid.uuid4()))
    
    embeddings = (
      self.embedder.embed_batch(
        documents
      )
    )
    
    self.collection.add(
      ids = ids,
      documents= documents,
      embeddings= embeddings,
      metadatas = metadatas
    )
  def search(
    self,
    query:str,
    top_k :int = 3
  ):
    
    query_embedding = (
      self.embedder.embed(query)
    )
    
    results = self.collection.query(
      query_embeddings=[
        query_embedding
      ],
      n_results = top_k
    )
    
    return results