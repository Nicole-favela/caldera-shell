''' 
ollama api wrapper
'''
import requests
from config import OLLAMA_API_URL, MODEL_NAME

def generate_response(prompt):
    '''
    Generate a response from the model using the Ollama API.
    '''
    url = f"{OLLAMA_API_URL}/api/generate"
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "max_tokens": 1000,
        "temperature": 0.2
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get('response', '')
    else:
        raise Exception(f"Error generating response: {response.status_code} - {response.text}")
