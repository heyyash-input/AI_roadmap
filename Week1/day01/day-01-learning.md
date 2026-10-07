# Day 01: Getting Started with LLMs, Python & APIs

## 📚 What I Learned

Today I built the foundation for working with LLM APIs using Python. I learned how to set up an isolated Python environment, make my first LLM API call, handle API keys securely, understand tokens, and safely push an AI project to GitHub.

---

## 1. Creating a Python Virtual Environment with `uv`

I learned how to use **uv** to create and manage a Python virtual environment.

A virtual environment keeps project dependencies isolated from the rest of the system.

### Create a Project

```bash
uv init
```

### Create a Virtual Environment

```bash
uv venv
```

### Activate the Environment on Windows

```powershell
.venv\Scripts\activate
```

### Install Packages

```bash
uv add groq
```

Using a virtual environment helps keep projects clean and prevents dependency conflicts.

---

## 2. Making My First LLM Call with the Groq API

I learned how to connect a Python application to an LLM using the **Groq API**.

Basic flow:

```text
Python Application
       ↓
Groq API
       ↓
LLM
       ↓
Response
       ↓
Python Application
```

Example:

```python
from groq import Groq

client = Groq()

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": "Explain what an API is."
        }
    ]
)

print(response.choices[0].message.content)
```

The important concept I learned is that my Python application sends messages to the model through an API and receives the generated response.

---

## 3. Understanding Message Roles

LLM applications commonly use three important message roles:

### System

Defines how the model should behave.

```text
You are a helpful Python tutor.
```

### User

Contains the user's actual request.

```text
Explain Python lists.
```

### Assistant

Contains the model's response.

```text
A Python list is an ordered, mutable collection...
```

The basic conversation structure is:

```text
System
  ↓
User
  ↓
Assistant
```

Understanding these roles is important when designing prompts and AI applications.

---

## 4. Understanding Tokens

I learned that LLMs process text using **tokens** rather than simply counting words.

For example:

```text
"Hello, how are you?"
```

is broken into smaller pieces called tokens.

Tokens can represent:

- Complete words
- Parts of words
- Punctuation
- Special characters

### Why Tokens Matter

Token usage affects:

- Context window
- API usage
- Cost
- Response length
- Application performance

The general flow is:

```text
Text
 ↓
Tokenization
 ↓
LLM processing
 ↓
Generated tokens
 ↓
Text response
```

Understanding tokens is important when building applications that process large amounts of text.

---

## 5. Safely Handling API Keys

I learned that API keys should **never be hardcoded** or committed to GitHub.

Instead, I used a `.env` file.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

Python can load environment variables using `python-dotenv`.

```bash
uv add python-dotenv
```

Example:

```python
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
```

### Important Rule

Never do this:

```python
api_key = "gsk_xxxxxxxxxxxxxxxxx"
```

API keys are secrets and should be treated like passwords.

---

## 6. Preventing API Keys from Being Pushed to GitHub

I learned how to use `.gitignore` to prevent sensitive files from being committed.

Example `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

The `.env` file stays on my local machine and is not pushed to GitHub.

Instead, I can provide an example configuration:

### `.env.example`

```env
GROQ_API_KEY=your_api_key_here
```

This allows other developers to understand which environment variables are required without exposing the actual secret.

---

## 7. Pushing the Project to GitHub Safely

Basic Git workflow:

```bash
git init
git add .
git commit -m "Day 01: Getting started with LLMs"
git branch -M main
git remote add origin <repository-url>
git push -u origin main
```

Before pushing, I learned to check:

```bash
git status
```

and verify that `.env` is not included.

### Safe Repository Structure

```text
project/
│
├── .env
├── .env.example
├── .gitignore
├── main.py
├── pyproject.toml
└── README.md
```

The important point is:

```text
.env          → NEVER PUSH
.env.example  → Safe to push
```

---

## 8. Breaking Things on Purpose

I also experimented with failure cases to understand how AI applications behave when something goes wrong.

### Failure Case 1: Invalid API Key

Using an incorrect API key causes authentication to fail.

```text
Invalid API Key
        ↓
Authentication Error
        ↓
API request fails
```

### Failure Case 2: Missing Environment Variable

If `GROQ_API_KEY` is missing:

```python
os.getenv("GROQ_API_KEY")
```

may return:

```text
None
```

The API client can then fail because no valid API key was provided.

### Failure Case 3: Invalid Model

If the requested model does not exist or is unavailable, the API request can fail.

This helped me understand that production applications need proper error handling rather than assuming every API request will succeed.

---

## 9. Failure Modes I Learned

AI applications can fail for many reasons:

```text
Invalid API Key
       ↓
Authentication failure

Invalid Model
       ↓
API request failure

Missing Environment Variable
       ↓
Configuration failure

Network/API Failure
       ↓
Request failure

Too Many Tokens
       ↓
Context/limit problem
```

Understanding failure modes is important for building reliable AI applications.

---

## 🧠 Key Takeaways

### Python Environment

```text
uv
 ↓
Virtual Environment
 ↓
Project Dependencies
```

### LLM API

```text
Python
 ↓
API
 ↓
LLM
 ↓
Response
```

### Message Roles

```text
System → Defines behavior
User → Provides request
Assistant → Generates response
```

### Security

```text
API Key
 ↓
.env
 ↓
.gitignore
 ↓
Never expose secrets
```

### GitHub

```text
Code → Git → GitHub
          ↑
       No secrets
```

---

## 🚀 Next Steps

- Learn more about prompt engineering.
- Experiment with system prompts.
- Understand temperature and model parameters.
- Build a reusable LLM client.
- Learn structured outputs.
- Start building a small AI agent.

---

## 🎯 Day 01 Summary

Today I learned the basic workflow required to start building LLM applications with Python.

I created a Python virtual environment using **uv**, made my first **Groq API** call, learned about **system, user, and assistant message roles**, explored **tokens**, securely handled API keys using `.env`, pushed code to **GitHub without exposing secrets**, and intentionally broke the application to understand common failure modes.

**Day 01 completed ✅**