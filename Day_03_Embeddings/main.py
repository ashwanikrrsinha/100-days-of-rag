# -----------------------------------------------
"""
🧩 Chunk 1: The Setup & Model Selection

The Goal: Prepare the environment and select the correct tool for the job.

The Algorithm: Model Selection Strategy. In previous days, we used a "Generative" model (gemini-2.0-flash) because we wanted it to talk. Today, we need a "Representation" model. We must specifically configure the client to use an Embedding Model (specifically text-embedding-004), which is optimized for math, not chatting.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load Secrets
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key not found!")

genai.configure(api_key=api_key)

# Note: We don't create a 'model' object here like before. 
# We will call the embedding function directly in the next chunk.

# -----------------------------------------------

"""
🧩 Chunk 2: The Mathematical Transformation

The Goal: Convert a string of text into a list of floating-point numbers.

The Algorithm: API Call (Embedding).

Input: Take a raw string (e.g., "The quick brown fox").

Process: Send it to the embed_content endpoint (NOT generate_content).

Model: Specify models/text-embedding-004.

Output: Receive a response object containing the vector data.
"""

text_input = "The quick brown fox jumps over the lazy dog."

print(f"Converting text: '{text_input}'...")

# LOGIC: We call 'embed_content' because we don't want a text reply. 
# We want the mathematical representation.
response = genai.embed_content(
    model="models/text-embedding-004",
    content=text_input
)

# -----------------------------------------------
"""
🧩 Chunk 3: Data Extraction (Parsing)

The Goal: Isolate the actual coordinate list from the API's JSON response.

The Algorithm: Dictionary Parsing. The API returns a wrapper (a dictionary) containing metadata. 
               We need to drill down into the specific key ['embedding'] to get the raw list of numbers.
"""

# The API returns something like: {'embedding': [0.1, -0.5, ...], 'usage_metadata': ...}
# We only want the list.
vector = response['embedding']

print("Vector extracted successfully.")

#-----------------------------------------------

"""
🧩 Chunk 4: Verification (The Dimensions)

The Goal: Verify the "shape" of our data to ensure it's valid for future use.

The Algorithm: Dimensionality Check. Every embedding model has a specific "fingerprint" size. For Gemini's text-embedding-004, every single 
               piece of text—whether it is one word or one page—gets converted into exactly 768 numbers.

If len(vector) == 768, we succeeded.

If not, something is wrong.
"""

# 1. Check the length
vector_length = len(vector)
print(f"\nVector Dimensions: {vector_length}") 

# 2. Peek at the data
# We print just the first 5 numbers to prove they are floats, not text.
print(f"First 5 coordinates: {vector[:5]}")

#-----------------------------------------------