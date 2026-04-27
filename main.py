"""
-----------------------------------------------------------
USER INPUT ROUTING
-----------------------------------------------------------

Every user input is classified into ONE of three types:

1. NUMBER INPUT (e.g., "1", "3", "5")
   → Routed to: handle_menu_pick()
   → Executes CALDERA-related actions with no llm involvement, just api calls and formatting returned

2. COMMAND INPUT (e.g., "status", "clear", "report", "quit")
   → Routed to: local utility handlers

3. FREE TEXT INPUT (any other input)
   → Routed to: agent.chat()
   → Handled entirely by LLM using conversation history and context


-----------------------------------------------------------
MENU OPTIONS → SYSTEM BEHAVIOR
-----------------------------------------------------------

[1] Show connected agents
    → agent.list_agents()
    → Returns machines currently controlled by CALDERA

[2] List available adversaries
    → agent.list_adversaries()
    → Returns predefined attack profiles (MITRE ATT&CK)

[3] Check operation status
    → agent.list_operations()
    → Displays running/completed operations

[4] Get & explain operation results
    → agent.get_results(raw=True) which is just a caldera api call to get results in raw form
    → agent.explain_results(results)
    → Pipeline:
        CALDERA → raw data → LLM explanation


"""

BANNER = """
╔══════════════════════════════════════════════════╗
║   CALDERA AI Red Team Assistant (Llama 3.1)      ║
║   Commands: 'report', 'clear', 'status', 'quit'  ║
╚══════════════════════════════════════════════════╝
Type a number to take a CALDERA action, or just type
a question in plain English at any time.
"""
MENU = """
─── CALDERA Actions ──────────────────────────
  1. Show connected agents
  2. List available adversaries
  3. Check operation status
  4. Get & explain operation results
─── Other ────────────────────────────────────
  status  — show active agent / operation
  report  — generate full report from results
  clear   — reset memory
  quit    — exit
  help    — show the menu options again
──────────────────────────────────────────────
"""
HELP_MENU = """ 
------------------ What these options mean: ____________________
1. Show connected agents
    - Lists all agents currently connected to CALDERA, along with details like their platform, host, and status.

""" #TODO: ADD DETAILED EXPLANATIONS OF EACH ITEM/OPTION FOR THAT THE USER CAN SELECT. 
from caldera.client import health_check, show_agents as list_agents, show_adversaries as list_adversaries, create_agent,create_agent2, create_operation, find_operation
from agent.controller import AgentController
import time
import asyncio
def print_menu():
    print(MENU)
def print_help():
    print(HELP_MENU)


def handle_menu_pick(pick, agent):
    if pick == '1':
        return agent.list_agents()
    elif pick == '2':
        return agent.list_adversaries()
    elif pick == '3':
        return agent.list_operations()
    elif pick == '4': # this should be the only option that uses caldera + llm to explain
        result = agent.get_results()
        return agent.explain_results(result)

async def async_main():
    print(BANNER)
   
    if not health_check():
        print('Warning cannot reach caldera... defaulting to simple AI agent')
    create_agent()
    time.sleep(1.5)
    agent = AgentController()
    agent.get_agent()
    response=agent.chat(agent.get_agent())
    print_menu()
    report_name=""
    op_id=""
    while True:
        try:
            user_input = input("You: ").strip()
        except(EOFError, KeyboardInterrupt):
            print("\nBye")
            break
        if not user_input:
            continue
        elif user_input.lower() == 'quit' or user_input.lower() == 'q':
            break
        elif user_input.lower() == "clear":
            agent.memory.clear()
            print("  Memory cleared.\n")
            print_menu()
            continue
        elif user_input.lower() == "status":
            print(f"  {agent.memory.get_context_summary()}\n")
            continue
        elif user_input.lower() == "report":
            if report_name==""
            	print(f" No report currently please enter operation name.")
            else:
            	if find_operation(report_name) == op_id
            		print(f" Generating report results...\n") #todo: implement report
            		agent.get_operation(op_id)
            continue
        elif user_input.lower() == "help":
            print_menu()
            continue
        elif user_input in ['1', '2', '3', '4']: #TODO: add llm involvement for 3 and 5. might need to separate these out
            print(f"  Processing CALDERA action {user_input}...\n") 
            response = handle_menu_pick(user_input, agent)
            print(f"\n{response}")
            print_menu()
            continue
        else:
            print("  Processing your question...\n")
            response = agent.chat(user_input)
            if "create_agent" in response:
            	create_agent2()
            	print("creating agent")
            elif "Creating Operation" in response:
            	name=str(user_input).split()
            	op_id=agent.create_operation(name[-1])
            print(f"\nAgent: {response}")
            continue
if __name__ == "__main__":

    asyncio.run(async_main())

