"""
Embedding model wrapper
"""

from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """Initialize embedder"""
        self.model = SentenceTransformer(model_name)
    
    def embed(self, text):
        """Embed text"""
        pass
    
    def embed_batch(self, texts):
        """Embed batch of texts"""
        pass

if __name__ == "__main__":
    pass
