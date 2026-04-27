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
        self.memory.add_user(user_input) #store first message
        context = self.memory.get_context_summary()
        messages = self.memory.get_messages() #user convo history
        if context or messages:
            messages = [{"role": "system", "content": f"Current state: {context}"}]
            messages += self.memory.get_messages()
            # messages.append({"role": "user", "content": user_input})
        llm_response = generate_chat(messages, system=SYSTEM_PROMPT)#, system = SYSTEM_PROMPT)
        #action = parse_action() #TODO: implement this to either return json for caldera or None if it's just a regular question
        
        self.memory.add_assistant(llm_response)
        return llm_response
    
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
        #agents = caldera.show_agents()
        agents = caldera.get_agents()
        if not agents:
            res = "Error retrieving agents."
            self.memory.add_assistant(res)
            return res

        top_agent = agents[0]
        self.memory.set_agent(top_agent["paw"])
        formatted_lines = ["Active agents:"]
        for agent in agents: #trim down to just relevant info
            formatted_lines.append(f"agent paw: {agent.get('paw', '?')}, group: {agent.get('group', '?')}, platform: {agent.get('platform', '?')}, architecture: {agent.get('architecture', '?')},  host: {agent.get('host', '?')}, status: {agent.get('status', '?')}, ip: {agent.get('host_ip_addrs', ['?'])[0]}")
        full_result =  "\n".join(formatted_lines)
        self.memory.add_assistant(full_result)
        return full_result
        
    def get_agent(self)-> str:
        agent=caldera.get_agents()
        agent_1=agent[0]
        self.memory.set_agent(agent_1["paw"])

    def list_adversaries(self) -> str:
        """
        Uses caldera client to list adversaries and then formats as a string
        """
        adversaries = caldera.show_adversaries()
        if not adversaries:
            return "Error retrieving adversaries."
        return adversaries
    
    def create_operation(self,name="test"):
        caldera.create_operation(name)
        op_id=caldera.find_operation(name)
        print(op_id)
        self.memory.set_operation(op_id)
        self.memory.add_assistant(op_id)
        return op_id

    def list_operations(self) -> str:
        """
        uses caldera client to list operations as a string
        """
        caldera.show_operations()
        pass

    def get_operation(self, op_id)-> str:
        """
        stops caldera operation by id and returns a statement telling the user the operation has stopped
        """
        report=caldera.get_reports(op_id)
        formated_report=caldera.format_report(report)
        pass
  
