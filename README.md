## A local AI-powered cybersecurity assistant that integrates with MITRE CALDERA to:

- Run adversary simulations

- Analyze output logs

- Explain results in plain English

- Generate structured reports

- Answer cybersecurity and CALDERA-related questions



## Prerequisites

Before starting, make sure the following are running on your machine or VM:

- Python 3.11+
- [Ollama](https://ollama.com) installed and running on your host ip with llama3.1:8b pulled
- CALDERA server running (see CALDERA setup below)
- A Sandcat agent deployed on your target VM using docker

---

## 1. Clone and enter the repo

## 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS

```


## 3. Install dependencies

```bash
pip install -r requirements.txt
```
## 4. CALDERA setup (if not already running)

```bash
cd /path/to/caldera
sudo docker run -it -p 8888:8888 caldera
```

CALDERA will be available at `http://localhost:8888`.
Default credentials: `red / password: <password_from_output>`

Note: add the token to your .env in ```CALDERA_API_KEY=```

## Usage

### Conversational mode (default)

Just type naturally — the AI will answer questions or trigger CALDERA actions
automatically based on what you ask and you can also ask it to explain what you currently have running:

```
You: what agents are connected?
You: run a discovery operation
You: explain the results
You: what is lateral movement?
```
### Built-in commands (deterministic)

| Command  | What it does                                      |
|----------|---------------------------------------------------|
| `status` | Show active agent and operation from memory if available      |
| `report` | Generate a structured report from CALDERA    |
| `clear`  | Wipe conversation history and CALDERA context     |
| `quit or q`   | Exit the chatbot                                  |
 `help`   | View menu options again                                  |
 | `1` | Show connected agents      |
| `2` | List available adversaries    |
| `3`   |   Check operation status                                |
 `4`   | Get & explain operation results                                  |




---

## Troubleshooting
**`Cannot reach Ollama`**
Ollama is not running. Start it with `OLLAMA_HOST=0.0.0.0:11434 ollama serve` in a separate terminal on host machine (Mac).
