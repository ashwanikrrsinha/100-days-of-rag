# Day 3: Embeddings Generator (The "Soul" of Data)

## 🧠 The Concept: What are Embeddings?
On Days 1 and 2, we treated text as simple strings (letters).
On **Day 3**, we learned to treat text as **Vectors** (mathematics).

An **Embedding** is a translation of human language into a list of floating-point numbers.
* **Input:** "The quick brown fox"
* **Output:** `[0.012, -0.931, 0.442, ...]` (Total 768 numbers)

### Why do we need this? (The "500-Page Book" Problem)
If you want to perform RAG on a massive PDF (e.g., a 500-page manual), you cannot paste the entire book into the prompt. It's too big and too expensive.

**The Solution:**
1.  We convert every paragraph of the book into a list of numbers (Embedding).
2.  We convert the User's Question into a list of numbers.
3.  We use math to find which paragraph is "closest" to the question.

## 🗺️ Visualizing Vector Space
Imagine a 3D map where words with similar **meanings** are placed close together.



* **"King"** and **"Queen"** are close (Royal connection).
* **"Apple"** and **"iPhone"** are close (Tech connection).
* **"Apple"** and **"Dog"** are far apart.

This allows the AI to understand that a search for "Canine" should find results for "Dog", even if the letters D-o-g aren't in the query.

## 💻 The Code Logic
We used the `text-embedding-004` model from Google Gemini.

1.  **Setup:** Configure the API with `.env` security.
2.  **Transformation:** Send text to `genai.embed_content`.
3.  **Dimensionality:** We discovered that Gemini always outputs **768 dimensions**. This means every thought, no matter how complex, is reduced to 768 specific numbers.

## 🏃‍♂️ How to Run
```bash
# Make sure you are in the Day_03 folder
python main.py

Converting text: 'The quick brown fox jumps over the lazy dog.'...

--- RESULTS ---
Vector Dimensions: 768
Sample Coordinates: [0.0412, -0.0123, ...]