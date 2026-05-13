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

            # Make sure user didn't just press Enter
            if topic.strip() == "":
                print("Please enter a valid topic!")
                continue

            try:
                # ---- AGENT 1 — Researcher ----
                research = research_topic(topic)
                print("\n" + research)

            except Exception as e:
                print(f"\n❌ Researcher Agent failed: {e}")
                print("Please check your API key and internet connection.")
                continue

            input("\nPress Enter to continue to your lesson...")

            try:
                # ---- AGENT 2 — Teacher ----
                lesson = teach_topic(research)
                print("\n" + lesson)

            except Exception as e:
                print(f"\n❌ Teacher Agent failed: {e}")
                print("Please try again.")
                continue

            input("\nPress Enter to start the quiz...")

            try:
                # ---- AGENT 3 — Quiz Master ----
                quiz_results = run_quiz(lesson)

            except Exception as e:
                print(f"\n❌ Quiz Master Agent failed: {e}")
                quiz_results = []

            # Calculate score
            score = 0
            if quiz_results:
                for result in quiz_results:
                    if "RESULT: CORRECT" in result["feedback"]:
                        score += 1

            # ---- SAVE SESSION ----
            try:
                save_study_session(topic, research, lesson, quiz_results, score)
            except Exception as e:
                print(f"\n❌ Could not save session: {e}")

        else:
            print("Invalid choice. Please type 1, 2 or 3.")


if __name__ == "__main__":
    main()