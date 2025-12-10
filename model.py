from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# Initialize and export model instance
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.01,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)