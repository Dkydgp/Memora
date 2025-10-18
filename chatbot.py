"""
chatbot.py
-----------
Chainlit + OpenRouter Chatbot with Self-Learning and Persistent Memory
-------------------------------------------------------------
Features:
✅ Uses OpenRouter API
✅ Stores and recalls past chats (persistent memory)
✅ Learns automatically using self_train.py
✅ Context-aware responses using last 5 messages
✅ Error-safe and PEP 8 compliant
"""

import os
import json
import traceback
from dotenv import load_dotenv
import chainlit as cl
from openai import OpenAI
from self_train import run_self_training, recall_from_knowledge
from tinydb import TinyDB, Query

# Initialize database (TinyDB stores data as a JSON file)
db = TinyDB('chat_memory_db.json')
Chat = Query()

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

CHAT_MEMORY_FILE = "chat_memory.json"


# ------------------------------
# Utility Functions
# ------------------------------
def load_chat_memory():
    """Load previous chat history from JSON file."""
    if not os.path.exists(CHAT_MEMORY_FILE):
        return []
    try:
        with open(CHAT_MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Error reading chat memory. Resetting file.")
        return []


def save_chat_to_memory(user_msg, bot_msg):
    """Save a user–assistant chat pair to chat_memory.json."""
    data = load_chat_memory()
    data.append({"user": user_msg, "assistant": bot_msg})
    with open(CHAT_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


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

    # Load full memory for context
    memory = load_chat_memory()

    # Recall related knowledge from long-term memory
    related_info = recall_from_knowledge(user_msg)
    related_text = "\n".join(related_info) if related_info else "None"

    # Keep last 5 messages as conversation context
    last_chats = memory[-5:] if len(memory) >= 5 else memory
    context_history = "\n".join(
        [f"User: {c['user']}\nAssistant: {c['assistant']}" for c in last_chats]
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

        # Send reply
        await cl.Message(content=bot_msg).send()

        # Save new chat pair to memory
        save_chat_to_memory(user_msg, bot_msg)

        # Automatically train every 5 chats
        if len(memory) % 5 == 0:
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
#   chainlit run chatbot.py -w
#
# Your chatbot will open in the browser automatically.
