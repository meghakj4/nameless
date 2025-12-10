import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from vector_store_manager import VectorStoreManager

# Load environment variables from .env file
load_dotenv()

# Initialize the model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.01,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Initialize vector store manager
vector_manager = VectorStoreManager(store_path="vector_store")

def load_pdfs_on_startup():
    """Load and store PDFs before chatbot starts"""
    print("=" * 50)
    print("PDF Learning Phase")
    print("=" * 50)
    print()
    
    pdf_files = []
    
    # Check if PDFs folder exists
    pdfs_folder = "pdfs"
    if os.path.exists(pdfs_folder):
        # Load all PDFs from pdfs folder
        for filename in os.listdir(pdfs_folder):
            if filename.endswith(".pdf"):
                pdf_path = os.path.join(pdfs_folder, filename)
                pdf_files.append(pdf_path)
    
    # Add the specific PDF file
    specific_pdf = r"C:\Users\Megha\Downloads\MOD5_Notes.pdf"
    if os.path.exists(specific_pdf):
        pdf_files.append(specific_pdf)
    
    # If no PDFs found
    if not pdf_files:
        print("⚠ No PDF files found!")
        print(f"Please place PDFs in '{pdfs_folder}/' folder or check the path.")
        print()
        add_more = input("Do you want to add a PDF manually? (yes/no): ").strip().lower()
        if add_more == 'yes':
            pdf_path = input("Enter PDF file path: ").strip()
            if os.path.exists(pdf_path):
                pdf_files.append(pdf_path)
            else:
                print(f"Error: File not found at {pdf_path}")
                return False
        else:
            print("Starting chatbot without any PDFs...\n")
            return True
    
    # Load all PDFs
    print(f"Found {len(pdf_files)} PDF file(s). Loading...\n")
    
    for pdf_path in pdf_files:
        print(f"Loading: {os.path.basename(pdf_path)}")
        success = vector_manager.add_pdf_to_store(pdf_path)
        if not success:
            print(f"Failed to load: {pdf_path}\n")
        else:
            print()
    
    # Display vector store info
    info = vector_manager.get_store_info()
    print(f"\n{info}")
    print("=" * 50)
    print("PDF Learning Complete! Ready to chat.\n")
    print()
    
    return True

def chat_bot():
    """Interactive command line chatbot with PDF context"""
    print("=" * 50)
    print("Welcome to the PDF-Based Chatbot!")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'add-pdf' to add a new PDF")
    print("Type 'info' to see vector store information")
    print("=" * 50)
    print()
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Exit condition
        if user_input.lower() in ['exit', 'quit']:
            print("\nChatbot: Goodbye! Thanks for chatting.")
            break
        
        # Add new PDF
        if user_input.lower() == 'add-pdf':
            pdf_path = input("Enter PDF file path: ").strip()
            print()
            vector_manager.add_pdf_to_store(pdf_path)
            print()
            continue
        
        # Get vector store info
        if user_input.lower() == 'info':
            info = vector_manager.get_store_info()
            print(f"\n{info}\n")
            continue
        
        # Skip empty inputs
        if not user_input:
            print("Chatbot: Please enter a question or message.\n")
            continue
        
        try:
            # Retrieve context from PDF
            pdf_context = vector_manager.retrieve_context(user_input, k=3)
            
            # Check if context was found
            if not pdf_context.strip():
                print("Chatbot: No relevant information found in PDFs. Please ask a different question.\n")
                continue
            
            # Create prompt with context
            prompt = f"""You are a helpful assistant. Answer the user's question based on the following context from the PDF:

Context from PDF:
{pdf_context}

User Question: {user_input}

Provide a clear and concise answer based on the context. If the answer is not in the provided context, say "I don't have this information in the provided PDF." """
            
            # Get response from the model
            response = model.invoke(prompt)
            print(f"\nChatbot: {response.content}\n")
        
        except Exception as e:
            print(f"\nChatbot: Sorry, an error occurred: {str(e)}\n")

if __name__ == "__main__":
    # Step 1: Load and learn PDFs before chatbot starts
    pdf_loading_success = load_pdfs_on_startup()
    
    # Step 2: Start chatbot after PDFs are loaded
    if pdf_loading_success:
        chat_bot()
    else:
        print("Failed to initialize chatbot. Please check your PDFs.")

####
# Step 1=> Built simple terminal chatbot with single subject context ✓
# Step 2 => Add all contexts ✓
# Final Step => Build the web chatbot (user, if needed => memory)
