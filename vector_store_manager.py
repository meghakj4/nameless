import os
import pickle
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from gemini_embeddings import GeminiFreeEmbeddings

class VectorStoreManager:
    """Manages persistent vector store that can append multiple PDFs"""
    
    def __init__(self, store_path="vector_store"):
        """Initialize the vector store manager"""
        self.store_path = store_path
        self.vector_store = None
        # Use HuggingFace embeddings
        self.embeddings = GeminiFreeEmbeddings()
        self.load_or_create_store()
    
    def load_or_create_store(self):
        """Load existing vector store or create new one"""
        if os.path.exists(self.store_path):
            try:
                self.vector_store = FAISS.load_local(
                    self.store_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print(f"✓ Loaded existing vector store from '{self.store_path}'")
                return True
            except Exception as e:
                print(f"Error loading vector store: {str(e)}")
                self.vector_store = None
                return False
        else:
            print(f"✓ New vector store will be created at '{self.store_path}'")
            return True
    
    def load_pdf(self, pdf_path):
        """Load and process PDF file"""
        try:
            if not os.path.exists(pdf_path):
                print(f"Error: PDF file '{pdf_path}' not found!")
                return None
            
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            print(f"✓ Loaded {len(documents)} pages from '{os.path.basename(pdf_path)}'")
            return documents
        except Exception as e:
            print(f"Error loading PDF: {str(e)}")
            return None
    
    def chunk_documents(self, documents):
        """Split documents into chunks"""
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_documents(documents)
            print(f"✓ Split into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            print(f"Error chunking documents: {str(e)}")
            return None
    
    def add_pdf_to_store(self, pdf_path):
        """Add a new PDF to the vector store"""
        try:
            # Load PDF
            documents = self.load_pdf(pdf_path)
            if documents is None:
                return False
            
            # Chunk documents
            chunks = self.chunk_documents(documents)
            if chunks is None:
                return False
            
            # Add to vector store
            if self.vector_store is None:
                # Create new vector store
                self.vector_store = FAISS.from_documents(chunks, self.embeddings)
                print(f"✓ Created new vector store with PDF")
            else:
                # Append to existing vector store
                self.vector_store.add_documents(chunks)
                print(f"✓ Appended PDF to existing vector store")
            
            # Save vector store
            self.save_store()
            return True
        except Exception as e:
            print(f"Error adding PDF to store: {str(e)}")
            return False
    
    def save_store(self):
        """Save vector store to disk"""
        try:
            if self.vector_store is not None:
                self.vector_store.save_local(self.store_path)
                print(f"✓ Vector store saved to '{self.store_path}'")
                return True
            return False
        except Exception as e:
            print(f"Error saving vector store: {str(e)}")
            return False
    
    def retrieve_context(self, query, k=3):
        """Retrieve relevant context from all PDFs"""
        try:
            # Check if vector store exists
            if self.vector_store is None:
                return ""
            
            results = self.vector_store.similarity_search(query, k=k)
            context = "\n".join([doc.page_content for doc in results])
            return context
        except Exception as e:
            print(f"Error retrieving context: {str(e)}")
            return ""
    
    def get_store_info(self):
        """Get information about current vector store"""
        if self.vector_store is None:
            return "No vector store loaded. Please add PDFs first."
        try:
            doc_count = self.vector_store.index.ntotal
            return f"✓ Vector store contains {doc_count} vectors from loaded PDFs"
        except:
            return "Vector store loaded but info unavailable"
    
    def is_store_loaded(self):
        """Check if vector store is loaded"""
        return self.vector_store is not None