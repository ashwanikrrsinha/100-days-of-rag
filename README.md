# 🧠 100 Days of RAG
I am undertaking a challenge to build 100 RAG (Retrieval-Augmented Generation) projects in 100 days to master LLM engineering.

## 🏆 Progress Tracker

| Day | Project Name | Tech Stack | Key Concepts | Status |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [The Naive RAG](./Day_01_Naive_RAG) | Python, Gemini | Prompt Engineering, Context Injection, Safety Filters | ✅ Done |
| 02 | [Text File RAG](./Day_02_Text_File_RAG) | Python, Gemini | Data Ingestion, .env Security, File I/O | ✅ Done |
| 03 | [Embeddings Generator](./Day_03_Embeddings) | Python, Gemini | Vector Space, Embeddings, Dimensionality (768) | ✅ Done |
| 04 | [Simple Vector Store](./Day_04_Vector_Store) | Python, Numpy | Cosine Similarity, Vector Search, Ranking | ✅ Done |
| 05 | [Chat with PDF](./Day_05_Chat_with_PDF) | Python, pypdf | Chunking, Overlap, Full RAG Pipeline | ✅ Done |
| 06 | [ChromaDB Vector Store](./Day_06_ChromaDB) | Python, ChromaDB | Persistent Storage, Database, Upserting | ✅ Done |
| 07 | [LangChain Refactor](./Day_07_LangChain_Intro) | Python, LangChain | Frameworks, Document Loaders, Text Splitters | ✅ Done |
| 08 | [Streamlit Frontend](./Day_08_Streamlit_Frontend) | Python, Streamlit | UI/UX, Session State, File Uploads | ✅ Done |
| 09 | [Context-Aware Chatbot](./Day_09_Chat_History) | Python, Streamlit | Chat History, Query Reformulation, LangChain Chains | ✅ Done |
| 10 | TBD | ... | ... | ⏳ |

---

## 📂 Daily Log

### Day 1: The Naive RAG (Simple Context Injection)
**Goal:** Build the simplest possible RAG system. Instead of using complex databases, we manually "inject" knowledge into the AI's prompt to force it to answer questions about data it has never seen before.

**Key Learnings:**
1.  **The RAG "Sandwich":** RAG is just instruction + context + question wrapped in a single prompt.
2.  **Safety Filters:** Words like "Secret" or "Pass-phrase" trigger Gemini's safety refusal. We had to sanitize inputs to get a response.
3.  **Environment Security:** Learned to use `.env` files to hide API keys instead of hardcoding them.

**Tech Stack:**
* **Model:** `gemini-2.0-flash`
* **Library:** `google-generativeai`

**Architecture:**
`[Input Question]` --> `[Inject Hardcoded Context]` --> `[Gemini LLM]` --> `[Answer]`

---

### Day 2: Text File RAG (Dynamic Ingestion)
**Goal:** Build a dynamic RAG system that reads from external files instead of hardcoded strings. This mimics real-world apps where data lives in documents, not code.

**Key Learnings:**
1.  **Dynamic Ingestion:** Wrote a Python function to open `.txt` files and load content into memory.
2.  **Environment Security:** Implemented `python-dotenv` to load API keys from a `.env` file, keeping secrets out of GitHub.
3.  **Scalability:** The same Python script can now handle any text topic just by swapping the `.txt` file (Separation of Data vs. Code).

**Tech Stack:**
* **Libraries:** `google-generativeai`, `python-dotenv`
* **Data Source:** Local `.txt` file (`mars_colony_guide.txt`)

**Architecture:**
`[Text File]` --> `[Python Read Function]` --> `[RAG Prompt]` --> `[Gemini LLM]` --> `[Answer]`

---

### Day 3: Embeddings Generator (Text to Math)
**Goal:** Create a script that converts human text into Vector Embeddings (lists of floating-point numbers) so computers can understand the "meaning" behind words.

**Key Learnings:**
1.  **Vector Space:** AI views text as coordinates in a multi-dimensional map.
2.  **The Model:** Used `text-embedding-004` (optimized for math) instead of `gemini-2.0-flash` (optimized for chat).
3.  **Dimensionality:** Discovered that Gemini converts every piece of text into exactly **768 numbers**.

**Tech Stack:**
* **Model:** `models/text-embedding-004`
* **Function:** `genai.embed_content()`

**Architecture:**
`[Text Input]` --> `[Embedding Model]` --> `[Vector (List of 768 floats)]`

---

### Day 4: The Vector Store (Semantic Search)
**Goal:** Build a custom search engine from scratch that uses vector mathematics to find the most relevant information for a user's query.

**Key Learnings:**
1.  **Cosine Similarity:** Learned the math formula `(A . B) / (|A| * |B|)` to calculate the "angle" or similarity between two pieces of text.
2.  **Vector Store:** Built a simple in-memory database (list of dictionaries) to store text alongside its embedding.
3.  **Semantic Ranking:** The system correctly identified that "Currency" is related to "Buying", even without keyword matching.

