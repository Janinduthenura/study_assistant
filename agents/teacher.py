# agents/teacher.py

from groq import Groq
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY, MODEL

client = Groq(api_key=GROQ_API_KEY)

def teach_topic(research):
    """
    Takes the research from the Researcher Agent
    and turns it into a clear lesson with quiz questions.
    """

    print(f"\n📚 Teacher Agent is preparing your lesson...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """You are a friendly and engaging teacher.
                You will receive research about a topic.
                Your job is to turn it into a clear lesson in this exact format:

                LESSON: [topic name]
                ================================

                [Write a friendly 3-4 sentence introduction to the topic]

                WHAT YOU NEED TO KNOW:
                1. [key point 1 — explain simply in 1-2 sentences]
                2. [key point 2 — explain simply in 1-2 sentences]
                3. [key point 3 — explain simply in 1-2 sentences]

                DID YOU KNOW?
                - [interesting fact 1]
                - [interesting fact 2]

                SUMMARY:
                [2-3 sentence summary of everything]

                ================================
                QUIZ TIME! Let's test what you learned:

                Q1: [question about a key concept]
                Q2: [question about an important fact]
                Q3: [question about something interesting]

                Always use simple, friendly language.
                Always follow this exact format."""
            },
            {
                "role": "user",
                "content": f"Turn this research into a lesson:\n\n{research}"
            }
        ]
    )

    lesson = response.choices[0].message.content
    return lesson


if __name__ == "__main__":
    # For testing — we'll feed it some fake research
    test_research = """
    TOPIC: Black Holes

    OVERVIEW:
    A black hole is a region in space where gravity is so strong
    that nothing, not even light, can escape from it.
    They form when massive stars collapse at the end of their lives.

    KEY CONCEPTS:
    1. Event Horizon: The point of no return around a black hole
    2. Singularity: The infinitely dense center of a black hole
    3. Hawking Radiation: Radiation that black holes slowly emit over time

    IMPORTANT FACTS:
    - Black holes can be millions of times more massive than the sun
    - Time slows down near a black hole
    - The first image of a black hole was captured in 2019

    FUN FACTS:
    - If the sun became a black hole it would be about 3km wide
    - Black holes are not actually holes, they are objects
    """

    result = teach_topic(test_research)
    print("\n" + result)