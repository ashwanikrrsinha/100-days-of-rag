# Day 4: The Vector Store (Semantic Search Engine)

## 🧠 The Concept: Semantic Search vs. Keyword Search
On **Day 4**, we moved beyond simple text matching.

* **Old Way (Keyword Search / Ctrl+F):**
    If you search for *"How to buy items"*, a keyword search looks for the exact letters `b-u-y`. If the document says *"Purchase goods"*, it returns **0 results** because the letters don't match.

* **New Way (Semantic Search):**
    We convert the query into a **Vector**.
    * Vector("Buy items") might point **North**. ⬆️
    * Vector("Purchase goods") also points **North**. ⬆️
    * **Result:** The AI knows they are the same thing because their vectors point in the same direction.

## 🧮 The Math: Cosine Similarity
To teach a computer to compare "meanings," we use a formula from high school geometry called **Cosine Similarity**.

It measures the **angle** between two vectors (arrows).

$$\text{Similarity} = \frac{A \cdot B}{\|A\| \times \|B\|}$$

### Breakdown of the Formula:
1.  **The Dot Product ($A \cdot B$):** We multiply the matching numbers in both lists and add them up. If high numbers align with high numbers, this value is huge.
2.  **The Magnitude ($\|A\| \times \|B\|$):** We calculate how "long" each arrow is. We divide by this to normalize the result.
3.  **The Result (Score):**
    * **1.0:** Perfect Match (The arrows point the exact same way).
    * **0.0:** No Relation (The arrows are 90° apart).
    * **-1.0:** Opposites (The arrows point in opposite directions).

## 🏗️ Architecture: The "In-Memory" Store
For this project, we built a **Vector Store** from scratch using a simple Python List.

**The Data Structure:**
We stored every document as a dictionary containing two things:
1.  **Payload:** The actual text (for humans to read).
2.  **Vector:** The 768 numbers (for the machine to search).

```python
vector_store = [
    {
        "text": "Mars currency is Red-Credits",
        "vector": [0.1, -0.5, 0.9, ...]
    },
    {
        "text": "Apples grow on trees",
        "vector": [0.8, 0.1, -0.2, ...]
    }
]

🚀 The Search Algorithm (Step-by-Step)
When the user asks: "How do I buy things?"

Embed: Convert the question into a Query Vector.

Scan: Loop through every item in our vector_store.

Compare: Calculate the Cosine Similarity between the Query Vector and the Document Vector.

Rank: Sort the results from Highest Score to Lowest Score.

Retrieve: Return the text with the score closest to 1.0.

--------------------------------------------------------------------------------------------------------

--- USER QUERY: 'How do I buy things on Mars?' ---

--- SEARCH RESULTS ---
Score: 0.7019 | Text: Mars has a currency called Red-Credits.
Score: 0.5418 | Text: You need an Aero-2000 suit to breathe on Mars.
Score: 0.2744 | Text: Apples are a fruit that grow on trees.

WINNER: 'Mars has a currency called Red-Credits.'