# agent.py - Smart decider with small talk
import wikipedia
import re

# === 1. Detect if needs Wikipedia search ===
def needs_search(question):
    q = question.lower()
    wiki_triggers = ["capital", "who", "what", "when", "where", "how"]
    return any(word in q for word in wiki_triggers)

# === 2. Detect if it's a weather question ===
def is_weather_question(question):
    q = question.lower()
    return any(word in q for word in ["weather", "rain", "sunny", "temperature", "forecast", "cloud"])

# === 3. Detect small talk (hi, thanks, bye) ===
def is_small_talk(question):
    q = question.lower().strip("!?.")
    small_talk = {
        "hi": "Hello! How can I help?",
        "hello": "Hi there! Ask me anything.",
        "hey": "Hey! What's up?",
        "thank you": "You're welcome!",
        "thanks": "Anytime!",
        "thank u": "You're welcome!",
        "bye": "Goodbye! Stay dry!",
        "goodbye": "See you later!"
    }
    return small_talk.get(q)

# === 4. Safe Wikipedia search ===
def search_wiki(query):
    try:
        safe_query = re.sub(r'[^a-zA-Z0-9 ]', '', query)
        if not safe_query.strip():
            return "No safe search term."
        wikipedia.set_lang("en")
        summary = wikipedia.summary(safe_query, sentences=1)
        return summary[:200]
    except:
        return "I couldn't find that."