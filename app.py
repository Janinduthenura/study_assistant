# app.py

from flask import Flask, render_template, request, session
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.researcher import research_topic, research_from_document
from agents.teacher import teach_topic
from agents.quiz_master import extract_questions, grade_answer
from utils.file_manager import save_study_session, load_study_history
from rag.embeddings import process_document, load_index

app = Flask(__name__)
app.secret_key = "study_assistant_secret_key"

# Make sure upload folder exists
os.makedirs("uploads", exist_ok=True)


# ---- ROUTES ----

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/study", methods=["POST"])
def study():
    # Which mode did the user choose?
    mode = request.form.get("mode")

    # ---- MODE 1 — Learn from AI ----
    if mode == "ai":
        topic = request.form.get("topic", "").strip()

        if topic == "":
            return render_template("index.html",
                error="Please enter a topic!")

        try:
            research = research_topic(topic)
            session["topic"] = topic
            session["research"] = research
            session["mode"] = "ai"

        except Exception as e:
            return render_template("index.html",
                error=f"Researcher Agent failed: {e}")

    # ---- MODE 2 — Learn from document ----
    elif mode == "document":
        # Check if file was uploaded
        if "document" not in request.files:
            return render_template("index.html",
                error="Please upload a file!")

        file = request.files["document"]

        if file.filename == "":
            return render_template("index.html",
                error="Please select a file!")

        # Check file type
        allowed = [".pdf", ".txt", ".md"]
        ext = os.path.splitext(file.filename)[1].lower()

        if ext not in allowed:
            return render_template("index.html",
                error="Only PDF, TXT and MD files are supported!")

        # Get the topic
        topic = request.form.get("doc_topic", "").strip()
        if topic == "":
            return render_template("index.html",
                error="Please enter what to study from the document!")

        try:
            # Save the uploaded file
            file_path = os.path.join("uploads", file.filename)
            file.save(file_path)

            # Process the document through RAG pipeline
            index, chunks = process_document(file_path)

            # Research from document
            research = research_from_document(topic, index, chunks)

            session["topic"] = topic
            session["research"] = research
            session["mode"] = "document"
            session["filename"] = file.filename

        except Exception as e:
            return render_template("index.html",
                error=f"Document processing failed: {e}")

    # ---- BOTH MODES continue the same way ----
    try:
        lesson = teach_topic(research)
        questions_text = extract_questions(lesson)

        questions = []
        for line in questions_text.strip().split("\n"):
            if line.startswith("Q1:") or line.startswith("Q2:") or line.startswith("Q3:"):
                questions.append(line.strip())

        session["lesson"] = lesson
        session["questions"] = questions

        return render_template(
            "result.html",
            topic=topic,
            research=research,
            lesson=lesson,
            questions=questions,
            mode=mode
        )

    except Exception as e:
        return render_template("index.html",
            error=f"Something went wrong: {e}")


@app.route("/quiz", methods=["POST"])
def quiz():
    questions = session.get("questions", [])
    topic = session.get("topic", "")
    research = session.get("research", "")
    lesson = session.get("lesson", "")
    mode = session.get("mode", "ai")

    score = 0
    results = []

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
        total=len(questions),
        mode=mode
    )


@app.route("/history")
def history():
    files = load_study_history()
    return render_template("index.html", history=files)


if __name__ == "__main__":
    app.run(debug=True)