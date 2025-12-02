import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

# --- SETUP ---
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Initialize ChromaDB (Persistent Storage)
# This will create a folder named 'chroma_db' in your directory
client = chromadb.PersistentClient(path="./chroma_db")


# 3. Create (or Get) a Collection
# Think of a collection like a SQL Table. Name it "rag_experiment".
collection = client.get_or_create_collection(name="rag_experiment")

# --- HELPER ---
def get_embedding(text):
    return genai.embed_content(
        model="models/text-embedding-004",
        content=text
    )['embedding']

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    """
    🧩 Chunk 3: Adding Data (Upsert)

        The Difference: Chroma needs 3 things:

        - IDs: A unique name for each chunk (e.g., "doc1", "doc2").

        - Embeddings: The vector list.

        - Documents: The actual text.
    """
    # 1. DATA INGESTION
    # Only add data if the collection is empty (to avoid duplicates for this test)
    if collection.count() == 0:
        print("Database is empty. Adding data...")
        documents = [
            "Mars is the fourth planet from the Sun.",
            "The capital of France is Paris.",
            "Python is a great language for AI.",
            "Elon Musk wants to colonize Mars.",
            "Croissants are a popular French pastry."
        ]
        
        for i, doc in enumerate(documents):
            print(f"Embedding doc {i}...")
            vec = get_embedding(doc)
            collection.add(
                ids=[str(i)],
                embeddings=[vec],
                documents=[doc]
            )
    else:
        print("Data already exists in DB. Skipping ingestion.")

    print(f"Collection Count: {collection.count()}")

    # 2. QUERY
    user_query = "Tell me about food in France"
    print(f"\nSearching for: '{user_query}'")
    
    query_vec = get_embedding(user_query) # 1. Embed Query
    
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=2 # 2. Ask Chroma for the Top 2 matches
    )
    
    # 3. DISPLAY
    print("\n--- RESULTS ---")
    # Chroma returns lists of lists (because you can query multiple things at once)
    first_result_docs = results['documents'][0]
    first_result_ids = results['ids'][0]
    
    for doc_id, doc_text in zip(first_result_ids, first_result_docs):
        print(f"ID: {doc_id} | Text: {doc_text}")