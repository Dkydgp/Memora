"""
chatbot.py
-----------
Chainlit + OpenRouter Chatbot with Self-Learning and Persistent Memory (TinyDB)
-------------------------------------------------------------
Features:
✅ Uses OpenRouter API
✅ Stores and recalls past chats (persistent TinyDB memory)
✅ Learns automatically using self_train.py
✅ Context-aware responses using last 5 messages
✅ Error-safe and PEP 8 compliant
"""

import os
import traceback
from dotenv import load_dotenv
import chainlit as cl
from openai import OpenAI
from self_train import run_self_training, recall_from_knowledge
from tinydb import TinyDB, Query

# ------------------------------
# Database (TinyDB for persistent memory)
# ------------------------------
db = TinyDB('chat_memory_db.json')
Chat = Query()


def save_chat_to_db(user_msg, bot_msg):
    """Save a user–assistant chat pair to TinyDB."""
    db.insert({'user': user_msg, 'assistant': bot_msg})


def load_chats_from_db(limit=10):
    """Load recent chat messages from TinyDB."""
    chats = db.all()
    return chats[-limit:] if chats else []


# ------------------------------
# Environment Setup
# ------------------------------
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)


# ------------------------------
# Chainlit Chatbot Events
# ------------------------------
@cl.on_chat_start
async def start_chat():
    await cl.Message(
        content="👋 Hi there! I'm your personal AI assistant. I can remember, learn, and chat naturally.\nHow can I help you today?"
    ).send()


@cl.on_message
async def handle_message(message: cl.Message):
    user_msg = message.content.strip()
    if not user_msg:
        await cl.Message(content="⚠️ Please type something to continue.").send()
        return

    # Load memory from TinyDB
    memory = load_chats_from_db(limit=5)

    # Recall related knowledge from self-learning module
    related_info = recall_from_knowledge(user_msg)
    related_text = "\n".join(related_info) if related_info else "None"

    # Prepare conversation context
    context_history = "\n".join(
        [f"User: {c.get('user', '')}\nAssistant: {c.get('assistant', '')}" for c in memory]
    )

    # Build full context-aware prompt
    full_prompt = (
        f"The following is the previous conversation:\n{context_history}\n\n"
        f"User now says: {user_msg}\n\n"
        f"Use this additional learned knowledge if helpful:\n{related_text}\n\n"
        f"Reply clearly and naturally."
    )

    try:
        # Generate response using OpenRouter model
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful, context-aware personal assistant chatbot "
                        "that remembers previous chats and uses knowledge base effectively."
                    ),
                },
                {"role": "user", "content": full_prompt},
            ],
        )

        bot_msg = response.choices[0].message.content.strip()

        # Send reply to user
        await cl.Message(content=bot_msg).send()

        # Save new chat pair to TinyDB
        save_chat_to_db(user_msg, bot_msg)

        # Automatically trigger self-training every 5 chats
        all_chats = db.all()
        if len(all_chats) % 5 == 0:
            run_self_training()

    except Exception as e:
        error_msg = f"❌ Error: {e}\n{traceback.format_exc()}"
        print(error_msg)
        await cl.Message(
            content="⚠️ Sorry, something went wrong while processing your request."
        ).send()


# ------------------------------
# Run Command
# ------------------------------
# Launch this chatbot using:
#   chainlit run chatbot.py --host 0.0.0.0 --port 10000
#
# (For Render deployment)