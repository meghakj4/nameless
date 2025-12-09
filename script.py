from langchain_google_genai import ChatGoogleGenerativeAI

import getpass
import os


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = ""

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