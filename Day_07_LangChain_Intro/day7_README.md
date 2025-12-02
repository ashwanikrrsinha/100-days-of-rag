# Day 7: Intro to LangChain (The Modern Stack)

## 🎯 The Goal
To refactor our manual RAG pipeline using **LangChain**, the industry-standard framework for building AI applications. This drastically reduces code volume and improves reliability.

## 🛠️ Key Components
We replaced manual Python logic with specialized LangChain classes:

### 1. `PyPDFLoader`
* **Old Way:** Manually reading binary streams and iterating pages.
* **New Way:** Automatically loads PDFs, handles errors, and extracts metadata (page numbers).

### 2. `RecursiveCharacterTextSplitter`
* **Old Way:** Fixed character slicing (often cutting words in half).
* **New Way:** Smarter splitting. It tries to split on paragraph breaks (`\n\n`) first, then newlines (`\n`), then spaces, ensuring text stays semantically whole.

### 3. `GoogleGenerativeAIEmbeddings`
* **Wrapper:** Connects directly to Gemini's `text-embedding-004` model without needing manual API calls.

### 4. `Chroma` (Vector Store)
* **Integration:** LangChain handles the `Upsert` logic automatically. `Chroma.from_documents()` is a powerful function that ingests, embeds, and saves data in one step.

### 5. `as_retriever()`
* **Abstraction:** Converts the database into a "Search Engine" interface. We simply ask it to `.invoke("query")`, and it handles the vector math.

## 🏃‍♂️ How to Run
```bash
python main.py

Ensure document.pdf is in the folder.

The script will load, chunk, embed, and answer your question using the defined API key. 