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
HEADERS     = {"KEY": API_KEY, "Content-Type": "application/json", "accept": "application/json", "enable_agent_output": "true"}
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
		count=0
		for agent in agents:
			if agent['status']=='alive':
				count+=1
		if agents == [] or count == 0:
			return f"There are no agents."
		print(f"{'PAW':<10} {'PLATFORM':<10} {'ARCHITECTURE':<10} {'HOST':<10} {'USER':<10} {'STATUS':<10} {'IP'}")
		print ("-" * 100)
		for agent in agents:
			if agent['status']=='alive':
				print(f"{agent['paw']:<10} {agent['platform']:<10} {agent['architecture']:<10} {agent['host']:<10} {agent['username']:<10} {agent['status']:<10} {agent['host_ip_addrs'][0]}")
		return f"All connected agents displayed"
	except Exception:
		return f"No agents to show"

def get_agents():
	try:
		r = requests.get(f"{CALDERA_URL}/api/v2/agents", headers = HEADERS, timeout=7)
		agents=r.json()
		return agents
	except Exception:
		return False
def get_agents():
	try:
		r = requests.get(f"{CALDERA_URL}/api/v2/agents", headers = HEADERS, timeout=14)
		return r.json()
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
			"name": "test dom",
			"adversary" : {
				"adversary_id": "0f4c3c67-845e-49a0-927e-90ed33c044e0" #"2346dbbc-9965-4380-bec3-689a291f43b6"
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
		return r.status_code
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

#Helper Functions for Getting Operations Reports
def get_operation_ids():
	try:
		r = requests.get(f"{CALDERA_URL}/api/v2/operations", headers = HEADERS, timeout=7)
		op_ids = []
		operations=r.json()
		for operation in operations:
			op_ids.append(operation['id'])
		return op_ids
	except Exception:
		return False

#TODO: Look at output and figure out how to parse relevant data to pass to LLM.
def get_reports(id):
	payload = {"enable_agent_output": "True"} #Gets stdout and stderr details from the report. False omits them.
	r = requests.post(f"{CALDERA_URL}/api/v2/operations/{id}/report", headers = HEADERS, json=payload, timeout=7)
	if(r.status_code == 200):
		return r.json()
	else:
		return False


def format_report(report: dict) -> dict:
	try:
		data = report
		operation = {
			"name": data.get("name"),
			"start": data.get("start"),
			"finish": data.get("finish"),
			"planner": data.get("planner"),
			"adversary_name": data.get("adversary", {}).get("name"),
			"host_group": format_host_group(data),
			"steps": format_steps(data),
		}
		return operation
	except Exception:
		return False


def format_host_group(data: dict) -> list[dict]:
	try:
		formatted_hosts = []
		for agent in data.get("host_group", []):
			formatted_hosts.append({
				"paw": agent.get("paw"),
				"location": agent.get("location"),
				"host_ip_addrs": agent.get("host_ip_addrs", []),
			})
		return formatted_hosts
	except Exception:
		return False


def format_steps(data: dict) -> list[dict]:
	try:
		formatted_steps = []
		for paw, agent_data in data.get("steps", {}).items():
			for step in agent_data.get("steps", []):
				formatted_steps.append({
					"paw": paw,
					"command_name": step.get("name"),
					"command": step.get("plaintext_command"),  # decoded; use "command" for base64
					"description": step.get("description", "").strip(),
					"tactic": step.get("attack", {}).get("tactic"),
					"technique_name": step.get("attack", {}).get("technique_name"),
					"output": step.get("output")
				})
		return formatted_steps
	except Exception:
		return False
		
