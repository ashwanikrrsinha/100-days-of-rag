# Day 9: Context-Aware Chatbot (Adding Memory)

## 🎯 The Goal
To solve the "Amnesia Problem" in RAG.
* **Old Behavior:** If you asked "Who is Elon?", then "When did **he** die?", the bot failed because it searched for "He" in the vector DB.
* **New Behavior:** The bot uses conversation history to rewrite queries. It changes "When did he die?" to "When did Elon Musk die?" *before* searching.

## 🧠 Core Concept: Query Reformulation
We introduced a **"Middleman" (The Rewriter)** into the pipeline.

1.  **Input:** User Question + Chat History.
2.  **Rewriter LLM:** Analyzes the history. If the question depends on history (like "he", "it", "that"), it creates a **Standalone Question**.
3.  **Retriever:** Uses the *Standalone Question* to search the Vector DB.
4.  **Answer LLM:** Uses the retrieved documents to answer the user.

## 🛠️ Key LangChain Chains
1.  **`create_history_aware_retriever`**: The "Rewriter" chain. It doesn't answer questions; it just fixes the search query.
2.  **`create_retrieval_chain`**: The final pipeline that connects the Rewriter, the Retriever, and the Answerer.

## 🏃‍♂️ How to Run
```bash
streamlit run app.py

---

Upload a PDF.

Ask a question about a person.

Follow up with "How old is he?" to test the memory