''' 
ollama api wrapper
'''
import requests
from config import OLLAMA_API_URL, MODEL_NAME
import os
from dotenv import load_dotenv
load_dotenv()

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL")

def generate_response(prompt):
    '''
    Generate a response from the model using the Ollama API.
    '''
    url = f"{OLLAMA_API_URL}/api/generate"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0.2,
        "stream": false
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get('response', '').strip()
        
    except requests.exceptions.ConnectionError:
        return "Error: cannot reach Ollama"
        
    except Exception as e:
        return f"Error on sLLM call: {e}"
def generate_chat(messages):
    """
    Multi-turn chats with /chat endpoint

    """
    url = f"{OLLAMA_API_URL}/api/chat"
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
    }
   
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["message"]["content"].strip()
    except Exception as e:
        return f"[ERROR] Chat call failed: {e}"