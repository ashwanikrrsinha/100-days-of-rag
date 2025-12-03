# Day 8: Streamlit Frontend (The "Chat with PDF" App)

## 🎯 The Goal
To replace the terminal interface with a user-friendly Web Application.
We used **Streamlit** to build a dashboard where users can upload PDFs via drag-and-drop and chat with them in a ChatGPT-style interface.

## 🧠 Core Concept: State Management
Web apps usually "forget" everything when you click a button (because the script re-runs).
To fix this, we used `st.session_state`:
* **`st.session_state["vector_store"]`**: Keeps the AI memory alive even when the user clicks "Chat".
* **`st.session_state["messages"]`**: Stores the chat history so the conversation stays on screen.

## 🛠️ Tech Stack
* **Frontend:** `Streamlit` (Pure Python UI)
* **Processing:** `LangChain` (PyPDFLoader, TextSplitter)
* **Backend:** `ChromaDB` (In-memory for this session)
* **AI:** `Gemini 2.0 Flash`

## 🏃‍♂️ How to Run
This is a web app, so we don't use `python app.py`.

```bash
# In the terminal
streamlit run app.py

---

A browser tab will open at localhost:8501.

- Upload a PDF in the sidebar.

- Click "Process Document".

- Ask questions in the chat bar.