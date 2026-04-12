from caldera.client import health_check
from agent.controller import AgentController
BANNER = """
╔══════════════════════════════════════════════════╗
║   CALDERA AI Red Team Assistant (Llama 3.1)     ║
║   Commands: 'report', 'clear', 'status', 'quit' ║
╚══════════════════════════════════════════════════╝
"""

def main():
    print(BANNER)
    if not health_check():
        print('Warning cannot reach caldera... defaulting to simple AI agent')
    agent = AgentController()
    while True:
        try:
            user_input = input("You: ").strip()
        except(EOFError, KeyboardInterrupt):
            print("\nBye")
            break
        if not user_input:
            continue
        if user_input.lower() == 'quit' or user_input.lower() == 'q':
            break

        #TODO: add other status report and clear operations
        response = agent.chat(user_input)
        print(f"\nAgent: {response}")
if __name__ == "__main__":
    main()