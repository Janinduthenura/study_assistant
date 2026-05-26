# rag/retriever.py

import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.embeddings import load_index, model


def retrieve_relevant_chunks(question, index, chunks, top_k=3):
    """
    Takes a question and finds the most relevant
    chunks from the indexed document.

    top_k = how many chunks to return
    """

    print(f"\n🔍 Searching for relevant chunks...")
    print(f"   Question: {question}")

    # Step 1 — Convert the question to 384 numbers
    question_embedding = model.encode([question])

    # Step 2 — Search the FAISS index
    # D = distances (how far each chunk is)
    # I = indices (which chunks were found)
    distances, indices = index.search(
        question_embedding.astype(np.float32),
        top_k
    )

    # Step 3 — Get the actual text of relevant chunks
    relevant_chunks = []
    for i, idx in enumerate(indices[0]):
        if idx != -1:  # -1 means no result found
            relevant_chunks.append({
                "chunk": chunks[idx],
                "distance": distances[0][i],
                "index": idx
            })
            print(f"   ✅ Found chunk {idx} (distance: {distances[0][i]:.4f})")

    return relevant_chunks


def build_context(relevant_chunks):
    """
    Combines relevant chunks into a single
    context string to send to the AI.
    """

    context = "Here is the relevant information from the document:\n\n"

    for i, item in enumerate(relevant_chunks):
        context += f"--- Section {i+1} ---\n"
        context += item["chunk"]
        context += "\n\n"

    return context


def answer_question(question, index, chunks):
    """
    Full RAG pipeline:
    1. Find relevant chunks
    2. Build context
    3. Send to AI with the context
    """
    from groq import Groq
    from config import GROQ_API_KEY, MODEL

    client = Groq(api_key=GROQ_API_KEY)

    # Step 1 — Find relevant chunks
    relevant_chunks = retrieve_relevant_chunks(question, index, chunks)

    if not relevant_chunks:
        return "I couldn't find relevant information in the document."

    # Step 2 — Build context from chunks
    context = build_context(relevant_chunks)

    # Step 3 — Send to AI with context
    print(f"\n🤖 Sending context to AI...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """You are a helpful study assistant.
                Answer questions based ONLY on the provided document context.
                If the answer is not in the context, say
                'I could not find that information in the document.'
                Always be clear and concise."""
            },
            {
                "role": "user",
                "content": f"{context}\n\nQuestion: {question}"
            }
        ]
    )

    return response.choices[0].message.content


# Test it directly
if __name__ == "__main__":
    from rag.embeddings import load_index

    # Load the saved index
    index, chunks = load_index("uploads/index")

    if index is None:
        print("No index found! Run embeddings.py first.")
    else:
        print("✅ Index loaded successfully!")

        # Test questions
        questions = [
            "What is photosynthesis?",
            "What are the two stages of photosynthesis?",
            "What does chlorophyll do?"
        ]

        for question in questions:
            print("\n" + "="*50)
            answer = answer_question(question, index, chunks)
            print(f"\nQ: {question}")
            print(f"A: {answer}")