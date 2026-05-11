# agents/quiz_master.py

from groq import Groq
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY, MODEL

client = Groq(api_key=GROQ_API_KEY)

def extract_questions(lesson):
    """
    Takes the lesson from Teacher Agent and
    extracts just the 3 quiz questions.
    """

    print("\n🎯 Quiz Master is preparing your quiz...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """You are a quiz extractor.
                You will receive a lesson that contains quiz questions at the bottom.
                Your job is to extract ONLY the questions and return them in this exact format:

                Q1: [question]
                Q2: [question]
                Q3: [question]

                Return ONLY the 3 questions, nothing else."""
            },
            {
                "role": "user",
                "content": f"Extract the quiz questions from this lesson:\n\n{lesson}"
            }
        ]
    )

    questions_text = response.choices[0].message.content
    return questions_text


def grade_answer(question, user_answer):
    """
    Takes a question and the user's answer,
    asks Groq to grade it and give feedback.
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """You are a friendly quiz grader.
                You will receive a question and a student's answer.
                Grade it and respond in this exact format:

                RESULT: [CORRECT or INCORRECT]
                FEEDBACK: [1-2 sentences explaining why, and the correct answer if wrong]

                Be encouraging and friendly even when the answer is wrong."""
            },
            {
                "role": "user",
                "content": f"Question: {question}\nStudent's answer: {user_answer}"
            }
        ]
    )

    return response.choices[0].message.content


def run_quiz(lesson):
    """
    Runs the full quiz — extracts questions,
    asks them one by one, grades each answer,
    and gives a final score.
    """

    # Step 1 — Extract questions from the lesson
    questions_text = extract_questions(lesson)

    # Step 2 — Split into individual questions
    questions = []
    for line in questions_text.strip().split("\n"):
        if line.startswith("Q1:") or line.startswith("Q2:") or line.startswith("Q3:"):
            questions.append(line.strip())

    if len(questions) == 0:
        print("Could not extract questions. Please try again.")
        return

    print("\n" + "="*40)
    print("QUIZ TIME! Answer these questions:")
    print("="*40 + "\n")

    score = 0
    results = []

    # Step 3 — Ask each question and grade the answer
    for i, question in enumerate(questions):
        print(f"\n{question}")
        user_answer = input("Your answer: ")

        # Grade the answer
        feedback = grade_answer(question, user_answer)
        print("\n" + feedback)

        # Check if correct to update score
        if "RESULT: CORRECT" in feedback:
            score += 1

        results.append({
            "question": question,
            "answer": user_answer,
            "feedback": feedback
        })

    # Step 4 — Show final score
    print("\n" + "="*40)
    print(f"QUIZ COMPLETE! Your score: {score}/{len(questions)}")

    if score == 3:
        print("🎉 Perfect score! You're a master!")
    elif score == 2:
        print("👍 Great job! Almost there!")
    elif score == 1:
        print("📚 Good try! Review the lesson and try again!")
    else:
        print("💪 Keep studying! You'll get it next time!")

    print("="*40)

    return results


# Test it directly
if __name__ == "__main__":
    test_lesson = """
    LESSON: Black Holes
    ================================
    Black holes are fascinating objects in space.

    WHAT YOU NEED TO KNOW:
    1. Event Horizon: The point of no return
    2. Singularity: The infinitely dense center
    3. Hawking Radiation: Radiation black holes emit

    DID YOU KNOW?
    - Time slows down near a black hole
    - The first image was captured in 2019

    SUMMARY:
    Black holes are regions where gravity is so strong nothing can escape.

    ================================
    QUIZ TIME! Let's test what you learned:

    Q1: What is the point of no return around a black hole called?
    Q2: Who predicted that black holes emit radiation?
    Q3: In what year was the first image of a black hole captured?
    """

    run_quiz(test_lesson)
    