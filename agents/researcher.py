# agents/researcher.py

from groq import Groq
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY, MODEL, RESEARCHER_PROMPT

client = Groq(api_key=GROQ_API_KEY)

def research_topic(topic):
    """
    Takes a topic and returns structured research about it.
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


if __name__ == "__main__":
    topic = input("Enter a topic to research: ")
    result = research_topic(topic)
    print("\n" + result)