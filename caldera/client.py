'''
responsible for api calls to caldera and processing outputs
'''
import os
import subprocess
import requests
import json
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
		
def show_agents():
	try:
		r = requests.get(f"{CALDERA_URL}/api/v2/agents", headers = HEADERS, timeout=7)
		agents=r.json()
		print(f"{'PAW':<10} {'GROUP':<10} {'PLATFORM':<10}  {'ARCHITECTURE':<10} {'TRUSTED':<10} {'HOST':<10} {'USER':<10} {'STATUS':<10} {'IP'}")
		print ("-" * 100)
		for agent in agents:
			print(f"{agent['paw']:<10} {agent['group']:<10} {agent['platform']:<10} {agent['architecture']:<10} {agent['trusted']:<10} {agent['host']:<10} {agent['username']:<10} {agent['status']:<10} {agent['host_ip_addrs'][0]}")
	except Exception:
		return False

# Abilities
def show_abilities():
	try:
		r = requests.get(f"{CALDERA_URL}/api/v2/abilities", headers = HEADERS, timeout=7)
		abilities=r.json()
		for ability in abilities:
			platforms= list({e["platform"] for e in ability.get("executors", [])})
			print(f"""
NAME:		{ability['name']}
ABILITY ID: 	{ability['ability_id']}
TACTIC: 	{ability['tactic']}
TECHNIQUE NAME: {ability['technique_name']}
TECHNIQUE ID:	{ability['technique_id']}
DESCRIPTION:	{ability['description']}
PLATFORMS:	{", ".join(platforms)}
DELETE PAYLOAD: {ability['delete_payload']}
			""")
	except Exception:
		return False

# Adversaries (work in progress)
def show_adversaries():
	try:
		r = requests.get(f"{CALDERA_URL}/api/v2/adversaries", headers = HEADERS, timeout=7)
		adversaries=r.json()
		for adversary in adversaries:
			print(f"""
NAME:		{adversary['name']}
DESCRIPTION: 	{adversary['description']}
ADVERSARY ID: 	{adversary['adversary_id']}
ATOMIC ORDERING:{adversary['atomic_ordering']}
PLUGIN:		{adversary['plugin']}
			""")
	except Exception:
		return false

# Operations


#Health
def health_check():
    try:
        r = requests.get(f"{CALDERA_URL}/api/v2/health", headers=HEADERS, timeout=7)
        return r.status_code == 200
    except Exception:
        return False


print(show_adversaries())
