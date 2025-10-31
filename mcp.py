# mcp.py - Model Context Protocol
class MCP:
    def __init__(self):
        self.history = []  # List of messages
        self.fact = ""     # One fact from search

    def add_user(self, text):
        self.history.append({"role": "user", "content": text})
        self._trim()

    def add_assistant(self, text):
        self.history.append({"role": "assistant", "content": text})

    def add_fact(self, fact):
        self.fact = fact[:200]  # Max 200 chars

    def _trim(self):
        # Keep only last 3 messages
        if len(self.history) > 3:
            self.history = self.history[-3:]

    def get_context(self):
        # Build clean context for AI
        parts = []
        if self.fact:
            parts.append(f"Fact: {self.fact}")
        for msg in self.history:
            parts.append(f"{msg['role'].capitalize()}: {msg['content']}")
        return " | ".join(parts)