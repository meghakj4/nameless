from langchain_huggingface import HuggingFaceEmbeddings

class GeminiFreeEmbeddings(HuggingFaceEmbeddings):
    """Custom embeddings using HuggingFace sentence transformers"""
    
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize HuggingFace embeddings"""
        super().__init__(model_name=model_name)