'''
orchestrates communication between agent and caldera
'''
import json
from llm.client import generate_response, generate_chat
from caldera import client as caldera
<<<<<<< HEAD
=======
from llm.prompts import SYSTEM_PROMPT
>>>>>>> master
from agent.memory import ConversationMemory

class AgentController:
    def __init__(self):
        self.memory = ConversationMemory(max_turns=15)
    def chat(self, user_input):
        """
        main entry point to take in user input and return a response. Decides whether the user wants to use caldera 
        or just ask a security question. 
        """
        context = self.memory.get_context_summary()
        messages = self.memory.get_messages()
        if context and context != "No active CALDERA session.":
            messages = [{"role": "system", "content": f"Current state: {context}"}]
        llm_response = generate_chat(messages, system = SYSTEM_PROMPT)
        action = parse_action() #TODO: implement this to either return json for caldera or None if it's just a regular question
        if action:
            result = self.use_caldera(action)
        else: #this is just a regular question
            result = llm_response
        self.memory.add_assistant(result)
        return result
    def parse_action(self, action: dict) -> str:
        """
        TODO: decide on what is needed from the user to logically decide on a caldera call.
        Helper function to route the user's action request to an actual caldera call.
        Expects a json string.
        """
        try:
            print(f"Parsing action: {action}")
            
        except Exception as e:
            return f"Caldera error: {e}"
    def list_agents(self) -> str:
        """
        uses caldera client to list agents and formats as a string
        """
        pass
    def list_operations(self) -> str:
        """
        uses caldera client to list operations as a string
        """
        pass
    def stop_operation(self, params)-> str:
        """
        stops caldera operation by id and returns a statement telling the user the operation has stopped
        """
        pass




