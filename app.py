# app.py — Flask web application

from flask import Flask, render_template, request, session
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.researcher import research_topic
from agents.teacher import teach_topic
from agents.quiz_master import extract_questions, grade_answer
from utils.file_manager import save_study_session, show_history, load_study_history

# Create the Flask app
app = Flask(__name__)

# Secret key for session (stores data between pages)
app.secret_key = "study_assistant_secret_key"


# ---- ROUTES ----

# Route 1 — Home page
@app.route("/")
def home():
    return render_template("index.html")


# Route 2 — Study a topic
@app.route("/study", methods=["POST"])
def study():
    # Get the topic from the form
    topic = request.form.get("topic", "").strip()

    if topic == "":
        return render_template("index.html", error="Please enter a topic!")

    try:
        # Run all 3 agents
        research = research_topic(topic)
        lesson = teach_topic(research)
        questions_text = extract_questions(lesson)

        # Extract questions into a list
        questions = []
        for line in questions_text.strip().split("\n"):
            if line.startswith("Q1:") or line.startswith("Q2:") or line.startswith("Q3:"):
                questions.append(line.strip())

        # Save everything in session so we can use it later
        session["topic"] = topic
        session["research"] = research
        session["lesson"] = lesson
        session["questions"] = questions

        return render_template(
            "result.html",
            topic=topic,
            research=research,
            lesson=lesson,
            questions=questions
        )

    except Exception as e:
        return render_template("index.html", error=f"Something went wrong: {e}")


# Route 3 — Submit quiz answers
@app.route("/quiz", methods=["POST"])
def quiz():
    # Get questions from session
    questions = session.get("questions", [])
    topic = session.get("topic", "")
    research = session.get("research", "")
    lesson = session.get("lesson", "")

    score = 0
    results = []

    # Grade each answer
    for i, question in enumerate(questions):
        answer = request.form.get(f"answer_{i}", "").strip()
        feedback = grade_answer(question, answer)

        if "RESULT: CORRECT" in feedback:
            score += 1

        results.append({
            "question": question,
            "answer": answer,
            "feedback": feedback
        })

    # Save the session
    try:
        save_study_session(topic, research, lesson, results, score)
    except Exception as e:
        print(f"Could not save session: {e}")

    return render_template(
        "result.html",
        topic=topic,
        research=research,
        lesson=lesson,
        questions=questions,
        results=results,
        score=score,
        total=len(questions)
    )


# Route 4 — Study history
@app.route("/history")
def history():
    files = load_study_history()
    return render_template("index.html", history=files)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)