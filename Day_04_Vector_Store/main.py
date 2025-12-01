#--------------------------------------------------------
# Day 04: Vector Store
#--------------------------------------------------------

import os
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# --- HELPER: GET EMBEDDING ---
def get_embedding(text):
    response = genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )
    return response['embedding']

#--------------------------------------------------------

"""
🧩 Chunk 1: The Math (Cosine Similarity)

The Goal: Calculate how similar two vectors are (0 to 1). The Formula: (A . B) / (|A| * |B|) (Dot Product divided by the Product of Magnitudes)
"""

def cosine_similarity(vec_a, vec_b):
    # Calculate Dot Product
    dot_product = np.dot(vec_a, vec_b)
    
    # Calculate Magnitude (Length of the arrow)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    
    # Avoid division by zero
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return dot_product / (norm_a * norm_b)

#--------------------------------------------------------

"""
🧩 Chunk 3: The Search Algorithm

The Goal: Find the best match for the user's question.
"""

def search_vector_store(query):
    # 1. Convert Query to Vector
    query_vec = get_embedding(query)
    
    # 2. Compare against EVERY document in the store
    results = []
    for item in vector_store:
        doc_vec = item["vector"]
        score = cosine_similarity(query_vec, doc_vec)
        
        results.append({
            "text": item["text"],
            "score": score
        })
    
    # 3. Sort by highest score first
    # (Lambda function explanation: Sort based on the 'score' key)
    results.sort(key=lambda x: x["score"], reverse=True)
    
    print("\n--- SEARCH RESULTS ---")
    for result in results:
        print(f"Score: {result['score']:.4f} | Text: {result['text']}")

    print(f"\nWINNER: '{results[0]['text']}'")

#--------------------------------------------------------

# --- MAIN EXECUTION ---
if __name__ == "__main__":

    """
    🧩 Chunk 2: The "Vector Store" (Ingestion)

    The Goal: Create a fake "Knowledge Base" and convert it all to numbers.
    """
    # 1. Our Documents (The Knowledge Base)
    documents = [
        "The mars colony was founded by Elon's clone.",
        "Mars has a currency called Red-Credits.",
        "Apples are a fruit that grow on trees.",
        "The capital of France is Paris.",
        "You need an Aero-2000 suit to breathe on Mars."
    ]

    # 2. The Vector Store (A simple list to hold data)
    vector_store = []

    print("Building Vector Store...")
    for doc in documents:
        # Get the embedding (using the function from Day 3)
        vec = get_embedding(doc) # We will define this helper function
        
        # Store text AND vector together
        vector_store.append({
            "text": doc,
            "vector": vec
        })
        print(f"Stored: '{doc[:20]}...'")


    # 3. USER QUERY
    user_query = "How do I buy things on Mars?"
    print(f"\n--- USER QUERY: '{user_query}' ---")

    search_vector_store(user_query)
#--------------------------------------------------------