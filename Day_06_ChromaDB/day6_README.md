# Day 6: ChromaDB (The Persistent Vector Database)

## 🎯 The Goal
To replace our temporary Python lists with a professional **Vector Database** (ChromaDB). This allows our application to save embeddings to the hard drive, so we don't have to re-process PDFs every time we run the app.

## 🧠 Core Concept: Persistence & Efficiency
* **Ephemeral (RAM):** Python Lists. Fast, but data is lost when the script stops. Good for testing.
* **Persistent (Disk):** ChromaDB. Data is saved to a local folder (`./chroma_db`). Good for production.

### Why ChromaDB?
It is an open-source, AI-native database designed specifically for vectors. It handles:
1.  **Storage:** Saving millions of vectors efficiently.
2.  **Indexing:** Using algorithms like HNSW (Hierarchical Navigable Small World) to search huge datasets in milliseconds.
3.  **Querying:** Automatically calculating Cosine Similarity for us.

## 🛠️ The Code Logic
1.  **Initialization:** `chromadb.PersistentClient(path="./chroma_db")` creates the database folder.
2.  **Upsert:** We added documents *only if* the database was empty.
3.  **Query:** We asked "Tell me about food in France". Chroma handled the math and returned the closest matches.

## 🏃‍♂️ How to Run
```bash
python main.py

----
Run 1: You will see "Adding data..." as it embeds the text.

Run 2: You will see "Data already exists..." proving persistence works.