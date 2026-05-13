# utils/file_manager.py

import os
import json
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def save_study_session(topic, research, lesson, quiz_results, score):
    """
    Saves a complete study session to the history folder.
    """

    # Create a timestamp like 2026-05-09_10-30
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

    # Clean the topic name for use as filename
    # Example: "black holes" → "black_holes"
    clean_topic = topic.lower().replace(" ", "_")

    # Build the filename
    filename = f"{clean_topic}_{timestamp}.txt"

    # Make sure history folder exists
    os.makedirs("history", exist_ok=True)

    # Full path to the file
    filepath = os.path.join("history", filename)

    # Build the content to save
    content = f"""
=====================================
📚 STUDY SESSION
=====================================
Topic: {topic}
Date: {datetime.now().strftime("%B %d, %Y at %I:%M %p")}
Score: {score}/3
=====================================

--- RESEARCH ---
{research}

--- LESSON ---
{lesson}

--- QUIZ RESULTS ---
"""

    # Add each question and answer
    if quiz_results:
        for i, result in enumerate(quiz_results):
            content += f"""
Question {i+1}: {result['question']}
Your Answer: {result['answer']}
{result['feedback']}
---
"""

    content += f"""
=====================================
Final Score: {score}/3
=====================================
"""

    # Write everything to the file
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(content)

    print(f"\n💾 Study session saved to: history/{filename}")
    return filepath


def load_study_history():
    """
    Returns a list of all past study sessions.
    """

    # If history folder doesn't exist yet
    if not os.path.exists("history"):
        return []

    # Get all .txt files in history folder
    files = [f for f in os.listdir("history") if f.endswith(".txt")]

    if len(files) == 0:
        return []

    return files


def show_history():
    """
    Prints all past study sessions nicely.
    """

    files = load_study_history()

    if len(files) == 0:
        print("\n📂 No study history yet!")
        return

    print("\n📂 Your Study History:")
    print("="*40)

    for i, filename in enumerate(files):
        # Clean up filename for display
        # "black_holes_2026-05-09_10-30.txt" → "black holes | 2026-05-09 10:30"
        name = filename.replace(".txt", "")
        parts = name.split("_")
        print(f"{i+1}. {' '.join(parts)}")

    print("="*40)