# agents/researcher.py

from groq import Groq
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY, MODEL, RESEARCHER_PROMPT

client = Groq(api_key=GROQ_API_KEY)


def research_topic(topic):
    """
    Mode 1 — Research a topic using AI memory.
    """
    print(f"\n🔍 Researcher Agent is gathering information about '{topic}'...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": RESEARCHER_PROMPT},
            {"role": "user", "content": f"Research this topic for me: {topic}"}
        ]
    )

    return response.choices[0].message.content


def research_from_document(topic, index, chunks):
    """
    Mode 2 — Research a topic from uploaded document using RAG.
    """
    print(f"\n🔍 Researcher Agent is searching your document for '{topic}'...")

    from rag.retriever import retrieve_relevant_chunks, build_context

    # Find relevant chunks from the document
    relevant_chunks = retrieve_relevant_chunks(topic, index, chunks)

    if not relevant_chunks:
        return f"Could not find information about '{topic}' in the document."

    # Build context from relevant chunks
    context = build_context(relevant_chunks)

    # Ask AI to structure it like normal research
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": f"""{RESEARCHER_PROMPT}
                Important: Base your research ONLY on the provided document context.
                Do not add information from outside the document."""
            },
            {
                "role": "user",
                "content": f"""Using ONLY this document content:

{context}

Create structured research about: {topic}"""
            }
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    # Test Mode 1
    print("Testing Mode 1 - AI Research:")
    result = research_topic("black holes")
    print(result)