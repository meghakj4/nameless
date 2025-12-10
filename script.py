import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from model_loader import load_latest_model

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

# Load the trained vector store model
vector_manager = load_latest_model()

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
    # Check if model is loaded
    if vector_manager is None:
        print("Failed to load model. Please run:")
        print("  python one_timer/create_syllab_iq_model.py")
    else:
        chat_bot()

####
# Step 1=> Built simple terminal chatbot with single subject context ✓
# Step 2 => Add all contexts ✓
# Step 3 => One-time model creation and loading ✓
# Final Step => Build the web chatbot (user, if needed => memory)
