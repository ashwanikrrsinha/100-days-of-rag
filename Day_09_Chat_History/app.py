import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# --- SETUP ---
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("API Key not found!")
    st.stop()

# --- UI CONFIG ---
st.set_page_config(page_title="Context-Aware RAG", layout="wide")
st.title("🧠 Context-Aware Chatbot (Day 9)")
st.caption("I remember what you said previously!")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Data Source")
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    process_btn = st.button("Process Document")

# --- STATE MANAGEMENT ---
if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# --- 1. PROCESSING LOGIC ---
if process_btn and uploaded_file:
    with st.spinner("Processing..."):
        # Save temp
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Load & Split
        loader = PyPDFLoader("temp.pdf")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        
        # Embed & Store
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)
        vector_store = Chroma.from_documents(chunks, embeddings) # In-memory for session
        
        st.session_state["vector_store"] = vector_store
        st.success("PDF Processed!")

# --- 2. MAIN CHAT LOGIC ---
if st.session_state["vector_store"]:
    # Display History
    for msg in st.session_state["chat_history"]:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

    # Handle Input
    if user_input := st.chat_input("Ask something..."):
        
        # A. Show User Message
        st.session_state["chat_history"].append(HumanMessage(content=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        # B. Generate Answer
        with st.chat_message("assistant"):
            llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key, temperature=0)
            retriever = st.session_state["vector_store"].as_retriever()
            
            # --- THE NEW PART: HISTORY AWARENESS ---
            
            # 1. Define sub-prompt to rephrase the question
            contextualize_q_system_prompt = """
            Given a chat history and the latest user question which might reference context in the chat history, 
            formulate a standalone question which can be understood without the chat history. 
            Do NOT answer the question, just reformulate it if needed and otherwise return it as is.
            """
            
            contextualize_q_prompt = ChatPromptTemplate.from_messages([
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ])
            
            # 2. Create the "History Aware Retriever" (The Rewriter)
            history_aware_retriever = create_history_aware_retriever(
                llm, retriever, contextualize_q_prompt
            )
            
            # 3. Define the Answer Prompt (Standard RAG)
            qa_system_prompt = """
            You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
            If you don't know the answer, just say that you don't know. 
            
            {context}
            """
            
            qa_prompt = ChatPromptTemplate.from_messages([
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"), # Context goes here too
                ("human", "{input}"),
            ])
            
            # 4. Create the Final Chain
            question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
            rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
            
            # 5. Run the Chain
            with st.spinner("Thinking..."):
                response = rag_chain.invoke({
                    "input": user_input,
                    "chat_history": st.session_state["chat_history"]
                })
            
            # Show Answer
            st.markdown(response["answer"])
            
            # Save to History
            st.session_state["chat_history"].append(AIMessage(content=response["answer"]))

else:
    st.info("Please upload a PDF to start.")