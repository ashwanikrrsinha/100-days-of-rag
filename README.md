# 🧠 100 Days of RAG
I am undertaking a challenge to build 100 RAG (Retrieval-Augmented Generation) projects in 100 days to master LLM engineering.

## 🏆 Progress Tracker

| Day | Project Name | Tech Stack | Key Concepts | Status |
| :--- | :--- | :--- | :--- | :--- |
| 01 | [The Naive RAG](./Day_01_Naive_RAG) | Python, Gemini | Prompt Engineering, Context Injection, Safety Filters | ✅ Done |
| 02 | TBD | ... | ... | ⏳ |

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
[Input Question] --> [Inject Hardcoded Context] --> [Gemini LLM] --> [Answer]