import os
import sys
import pickle
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vector_store_manager import VectorStoreManager

def create_model():
    """Create and save a trained model from PDFs"""
    print("=" * 50)
    print("Creating Syllab IQ Model")
    print("=" * 50)
    print()
    
    # Initialize vector store with a temporary name
    model_name = f"syllab_iq_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    store_path = os.path.join("models", model_name)
    
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    vector_manager = VectorStoreManager(store_path=store_path)
    
    # Learn PDFs
    pdf_files = []
    
    # Check pdfs folder
    pdfs_folder = "pdfs"
    if os.path.exists(pdfs_folder):
        for filename in os.listdir(pdfs_folder):
            if filename.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(pdfs_folder, filename))
    
    if not pdf_files:
        print("⚠ No PDF files found!")
        print(f"Please place PDFs in '{pdfs_folder}/' folder or check the path.")
        return False
    
    print(f"Found {len(pdf_files)} PDF file(s). Learning...\n")
    
    for pdf_path in pdf_files:
        print(f"Learning: {os.path.basename(pdf_path)}")
        success = vector_manager.add_pdf_to_store(pdf_path)
        if not success:
            print(f"Failed to learn: {pdf_path}\n")
    
    # Display info
    info = vector_manager.get_store_info()
    print(f"\n{info}")
    
    # Save the model
    model_file = os.path.join("models", f"{model_name}.pkl")
    try:
        with open(model_file, "wb") as f:
            pickle.dump(vector_manager, f)
        print(f"\n✓ Model saved to '{model_file}'")
        print("=" * 50)
        print("Model creation complete!")
        print("=" * 50)
        return True
    except Exception as e:
        print(f"Error saving model: {str(e)}")
        return False

if __name__ == "__main__":
    create_model()