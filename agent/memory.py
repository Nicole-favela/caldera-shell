'''
handles chat and state memory for the agent using sliding window implementation
maintains only max_turns and context needed for caldera
'''
from collections import deque

class ConversationMemory:

    def __init__(self, max_turns=15):
        self.history: deque[dict] = deque(maxlen=max_turns * 2)  # user+assistant pairs
        self.caldera_context: dict = {"op_id":None, "agent_paw": None, "op_name": None} #TODO: decide on what this should contain!
    #for formatting user and assistant messages for ollama
    def add_user(self, message: str):
        self.history.append({"role": "user", "content": message})

    def add_assistant(self, message: str):
        self.history.append({"role": "assistant", "content": message})
    #converts to list to send to ollama
    def get_messages(self) -> list[dict]:
        return list(self.history)
    #sets caldera paw agent identifier
    def set_agent(self, paw: str):
        self.caldera_context["agent_paw"] = paw

    def set_last_results(self, results: list[dict]):
        self.caldera_context["last_results"] = results
    def get_context_summary(self) -> str:
        caldera_context = self.caldera_context
        info = []
        if caldera_context["agent_paw"]:
            info.append(f"Current agent: {caldera_context['agent_paw']}")
        if caldera_context["op_name"]:
            info.append(f"Current operation: {caldera_context['op_name']}, ID: {caldera_context['op_id']}")
        return ", ".join(info) if info else "No active CALDERA session."
    def clear(self):
        self.history.clear()
        self.caldera_context = {k: None for k in self.caldera_context}