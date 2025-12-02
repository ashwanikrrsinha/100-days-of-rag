import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- SETUP ---
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("API Key not found!")

# --- 1. LOAD & SPLIT ---
# Ensure 'document.pdf' exists in this folder!
if not os.path.exists("document.pdf"):
    print("Error: Please add 'document.pdf' to this folder.")
    exit()

print("Loading and Chunking PDF...")
loader = PyPDFLoader("document.pdf")
docs = loader.load()

# Intelligent Chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
chunks = splitter.split_documents(docs)
print(f"Generated {len(chunks)} chunks.")

# --- 2. VECTOR STORE ---
print("Embedding data into ChromaDB...")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)

# This one line handles: Embedding -> Upserting -> Saving
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# --- 3. RETRIEVAL ---
query = input("\nAsk a question about the PDF: ")

# Retrieve top 3 chunks
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
relevant_docs = retriever.invoke(query)

print(f"\nFound {len(relevant_docs)} relevant context chunks.")

# --- 4. GENERATION ---
print("Generating Answer...")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

# Combine context
context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

prompt = f"""
Answer the user's question based on the context provided below.
If the answer is not in the context, say "I don't know".

Context:
{context_text}

Question: 
{query}
"""

response = llm.invoke(prompt)
print("\n=== ANSWER ===")
print(response.content)