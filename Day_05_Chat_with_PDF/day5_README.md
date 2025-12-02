# Day 5: Chat with PDF (The Full RAG Pipeline)

## 🎯 The Goal
To build a functional application where a user can upload a PDF document and ask questions about it. The AI must answer based *only* on the content of that specific PDF.

## 🧠 Core Concept: "Chunking" (Solving the Context Limit)
The biggest challenge in RAG is **Input Size**.
* **The Problem:** You cannot feed a 100-page PDF into an LLM's prompt. It exceeds the "Context Window" (memory limit) and confuses the model.
* **The Solution:** We slice the document into smaller, manageable pieces called **Chunks**.

### The "Sliding Window" Algorithm
We don't just cut the text every 1000 characters. We use an **Overlap**.

* **Chunk Size:** 1000 characters.
* **Overlap:** 100 characters.

**Why Overlap?**
Imagine a sentence like: *"The secret code is [CUT] 12345."*
If we cut right in the middle, Chunk A has "The secret code is" and Chunk B has "12345". Neither chunk makes sense alone.
**Overlap** ensures that the end of Chunk A is repeated at the start of Chunk B, preserving the context across the cut.

## 🏗️ The Architecture (Pipeline)
We combined all previous days into a 5-step pipeline:

1.  **Ingestion (Day 2 Logic):**
    * **Tool:** `pypdf`
    * **Action:** Extract raw text from the binary PDF file.

2.  **Chunking (Day 5 Logic):**
    * **Action:** Split the raw text into a list of 1000-character strings.

3.  **Embedding (Day 3 Logic):**
    * **Tool:** `text-embedding-004`
    * **Action:** Convert the User's Question and the Chunks into Vectors (lists of 768 numbers).

4.  **Retrieval (Day 4 Logic):**
    * **Math:** Cosine Similarity.
    * **Action:** Compare the Question Vector against *every* Chunk Vector. Find the single chunk with the highest similarity score.

5.  **Generation (Day 1 Logic):**
    * **Tool:** `gemini-2.0-flash`
    * **Action:** Inject the "Winning Chunk" into the prompt and ask Gemini to answer.

## 📊 Visual Flow
`[PDF File]` -> `[Text Extraction]` -> `[Split into Chunks]`
      |
      v
`[User Question]` -> `[Vector Search]` -> `[Find Best Chunk]` -> `[Generate Answer]`

## 💻 Code Breakdown
* **`load_pdf()`**: Handles the file system and parsing.
* **`split_text()`**: Implements the sliding window logic.
* **`find_best_chunk()`**: The search engine. It performs the vector math.
* **`ask_gemini()`**: The final interface that talks to the user.

## 🏃‍♂️ How to Run
1.  Place a file named `document.pdf` in this folder.
2.  Run the script:
    ```bash
    python main.py
    ```
3.  Type your question when prompted.