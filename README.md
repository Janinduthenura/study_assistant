# 🎓 AI Study Assistant

A multi-agent AI system that helps you study any topic through research, 
teaching, and interactive quizzes.

## 🤖 How It Works

This project uses 3 specialized AI agents that work together:

- **Researcher Agent** — Gathers and organizes information about any topic
- **Teacher Agent** — Turns research into a clear, simple lesson
- **Quiz Master Agent** — Tests your knowledge with questions and feedback

## 🚀 Getting Started

### 1. Clone the repository
git clone https://github.com/Janinduthenura/study_assistant.git
cd study_assistant

### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies
pip install -r requirements.txt

### 4. Add your API key
Create a config.py file:
GROQ_API_KEY = "your_groq_api_key_here"
MODEL = "llama-3.3-70b-versatile"

### 5. Run the project
python main.py

## 🛠️ Built With
- Python
- Groq API
- LLaMA 3.3 70B

## 📁 Project Structure
study_assistant/
├── agents/
│   ├── researcher.py    
│   ├── teacher.py        
│   └── quiz_master.py    
├── utils/
│   └── file_manager.py   
├── main.py               
├── config.py             
└── requirements.txt      

## 👤 Author
Janinduthenura