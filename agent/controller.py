'''
orchestrates communication between agent and caldera
'''
import json
from llm.client import generate_response, generate_chat
from caldera import client as caldera

class AgentController:
    def __init__(self):
        self.memory = ConversationMemory(max_turns=15)
    def chat(self, user_input):
        pass





