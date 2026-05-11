# main.py — connects all 3 agents together

from agents.researcher import research_topic
from agents.teacher import teach_topic
from agents.quiz_master import run_quiz

def main():
    print("="*40)
    print("🎓 Welcome to AI Study Assistant!")
    print("="*40)

    while True:
        print("\nWhat would you like to do?")
        print("1. Study a new topic")
        print("2. Quit")

        choice = input("\nYour choice (1 or 2): ")

        if choice == "2":
            print("\nGoodbye! Keep learning! 👋")
            break

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
            run_quiz(lesson)

            print("\nWould you like to study another topic?")

        else:
            print("Invalid choice. Please type 1 or 2.")


if __name__ == "__main__":
    main()