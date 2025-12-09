from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()


# Initialize the model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.01,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def chat_bot():
    """Interactive command line chatbot"""
    print("=" * 50)
    print("Welcome to the Interactive Chatbot!")
    print("Type 'exit' or 'quit' to end the conversation")
    print("=" * 50)
    print()
    
    while True:
        # Get user input
        user_input = input("You: ").strip()
        
        # Exit condition
        if user_input.lower() in ['exit', 'quit']:
            print("\nChatbot: Goodbye! Thanks for chatting.")
            break
        
        # Skip empty inputs
        if not user_input:
            print("Chatbot: Please enter a question or message.\n")
            continue
        
        try:
            # Get response from the model
            response = model.invoke(user_input)
            print(f"\nChatbot: {response.content}\n")
        
        except Exception as e:
            print(f"\nChatbot: Sorry, an error occurred: {str(e)}\n")

if __name__ == "__main__":
    chat_bot()

####
# Step 1=> Built simple terminal chatbot with single subject context
# Step 2 => Add all contexts
# Final Step => Build the web chatbot (user, if needed => memory)
