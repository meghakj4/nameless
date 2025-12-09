from langchain_google_genai import ChatGoogleGenerativeAI

model = ChatGoogleGenerativeAI(
    model="gemini-3-pro-preview",
    temperature=0.01,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)



response = model.invoke("WHen was shakespeare born?")
print(response.content)
# print(response.generations[0][0].text)



####
# Step 1=> Built simple terminal chatbot with single subject context
# Step 2 => Add all contexts
# Final Step => Build the web chatbot (user, if needed => memory)