'''
responsible for api calls to caldera and processing outputs
'''
import os
import requests
from client import CALDERA_API_URL
from dotenv import load_dotenv
load_dotenv()

#for wnen we add these to the env file
CALDERA_URL = os.getenv("CALDERA_URL", "http://localhost:8888")
API_KEY     = os.getenv("CALDERA_API_KEY")
HEADERS     = {"KEY": API_KEY, "Content-Type": "application/json"}
# Agents


# Abilities

# Operations


#Health
def health_check():
    try:
        r = requests.get(f"{CALDERA_API_URL}/api/v2/health", headers=HEADERS, timeout=7)
        return r.status_code == 200
    except Exception:
        return False