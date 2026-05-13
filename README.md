# 🎓 AI Study Assistant

A multi-agent AI system that helps you study any topic through research, 
teaching, and interactive quizzes.

## 🤖 How It Works

This project uses 3 specialized AI agents that work together:

You enter a topic
↓
🔍 Researcher Agent  →  Gathers structured information about the topic
↓
📚 Teacher Agent     →  Turns research into a clear lesson + quiz questions
↓
🎯 Quiz Master Agent →  Tests your knowledge and grades your answers
↓
💾 File Manager      →  Saves the full session to your history

---

## ✨ Features

- 🔍 **Auto Research** — Instantly get structured research on any topic
- 📚 **Personalized Lessons** — Research turned into beginner friendly lessons
- 🎯 **Interactive Quiz** — Test yourself and get instant AI grading
- 💾 **Study History** — Every session saved with timestamp for review
- 🔄 **Multi Agent Pipeline** — 3 agents working together seamlessly

---

## 🛠️ Tech Stack

- **Python** — Core programming language
- **Groq API** — Fast AI inference
- **LLaMA 3.3 70B** — The AI model powering all 3 agents

---

## 📁 Project Structure
study_assistant/
├── agents/
│   ├── researcher.py    ← Agent 1: Gathers research
│   ├── teacher.py       ← Agent 2: Creates lessons
│   └── quiz_master.py   ← Agent 3: Runs quizzes
├── utils/
│   └── file_manager.py  ← Saves study sessions
├── history/             ← Study sessions saved here
├── main.py              ← Entry point, connects all agents
├── config.py            ← API key and settings (not on GitHub)
└── requirements.txt     ← Project dependencies

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Janinduthenura/study_assistant.git
cd study_assistant
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a free Groq API key
- Go to [console.groq.com](https://console.groq.com)
- Sign up for free
- Create an API key

### 5. Create config.py
Create a file called `config.py` in the root folder:
```python
GROQ_API_KEY = "your_groq_api_key_here"
MODEL = "llama-3.3-70b-versatile"
```

### 6. Run the project
```bash
python main.py
```

---

## 🛠️ Built With
- Python
- Groq API
- LLaMA 3.3 70B

## 💡 Example Usage

🎓 Welcome to AI Study Assistant!
What would you like to do?

Study a new topic
View study history
Quit

Your choice: 1
What topic do you want to study? black holes
🔍 Researcher Agent is gathering information about 'black holes'...
📚 Teacher Agent is preparing your lesson...
🎯 Quiz Master is preparing your quiz...
Q1: What is the point of no return around a black hole called?
Your answer: event horizon
RESULT: CORRECT ✅
Final Score: 3/3 🎉
💾 Study session saved!

---

## 🗺️ What I Learned Building This

- Multi agent AI system design
- Prompt engineering and structured outputs
- Chaining agents so output of one becomes input of next
- File management and data persistence
- Git and GitHub for version control
- API integration with Groq

---

## 🔮 Future Improvements

- [ ] Add a web interface using Flask
- [ ] Support multiple quiz attempts per topic
- [ ] Add difficulty levels for quizzes
- [ ] Generate study flashcards
- [ ] Add topic recommendations based on history

---

## 👤 Author

**Janinduthenura**
- GitHub: [@Janinduthenura](https://github.com/Janinduthenura)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

