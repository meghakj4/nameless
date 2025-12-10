def run_chatbot(model, vector_manager):
    """Interactive command line chatbot with PDF context"""
    print("=" * 50)
    print("Welcome to the PDF-Based Chatbot!")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'add-pdf' to add a new PDF")
    print("Type 'info' to see vector store information")
    print("=" * 50)
    print()
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit']:
            print("\nChatbot: Goodbye! Thanks for chatting.")
            break
        
        if user_input.lower() == 'add-pdf':
            pdf_path = input("Enter PDF file path: ").strip()
            print()
            vector_manager.add_pdf_to_store(pdf_path)
            print()
            continue
        
        if user_input.lower() == 'info':
            info = vector_manager.get_store_info()
            print(f"\n{info}\n")
            continue
        
        if not user_input:
            print("Chatbot: Please enter a question or message.\n")
            continue
        
        try:
            if not vector_manager.is_store_loaded():
                print("Chatbot: No PDFs loaded yet. Use 'add-pdf' to add files.\n")
                continue
            
            pdf_context = vector_manager.retrieve_context(user_input, k=3)
            if not pdf_context.strip():
                print("Chatbot: No relevant information found in PDFs. Please ask a different question.\n")
                continue
            
            prompt = f"""You are a helpful assistant. Answer the user's question based on the following context from the PDF:

Context from PDF:
{pdf_context}

User Question: {user_input}

Provide a clear and concise answer based on the context. If the answer is not in the provided context, say "I don't have this information in the provided PDF." """
            
            response = model.invoke(prompt)
            print(f"\nChatbot: {response.content}\n")
        except Exception as e:
            print(f"\nChatbot: Sorry, an error occurred: {str(e)}\n")