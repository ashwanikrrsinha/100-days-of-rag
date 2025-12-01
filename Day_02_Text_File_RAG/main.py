"""
🧩 Chunk 1: The Setup & Security Layer

The Goal: Connect our Python script to the Google Gemini brain without exposing our passwords (API Keys) to the public.

The Algorithm: Environment Variable Loading. Instead of writing the key in the code, we tell the code: "Look for a hidden file named .env 
one folder above me, read the secret key inside it, and authenticate with Google."

"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# LOGIC: The .env file is in the parent folder (100-days-of-rag), 
# but this script is inside (Day_02_Text_File_RAG). 
# So we use "../.env" to tell Python to look "up one level".
load_dotenv(dotenv_path=".env") 

# Retrieve the key safely
api_key = os.getenv("GEMINI_API_KEY")

# Simple Validation Algorithm: If key is missing, stop immediately.
if not api_key:
    raise ValueError("API Key not found! Check your .env file.")

# Authenticate
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

# --------------------------------------------------------------

"""

🧩 Chunk 2: The Data Ingestion Engine

The Goal: Move data from your Hard Drive (Storage) into the Python Memory (RAM).

The Algorithm: File I/O with Exception Handling.

Open: Attempt to open the file in "Read Mode" ("r").

Read: Extract all text as a single string.

Close: Close the file to free up system resources (with open does this automatically).

Exception Handling: If the file doesn't exist, don't crash. Catch the error and tell the user nicely.

"""


def read_text_file(file_path):
    # Try to open the file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read() # Return the text string
            
    # If the file is missing, run this fallback logic
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

# Execution: Actually call the function
filename = "mars_colony_guide.txt"
context_text = read_text_file(filename)

# Verification Logic
if not context_text:
    exit() # Stop if no data

# -------------------------------------------------------------

"""

🧩 Chunk 3: The RAG "Prompt Engineering"

The Goal: Create a prompt that forces the AI to use our file, not its own training data.

The Algorithm: Context Injection (The Sandwich Method). We treat the prompt as a template with three slots.

Slot 1 (System): "You are an expert. Use provided text."

Slot 2 (Data): Paste the variable context_text we read in Chunk 2.

Slot 3 (Query): The user's specific question.

"""

user_question = "What is the currency on Mars and who founded the colony?"

# The f-string is our "Template Engine"
rag_prompt = f"""
You are a Mars Colony expert. Answer the question based ONLY on the context below.

### CONTEXT:
{context_text}

### QUESTION:
{user_question}
"""

# -------------------------------------------------------------

""" 
🧩 Chunk 4: Retrieval & Generation

The Goal: Send the "Sandwich" to Google and print the result.

The Algorithm: API Request/Response Cycle. We send the string. The model processes the tokens. It predicts the most likely next words based specifically on the text we provided in the prompt.

"""

print("Asking Gemini...")
response = model.generate_content(rag_prompt)

print("\n--- ANSWER ---")
print(response.text)

