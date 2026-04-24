'''
orchestrates communication between agent and caldera
'''
import json
from llm.client import generate_response, generate_chat
from caldera import client as caldera
from llm.prompts import SYSTEM_PROMPT
from agent.memory import ConversationMemory

class AgentController:
    def __init__(self):
        self.memory = ConversationMemory(max_turns=15)
    def chat(self, user_input):
        """
        Used only for general cybersec questions and for questions about the current operation/agent context.
        or just ask a security question. 
        handles questions like what does x attack mean or other questions.
        """
        context = self.memory.get_context_summary()
        messages = self.memory.get_messages()
        if context and context != "No active CALDERA session.":
            messages = [{"role": "system", "content": f"Current state: {context}"}]
<<<<<<< HEAD
        llm_response = generate_chat(messages)
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
=======
        llm_response = generate_chat(messages)#, system = SYSTEM_PROMPT)
        #action = parse_action() #TODO: implement this to either return json for caldera or None if it's just a regular question
        
        self.memory.add_assistant(llm_response)
        return llm_response
    # def parse_action(self, action: dict) -> str:
    #     """
    #     TODO: decide on what is needed from the user to logically decide on a caldera call.
    #     Helper function to route the user's action request to an actual caldera call.
    #     Expects a json string.
    #     """
    #     try:
    #         print(f"Parsing action: {action}")
>>>>>>> origin/dom
            
    #     except Exception as e:
    #         return f"Caldera error: {e}"
    def get_results(self) -> list[dict]:
        operation_ids = []
        operation_ids = caldera.get_operation_ids()
        reports = []
        for id in operation_ids:
            reports.append(caldera.format_report(caldera.get_reports(id)))
        reports.append(caldera.format_report(caldera.get_reports(operation_ids)))
        return reports

    def explain_results(self, results: list[dict]) -> str:
        """
        takes in caldera results and uses the llm to explain them to the user in simple terms. 
        """
        prompt = f"Explain these CALDERA results in simple terms for a red team analyst for the entire report. Do not omit anything: {json.dumps(results)}"
        explanation = generate_response(prompt)
        return explanation
    
    def list_agents(self) -> str:
        """
        uses caldera client to list agents and formats as a string
        """
        agents = caldera.show_agents()
        if not agents:
            return "Error retrieving agents."
        return agents
    
    def list_adversaries(self) -> str:
        """
        Uses caldera client to list adversaries and then formats as a string
        """
        adversaries = caldera.show_adversaries()
        if not adversaries:
            return "Error retrieving adversaries."
        return adversaries
    
    def create_operation(self):
        caldera.create_operation()

    def list_operations(self) -> str:
        """
        uses caldera client to list operations as a string
        """
        caldera.show_operations()
        pass

    def stop_operation(self, params)-> str:
        """
        stops caldera operation by id and returns a statement telling the user the operation has stopped
        """
        pass




