# 🧠 100 Days of RAG
I am undertaking a challenge to build 100 RAG (Retrieval-Augmented Generation) projects in 100 days to master LLM engineering.

## 🏆 Progress Tracker

| Day | Project Name | Tech Stack | Key Concepts | Status |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [The Naive RAG](./Day_01_Naive_RAG) | Python, Gemini | Prompt Engineering, Context Injection, Safety Filters | ✅ Done |
| 02 | [Text File RAG](./Day_02_Text_File_RAG) | Python, Gemini | Data Ingestion, .env Security, File I/O | ✅ Done |
| 03 | TBD | ... | ... | ⏳ |

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