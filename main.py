# main.py - Full MCP Weather Chatbot with Animation
from mcp import MCP
from agent import is_weather_question, search_wiki
from agent import needs_search, search_wiki
from animator import show_step
from transformers import pipeline
import os

# === 1. Load AI Model (small & safe) ===
show_step("AI", "Loading small brain (flan-t5-small)...", "green")
generator = pipeline("text2text-generation", model="google/flan-t5-small")

# === 2. Start MCP ===
mcp = MCP()

# === 3. Welcome ===
show_step("MCP", "Context Protocol Active: 3 messages + 1 fact", "yellow")

# === 4. Chat Loop ===
print("\n" + "="*50)
print("MCP WEATHER CHATBOT READY! (Type 'quit' to stop)")
print("="*50 + "\n")

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() == "quit":
        show_step("Bye", "Chatbot stopped. Stay dry!", "magenta")
        break
    
    if not user_input:
        continue

    # === Step 1: User speaks ===
    show_step("User", user_input, "blue")
    mcp.add_user(user_input)

    # === Step 2: Check small talk FIRST ===
    from agent import is_small_talk
    small_response = is_small_talk(user_input)
    if small_response:
        show_step("Agent", "Friendly chat detected!", "cyan")
        show_step("Assistant", small_response, "green")
        mcp.add_assistant(small_response)
        continue  # Skip AI thinking

    # === Step 3: Weather or Wiki? ===
    if is_weather_question(user_input):
        show_step("Agent", "Weather question! Getting live data...", "cyan")
        from weather import get_weather
        city = user_input.split("in")[-1].strip() if "in" in user_input.lower() else "London"
        fact = get_weather(city)
        mcp.add_fact(fact)
        show_step("Weather", fact, "white")
    elif needs_search(user_input):
        show_step("Agent", "I don't know... searching Wikipedia...", "yellow")
        fact = search_wiki(user_input)
        mcp.add_fact(fact)
        show_step("Wiki", fact, "white")
    else:
        mcp.add_fact("")
        show_step("Agent", "I know this! No search needed.", "green")

    # === Step 4: MCP builds context ===
    context = mcp.get_context()
    show_step("MCP", context, "yellow")

    # === Step 5: AI answers ===
    prompt = f"Answer in 1 short sentence using this: {context}"
    show_step("GenAI", "Thinking...", "purple")
    result = generator(prompt, max_length=60, do_sample=False)[0]['generated_text']
    
    show_step("Assistant", result, "green")
    mcp.add_assistant(result)