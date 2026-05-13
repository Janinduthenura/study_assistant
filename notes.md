# Personal Notes & Command Reference

## Virtual Environment Commands

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install libraries
pip install groq

# Install all dependencies from requirements.txt
pip install -r requirements.txt

---

## Git Commands

# Initialize git in a folder
git init

# Check what files are being tracked
git status

# Check commit history
git log --oneline

# See what's inside a commit
git show --stat HEAD

# Add all files
git add .

# Add a specific file
git add filename.py

# Commit with a message
git commit -m "your message here"

# Connect to GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/repo-name.git

# Push to GitHub
git push -u origin main

# Force push (use carefully!)
git push --force

# Remove a file from Git tracking (but keep it on your computer)
git rm --cached filename.py

# Reset last commit but keep the files
git reset --soft HEAD~1

# Remove a file from staging
git reset HEAD filename.py

---

## API Key Safety Rules

- NEVER put real API key in code
- ALWAYS add config.py to .gitignore
- If key is exposed → regenerate it immediately at console.groq.com
- Store key as environment variable:

# Windows
set GROQ_API_KEY=your_real_key_here

# Mac/Linux
export GROQ_API_KEY=your_real_key_here

---

## Project Structure

study_assistant/
├── agents/
│   ├── researcher.py      ← Agent 1
│   ├── teacher.py         ← Agent 2
│   └── quiz_master.py     ← Agent 3
├── utils/
│   └── file_manager.py    ← saves study history
├── history/               ← study sessions saved here
├── main.py                ← connects all agents
├── config.py              ← API key and settings (never push this!)
├── requirements.txt       ← list of libraries
├── README.md              ← GitHub description
└── NOTES.md               ← this file (personal notes)

---

## Errors & Fixes

### GitHub blocked push — API key exposed
- Regenerate API key immediately
- Make sure config.py is in .gitignore
- Run: git rm --cached config.py
- Run: git reset --soft HEAD~1
- Run: git add . then git commit and git push

### fatal: pathspec 'config.py' did not match any files
- Means config.py was never committed — you're safe!
- Just continue with git add . and push

### "nothing to commit, working tree clean" but push fails
- Run: git show --stat HEAD
- Check if secret file is inside the commit
- If not → just push directly: git push -u origin main

---

## Day 3 & 4 — New Concepts

### try / except (Error Handling)
try:
    # code that might fail
except Exception as e:
    print(f"Error: {e}")  # handle it gracefully

### datetime formatting
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

### Writing to a file
with open("filename.txt", "w", encoding="utf-8") as file:
    file.write(content)

### Reading files in a folder
import os
files = os.listdir("history")

### Moving prompts to config.py
- Keeps agents clean and focused
- Easy to update prompts in one place
- Import like: from config import RESEARCHER_PROMPT

### Badges in README
![Badge](https://img.shields.io/badge/Label-Message-color)
Colors: blue, green, orange, red, yellow