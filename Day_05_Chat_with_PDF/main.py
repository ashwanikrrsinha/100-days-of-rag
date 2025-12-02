import os
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader

# --- CONFIGURATION ---
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# --- STEP 2: PDF LOADER ---
def load_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# --- STEP 3: CHUNKER ---
def split_text(text, chunk_size=1000, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap 
    return chunks

# --- STEP 4: RETRIEVAL ---
def find_best_chunk(query, chunks):
    # Embed Query
    query_vec = genai.embed_content(
        model="models/text-embedding-004", content=query
    )['embedding']
    
    chunk_data = []
    print(f"Scanning {len(chunks)} chunks...")
    
    # Embed Chunks & Calculate Score
    for chunk in chunks:
        chunk_vec = genai.embed_content(
            model="models/text-embedding-004", content=chunk
        )['embedding']
        
        # Cosine Similarity Formula
        dot_product = np.dot(query_vec, chunk_vec)
        norm_a = np.linalg.norm(query_vec)
        norm_b = np.linalg.norm(chunk_vec)
        score = dot_product / (norm_a * norm_b)
        
        chunk_data.append({"text": chunk, "score": score})
    
    # Sort by Score
    chunk_data.sort(key=lambda x: x["score"], reverse=True)
    return chunk_data[0]

# --- STEP 5: GENERATION ---
def ask_gemini(chunk_text, user_question):
    model = genai.GenerativeModel('gemini-2.0-flash')
    prompt = f"""
    Answer the question based ONLY on the context below.
    ### CONTEXT:
    {chunk_text}
    ### QUESTION:
    {user_question}
    """
    response = model.generate_content(prompt)
    return response.text

# --- EXECUTION ---
if __name__ == "__main__":
    
    # 1. Setup
    pdf_file = "document.pdf" # <--- MAKE SURE THIS FILE EXISTS
    if not os.path.exists(pdf_file):
        print("Error: 'document.pdf' not found in this folder.")
        exit()

    # 2. Ingest
    print("Reading PDF...")
    raw_text = load_pdf(pdf_file)
    chunks = split_text(raw_text)
    print(f"Split PDF into {len(chunks)} chunks.")

    # 3. Interactive Loop
    while True:
        query = input("\nAsk a question (or type 'quit'): ")
        if query.lower() == 'quit':
            break
            
        print("Searching...")
        best_match = find_best_chunk(query, chunks)
        print(f"Best match score: {best_match['score']:.4f}")
        
        print("Generating answer...")
        answer = ask_gemini(best_match['text'], query)
        print(f"\n--- AI Answer ---\n{answer}\n")