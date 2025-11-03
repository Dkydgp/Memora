# 🧠 Memora – The Chatbot That Remembers You

> **“Talk once, continue anytime — Memora remembers.”**

Memora is an **AI-powered chatbot** built with **Python**, **Chainlit**, and the **OpenRouter API**.  
Unlike ordinary chatbots, Memora can **remember your past chats** and **recall context** across sessions — offering a truly personalized conversation experience.

---
### 🧠 Code Quality (Pylint)

![Pylint Score](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Dkydgp/Memora/main/pylint_score.json?cacheBust=1)
![Workflow Status](https://github.com/Dkydgp/Memora/actions/workflows/pylint.yml/badge.svg)

## ✨ Features

✅ **Persistent Memory** – Stores chat history in a local `chat_memory.json` file  
✅ **Context-Aware Conversations** – Keeps track of user details and previous chats  
✅ **OpenRouter API Integration** – Uses GPT-based models for natural, intelligent replies  
✅ **Beautiful UI** – Powered by Chainlit for an interactive chat interface  
✅ **PEP 8 Compliant Code** – Clean, structured, and easy to customize  

---

## 🛠️ Tech Stack

| Component | Technology Used |
|------------|------------------|
| **Language** | Python |
| **Framework** | Chainlit |
| **AI API** | OpenRouter (GPT models) |
| **Environment Variables** | python-dotenv |
| **Memory Storage** | JSON (Local persistent memory) |

---

## ⚙️ Installation & Setup

### 1. Clone this Repository
```bash
git clone https://github.com/<your-username>/memora-chatbot.git
cd memora-chatbot
2. Create and Activate a Virtual Environment
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Add Your Environment Variables

Create a .env file in the root directory with:

OPENAI_API_KEY=your_openrouter_api_key


👉 (You can also create a .env.example file for others to follow.)

5. Run the Chatbot
chainlit run chatbot.py -w


Then open your browser at 👉 http://localhost:8000

💾 Memory System

Memora stores chat context in a local file called:

chat_memory.json


Each conversation is automatically saved and loaded when you restart the app, allowing continuous chat flow even after closing the session.

🧩 Folder Structure
📦 memora-chatbot
 ┣ 📜 chatbot.py
 ┣ 📜 requirements.txt
 ┣ 📜 .env.example
 ┣ 📜 chat_memory.json
 ┣ 📜 README.md
 ┗ 📁 assets/

🧠 Example Conversation

User: "Hey Memora, remember that I like tea more than coffee."
Memora: "Got it! I’ll remember that you prefer tea ☕"

User (next day): "What’s my favorite drink?"
Memora: "You told me yesterday that you like tea more than coffee!"

🌐 Future Enhancements

🔸 Database-based memory (SQLite/Firebase)

🔸 Voice input & output

🔸 Emotion detection

🔸 Multi-user session handling

🔸 Deployment to Render & n8n automation

🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open a pull request or suggest improvements.

🧾 License

This project is licensed under the MIT License – see the LICENSE
 file for details.

❤️ Author

Developed by: Dipak Kumar Yadav
Project Name: Memora – The Chatbot That Remembers You
Based on: Chainlit + OpenRouter API + Python

### Code quality (Pylint)
![Pylint Score](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Dkydgp/Memora/main/pylint_score.json)

### 🧠 Code Quality (Pylint)

![Pylint Score](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/Dkydgp/Memora/main/pylint_score.json)

---

