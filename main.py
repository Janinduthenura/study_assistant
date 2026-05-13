# main.py

from agents.researcher import research_topic
from agents.teacher import teach_topic
from agents.quiz_master import run_quiz
from utils.file_manager import save_study_session, show_history

def main():
    print("="*40)
    print("🎓 Welcome to AI Study Assistant!")
    print("="*40)

    while True:
        print("\nWhat would you like to do?")
        print("1. Study a new topic")
        print("2. View study history")
        print("3. Quit")

        choice = input("\nYour choice (1, 2 or 3): ")

        if choice == "3":
            print("\nGoodbye! Keep learning! 👋")
            break

        elif choice == "2":
            show_history()

        elif choice == "1":
            topic = input("\nWhat topic do you want to study? ")

            # ---- AGENT 1 — Researcher ----
            research = research_topic(topic)
            print("\n" + research)

            input("\nPress Enter to continue to your lesson...")

            # ---- AGENT 2 — Teacher ----
            lesson = teach_topic(research)
            print("\n" + lesson)

            input("\nPress Enter to start the quiz...")

            # ---- AGENT 3 — Quiz Master ----
            quiz_results = run_quiz(lesson)

            # Calculate score from results
            score = 0
            if quiz_results:
                for result in quiz_results:
                    if "RESULT: CORRECT" in result["feedback"]:
                        score += 1

            # ---- SAVE SESSION ----
            save_study_session(topic, research, lesson, quiz_results, score)

        else:
            print("Invalid choice. Please type 1, 2 or 3.")


if __name__ == "__main__":
    main()