**Tech Stack:**
* **Library:** `numpy` for dot products and linear algebra.
* **Concept:** k-Nearest Neighbors (k-NN) search logic.

**Architecture:**
`[Query Vector]` vs `[All Document Vectors]` -> `[Calculate Scores]` -> `[Sort & Pick Top 1]`

---

### Day 5: Chat with PDF (The Full Pipeline)
**Goal:** Combine all previous concepts to build a functioning app that reads a PDF and answers questions about it using Vector Search.

**Key Learnings:**
1.  **Chunking Strategy:** Learned to split large documents into smaller pieces (1000 chars) using a "Sliding Window" with overlap to preserve context.
2.  **PDF Parsing:** Used `pypdf` to extract raw text from binary files.
3.  **Pipeline Integration:** Successfully connected Ingestion -> Chunking -> Embedding -> Search -> Generation into a single workflow.

**Tech Stack:**
* **Libraries:** `pypdf`, `numpy`, `google-generativeai`
* **Algorithm:** Sliding Window Chunking + Cosine Similarity Search.

**Architecture:**
`[PDF]` -> `[Chunks]` -> `[Vector Search]` -> `[Relevant Chunk]` -> `[LLM Answer]`

---

### Day 6: ChromaDB Vector Store (Persistent Memory)
**Goal:** Upgrade the storage backend from a temporary Python list to a dedicated Vector Database (ChromaDB) to enable long-term memory and efficient querying.

**Key Learnings:**
1.  **Persistence:** Created a database that saves data to the local disk (`./chroma_db`), allowing the app to remember information across restarts.
2.  **Efficiency:** Learned that Vector DBs eliminate the need to pay for re-embedding the same data repeatedly (Upsert logic).
3.  **ChromaDB API:** Mastered the basics of creating collections, adding documents, and querying nearest neighbors without manual math.

**Tech Stack:**
* **Database:** `chromadb`
* **Model:** `models/text-embedding-004`

**Architecture:**
`[Documents]` -> `[Embedding]` -> `[ChromaDB (Disk)]` <-> `[Query]`

---

### Day 7: LangChain Intro (The Modern Stack)
**Goal:** Refactor the manual RAG pipeline from Day 5 using the **LangChain** framework to reduce code complexity and use industry-standard tools.

**Key Learnings:**
1.  **LangChain Abstractions:** Learned how `PyPDFLoader` and `RecursiveCharacterTextSplitter` handle data ingestion much better than manual scripts.
2.  **Vector Store Integration:** Used `Chroma.from_documents` to handle embedding and storage in a single line of code.
3.  **Component Chaining:** Connected the Retriever to the LLM manually (conceptually preparing for "Chains").

**Tech Stack:**
* **Framework:** `LangChain`
* **Connectors:** `langchain-google-genai`, `langchain-chroma`

**Architecture:**
`[PDF]` -> `[PyPDFLoader]` -> `[TextSplitter]` -> `[ChromaDB]` -> `[Retriever]` -> `[LLM]`

---

### Day 8: Streamlit Frontend (The Web App)
**Goal:** Build a browser-based user interface so users can interact with the RAG system without touching the terminal.

**Key Learnings:**
1.  **Streamlit Basics:** Built a Sidebar for inputs and a Main Area for chat.
2.  **Session State:** Learned how to persist variables (like the Vector Database and Chat History) across app re-runs.
3.  **UI Feedback:** Added spinners (`st.spinner`) and success messages to improve user experience during the slow PDF processing step.

**Tech Stack:**
* **UI Library:** `streamlit`
* **Command:** `streamlit run app.py`

**Architecture:**
`[User UI]` <-> `[Session State (Memory)]` <-> `[ChromaDB]` -> `[LangChain Retrieval]` -> `[Gemini Answer]`

---

### Day 9: Context-Aware Chatbot (Adding Memory)
**Goal:** Upgrade the RAG system to handle follow-up questions by implementing "Conversational Memory."

**Key Learnings:**
1.  **The Amnesia Problem:** Vector Search fails on pronouns ("he", "it") because it lacks context.
2.  **Query Reformulation:** Implemented a "Rewriter" step using `create_history_aware_retriever` that converts follow-up questions into standalone search queries.
3.  **LangChain Chains:** Composed multiple chains (History Chain + Document Chain) into a single `create_retrieval_chain` workflow.

**Tech Stack:**
* **Chains:** `create_history_aware_retriever`, `create_retrieval_chain`
* **Prompting:** `ChatPromptTemplate`, `MessagesPlaceholder`

**Architecture:**
`[Query + History]` -> `[Rewriter LLM]` -> `[Standalone Query]` -> `[Vector Store]` -> `[Answer LLM]`