# agents/researcher.py

from groq import Groq
import sys
import os

# This lets us import from the parent folder (study_assistant/)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY, MODEL

# Create the Groq client
client = Groq(api_key=GROQ_API_KEY)

def research_topic(topic):
    """
    Takes a topic and returns structured research about it.
    """

    print(f"\n🔍 Researcher Agent is gathering information about '{topic}'...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """You are an expert researcher. 
                When given a topic, you provide well structured research in this exact format:

                TOPIC: [topic name]

                OVERVIEW:
                [2-3 sentence simple explanation of what it is]

                KEY CONCEPTS:
                1. [concept 1]: [simple explanation]
                2. [concept 2]: [simple explanation]
                3. [concept 3]: [simple explanation]

                IMPORTANT FACTS:
                - [fact 1]
                - [fact 2]
                - [fact 3]
                - [fact 4]
                - [fact 5]

                FUN FACTS:
                - [fun fact 1]
                - [fun fact 2]
                - [fun fact 3]

                Always use simple language that a beginner can understand.
                Always follow this exact format, nothing more nothing less."""
            },
            {
                "role": "user",
                "content": f"Research this topic for me: {topic}"
            }
        ]
    )

    # Extract the research text from the response
    research = response.choices[0].message.content
    return research


# This lets us test the agent directly by running this file
if __name__ == "__main__":
    topic = input("Enter a topic to research: ")
    result = research_topic(topic)
    print("\n" + result)
    