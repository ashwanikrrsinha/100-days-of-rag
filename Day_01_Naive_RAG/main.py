import os
import google.generativeai as genai
from dotenv import load_dotenv  # <--- Import this

load_dotenv()  # <--- This reads the .env file
api_key = os.getenv("GEMINI_API_KEY") # <--- Get the key safely

os.environ["Gemini_API_Key"] = api_key
genai.configure(api_key=os.environ["Gemini_API_Key"])

model = genai.GenerativeModel('gemini-2.0-flash')

txt_context = """
The secret pass-phrase for the hidden bunker is 'Purple-Banana-42'. 
The bunker is located under the ancient oak tree in Central Park. 
It was built in 2024 by a secret society of coders known as 'The 100'.
"""

user_question = "What is the pass-phrase for the bunker and who built it?"

rag_prompt = f"""
You are a helpful assistant. Answer the user's question based ONLY on the context provided below.
If the answer is not in the context, say "I don't know."

### CONTEXT:
{txt_context}

### QUESTION:
{user_question}
"""

print("Thinking...")
response = model.generate_content(rag_prompt)

print("\n--- RAG ANSWER ---")
print(response.text)