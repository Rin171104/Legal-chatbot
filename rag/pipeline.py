"""
RAG Pipeline - end-to-end processing
"""

from .embedder import Embedder
from .retriever import Retriever
from .generator import Generator
from .prompt import create_rag_prompt

class RAGPipeline:
    def __init__(self, embedder, retriever, generator):
        """Initialize RAG pipeline"""
        self.embedder = embedder
        self.retriever = retriever
        self.generator = generator
    
    def process(self, query):
        """Process query through RAG pipeline"""
        # 1. Embed query
        # 2. Retrieve relevant chunks
        # 3. Create prompt with context
        # 4. Generate response
        pass
    
    def process_stream(self, query):
        """Process query with streaming response"""
        pass

if __name__ == "__main__":
    pass
