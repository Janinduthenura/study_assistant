# agents/teacher.py

from groq import Groq
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY, MODEL, TEACHER_PROMPT

client = Groq(api_key=GROQ_API_KEY)

def teach_topic(research):
    """
    Takes research from Researcher Agent and
    turns it into a clear lesson with quiz questions.
    """
    print(f"\n📚 Teacher Agent is preparing your lesson...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": TEACHER_PROMPT},
            {"role": "user", "content": f"Turn this research into a lesson:\n\n{research}"}
        ]
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    test_research = """
    TOPIC: Black Holes
    OVERVIEW: A black hole is a region in space where gravity is so strong
    that nothing, not even light, can escape from it.
    KEY CONCEPTS:
    1. Event Horizon: The point of no return
    2. Singularity: The infinitely dense center
    3. Hawking Radiation: Radiation black holes emit
    IMPORTANT FACTS:
    - Black holes can be millions of times more massive than the sun
    - Time slows down near a black hole
    FUN FACTS:
    - If the sun became a black hole it would be about 3km wide
    """
    result = teach_topic(test_research)
    print("\n" + result)