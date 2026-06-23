from sentence_transformers import SentenceTransformer

class Embedder:
  def __init__(self):
    self.model = SentenceTransformer(
      "all-MiniLM-L6-v2"
    )
  def embed(self,text:str):
    return self.model.encode(text).tolist()
  def embed_batch(self,texts:list[str]):
    return self.model.encode(texts).tolist()