# agents/quiz_master.py

from groq import Groq
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import GROQ_API_KEY, MODEL, QUIZ_EXTRACTOR_PROMPT, QUIZ_GRADER_PROMPT

client = Groq(api_key=GROQ_API_KEY)

def extract_questions(lesson):
    """
    Extracts the 3 quiz questions from the lesson.
    """
    print("\n🎯 Quiz Master is preparing your quiz...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": QUIZ_EXTRACTOR_PROMPT},
            {"role": "user", "content": f"Extract the quiz questions from this lesson:\n\n{lesson}"}
        ]
    )

    return response.choices[0].message.content


def grade_answer(question, user_answer):
    """
    Grades the user's answer and gives feedback.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": QUIZ_GRADER_PROMPT},
            {"role": "user", "content": f"Question: {question}\nStudent's answer: {user_answer}"}
        ]
    )

    return response.choices[0].message.content


def run_quiz(lesson):
    """
    Runs the full quiz — extract, ask, grade, score.
    """
    questions_text = extract_questions(lesson)

    questions = []
    for line in questions_text.strip().split("\n"):
        if line.startswith("Q1:") or line.startswith("Q2:") or line.startswith("Q3:"):
            questions.append(line.strip())

    if len(questions) == 0:
        print("Could not extract questions. Please try again.")
        return []

    print("\n" + "="*40)
    print("QUIZ TIME! Answer these questions:")
    print("="*40 + "\n")

    score = 0
    results = []

    for i, question in enumerate(questions):
        print(f"\n{question}")
        user_answer = input("Your answer: ")

        feedback = grade_answer(question, user_answer)
        print("\n" + feedback)

        if "RESULT: CORRECT" in feedback:
            score += 1

        results.append({
            "question": question,
            "answer": user_answer,
            "feedback": feedback
        })

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


if __name__ == "__main__":
    test_lesson = """
    LESSON: Black Holes
    ================================
    QUIZ TIME!
    Q1: What is the point of no return around a black hole called?
    Q2: Who predicted that black holes emit radiation?
    Q3: In what year was the first image of a black hole captured?
    """
    run_quiz(test_lesson)