"""
self_train.py
-------------
Handles local self-learning for your chatbot.
Extracts key patterns and stores them in a simple knowledge index.
"""

import json
import re
from collections import defaultdict
from pathlib import Path


# -----------------------------
# File Paths
# -----------------------------
CHAT_MEMORY_FILE = Path("chat_memory.json")
KNOWLEDGE_INDEX_FILE = Path("knowledge_index.json")


# -----------------------------
# Step 1: Load and Clean Chat Data
# -----------------------------
def clean_chat_data():
    """Load chats from chat_memory.json and clean unnecessary data."""
    if not CHAT_MEMORY_FILE.exists():
        print("⚠️ No chat memory found yet.")
        return []

    with open(CHAT_MEMORY_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("❌ Error reading chat_memory.json — invalid JSON.")
            return []

    cleaned_data = []
    for chat in data:
        user = chat.get("user", "").strip()
        bot = chat.get("assistant", "").strip()
        if user and bot:
            cleaned_data.append({"user": user, "assistant": bot})

    return cleaned_data


# -----------------------------
# Step 2: Extract Patterns
# -----------------------------
def extract_patterns(cleaned_data):
    """Extract frequent user queries and bot responses."""
    patterns = defaultdict(list)
    for chat in cleaned_data:
        user_text = re.sub(r"[^a-zA-Z0-9\s]", "", chat["user"]).lower()
        words = user_text.split()

        # Basic keyword extraction
        for word in words:
            if len(word) > 3:  # ignore short words like 'a', 'is', 'to'
                patterns[word].append(chat["assistant"])

    # Summarize: keep only most common responses
    summarized_patterns = {}
    for word, responses in patterns.items():
        unique_responses = list(set(responses))
        summarized_patterns[word] = unique_responses[:3]  # limit memory

    return summarized_patterns


# -----------------------------
# Step 3: Update Knowledge Index
# -----------------------------
def update_knowledge_index(new_patterns):
    """Add new learnings to the local knowledge base."""
    if KNOWLEDGE_INDEX_FILE.exists():
        with open(KNOWLEDGE_INDEX_FILE, "r", encoding="utf-8") as f:
            knowledge_index = json.load(f)
    else:
        knowledge_index = {}

    for key, responses in new_patterns.items():
        if key not in knowledge_index:
            knowledge_index[key] = responses
        else:
            # merge new responses without duplicates
            for resp in responses:
                if resp not in knowledge_index[key]:
                    knowledge_index[key].append(resp)

    with open(KNOWLEDGE_INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(knowledge_index, f, indent=4, ensure_ascii=False)

    print("✅ Knowledge index updated successfully!")


# -----------------------------
# Step 4: Recall Knowledge
# -----------------------------
def recall_from_knowledge(query):
    """Find related knowledge based on keywords in the query."""
    if not KNOWLEDGE_INDEX_FILE.exists():
        return None

    with open(KNOWLEDGE_INDEX_FILE, "r", encoding="utf-8") as f:
        knowledge_index = json.load(f)

    query_words = re.sub(r"[^a-zA-Z0-9\s]", "", query).lower().split()
    related_responses = []

    for word in query_words:
        if word in knowledge_index:
            related_responses.extend(knowledge_index[word])

    if related_responses:
        return list(set(related_responses))
    return None


# -----------------------------
# Step 5: Run Training Cycle
# -----------------------------
def run_self_training():
    """Main pipeline to process and learn from past chat memory."""
    print("🧠 Starting self-learning process...")
    cleaned_data = clean_chat_data()
    if not cleaned_data:
        print("No valid data to train on.")
        return

    patterns = extract_patterns(cleaned_data)
    update_knowledge_index(patterns)
    print("🤖 Learning complete. Knowledge saved in knowledge_index.json.")


# -----------------------------
# Optional: Test Run
# -----------------------------
if __name__ == "__main__":
    run_self_training()
