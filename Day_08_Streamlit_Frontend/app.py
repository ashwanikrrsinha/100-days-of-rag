import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- SETUP ---
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found! Check .env file.")
    st.stop()

# --- UI CONFIG ---
st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("🤖 Chat with your PDF")
st.caption("Powered by Gemini 2.0 & LangChain")

# --- SIDEBAR: INPUT ---
with st.sidebar:
    st.header("Data Source")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    process_btn = st.button("Process Document")

# --- LOGIC: PROCESS PDF ---
if process_btn and uploaded_file:
    with st.spinner("Reading, Chunking, and Embedding..."):
        # 1. Save temp file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 2. Load & Split
        loader = PyPDFLoader("temp.pdf")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        
        # 3. Create Vector Store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
        
        # Note: We use a temporary in-memory DB for the session to avoid locking issues
        vector_store = Chroma.from_documents(chunks, embeddings)
        
        # Save to Session State
        st.session_state["vector_store"] = vector_store
        st.success(f"Processed {len(chunks)} chunks!")

# --- CHAT UI ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display History
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Handle Input
if prompt := st.chat_input("Ask something about the PDF..."):
    # 1. Show User Message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Process Answer
    if "vector_store" in st.session_state:
        with st.chat_message("assistant"):
            stream_container = st.empty()
            
            # Retrieve
            retriever = st.session_state["vector_store"].as_retriever(search_kwargs={"k": 3})
            relevant_docs = retriever.invoke(prompt)
            context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
            
            # Generate
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)
            rag_prompt = f"""
            You are a helpful assistant. Answer based ONLY on the context below.
            
            Context:
            {context_text}
            
            Question:
            {prompt}
            """
            
            response = llm.invoke(rag_prompt)
            st.markdown(response.content)
            
            # Save History
            st.session_state["messages"].append({"role": "assistant", "content": response.content})
    else:
        st.warning("Please upload and process a PDF first!")