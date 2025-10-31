# gui.py - Simple GUI for MCP Weather Chatbot
import customtkinter as ctk
from mcp import MCP
from agent import needs_search, is_weather_question, is_small_talk, search_wiki
from weather import get_weather
from transformers import pipeline
import threading

# === 1. Load AI Model (once) ===
print("Loading AI model... (this takes 10 seconds)")
generator = pipeline("text2text-generation", model="google/flan-t5-small")
mcp = MCP()

# === 2. Setup GUI ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("500x600")
app.title("MCP Weather AI - By You")

# === 3. Chat Display ===
chat_box = ctk.CTkTextbox(app, width=460, height=450, font=("Arial", 14))
chat_box.pack(pady=20)
chat_box.insert("end", "MCP Weather AI Ready! Ask me anything.\n\n")
chat_box.configure(state="disabled")

# === 4. Input + Button ===
frame = ctk.CTkFrame(app)
frame.pack(pady=10)

entry = ctk.CTkEntry(frame, placeholder_text="Type here...", width=350)
entry.pack(side="left", padx=5)

# === 5. Send Function ===
def send_message():
    user_text = entry.get().strip()
    if not user_text or user_text.lower() == "quit":
        return
    
    # Show user message
    chat_box.configure(state="normal")
    chat_box.insert("end", f"You: {user_text}\n", "user")
    chat_box.configure(state="disabled")
    entry.delete(0, "end")
    
    # Run AI in background
    threading.Thread(target=process_ai, args=(user_text,), daemon=True).start()

def process_ai(user_input):
    mcp.add_user(user_input)
    
    # Small talk?
    small_response = is_small_talk(user_input)
    if small_response:
        add_assistant(small_response)
        return
    
    # Weather?
    if is_weather_question(user_input):
        city = user_input.split("in")[-1].strip() if "in" in user_input.lower() else "London"
        fact = get_weather(city)
        mcp.add_fact(fact)
        add_assistant(f"Weather in {city}: {fact.split(':')[-1]}")
        return
    
    # Wiki?
    if needs_search(user_input):
        fact = search_wiki(user_input)
        mcp.add_fact(fact)
    
    # AI Answer
    context = mcp.get_context()
    prompt = f"Answer in 1 short sentence using this: {context}"
    result = generator(prompt, max_length=60, do_sample=False)[0]['generated_text']
    
    add_assistant(result)
    mcp.add_assistant(result)

def add_assistant(text):
    chat_box.configure(state="normal")
    chat_box.insert("end", f"Tuff Agent: {text}\n\n", "ai")
    chat_box.configure(state="disabled")
    chat_box.see("end")

# Tags for colors
chat_box.tag_config("user", foreground="#4FC3F7")
chat_box.tag_config("ai", foreground="#A5D6A7")

# Bind Enter key
entry.bind("<Return>", lambda e: send_message())
send_btn = ctk.CTkButton(frame, text="Send", width=80, command=send_message)
send_btn.pack(side="left")

# === 6. Run ===
app.mainloop()