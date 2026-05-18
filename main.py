from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests

load_dotenv()

app = FastAPI(title="ServiceNow AI Incident Copilot")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class IncidentRequest(BaseModel):
    number: str
    short_description: str
    description: str
    priority: str | None = None
    category: str | None = None


@app.get("/")
def home():
    return {"message": "ServiceNow AI Incident Copilot is running"}


@app.get("/check-env")
def check_env():
    openai_key = os.getenv("OPENAI_API_KEY")
    return {
        "openai_key_loaded": bool(openai_key)
    }


@app.get("/ai-test")
def ai_test():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an IT support assistant."},
            {"role": "user", "content": "Summarize what an incident copilot should do in one sentence."}
        ]
    )

    return {
        "ai_response": response.choices[0].message.content
    }


@app.post("/summarize-incident")
def summarize_incident(incident: IncidentRequest):
    prompt = f"""
You are an ITSM incident copilot.

Summarize this ServiceNow incident clearly for an IT support analyst.

Incident Number: {incident.number}
Short Description: {incident.short_description}
Description: {incident.description}
Priority: {incident.priority}
Category: {incident.category}

Return:
1. Plain-English summary
2. Possible impact
3. First troubleshooting step
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful ServiceNow ITSM assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "incident_number": incident.number,
        "ai_summary": response.choices[0].message.content
    }


@app.get("/test-servicenow")
def test_servicenow():
    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = f"{instance_url}/api/now/table/incident?sysparm_limit=1"

    response = requests.get(
        url,
        auth=(username, password),
        headers={"Accept": "application/json"}
    )

    return {
        "status_code": response.status_code,
        "content_type": response.headers.get("Content-Type"),
        "text_preview": response.text[:500]
    }
@app.get("/latest-incident")
def latest_incident():
    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = (
        f"{instance_url}/api/now/table/incident"
        "?sysparm_limit=1"
        "&sysparm_query=ORDERBYDESCsys_created_on"
        "&sysparm_fields=number,short_description,description,priority,category,state,sys_created_on"
    )

    response = requests.get(
        url,
        auth=(username, password),
        headers={"Accept": "application/json"}
    )

    data = response.json()
    return data["result"][0] if data.get("result") else {"message": "No incidents found"}
@app.get("/ai-latest-incident")
def ai_latest_incident():
    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = (
        f"{instance_url}/api/now/table/incident"
        "?sysparm_limit=1"
        "&sysparm_query=ORDERBYDESCsys_created_on"
        "&sysparm_fields=number,short_description,description,priority,category,state,sys_created_on"
    )

    response = requests.get(
        url,
        auth=(username, password),
        headers={"Accept": "application/json"}
    )

    incident = response.json()["result"][0]

    prompt = f"""
You are a ServiceNow ITSM AI Incident Copilot.

Analyze this real ServiceNow incident:

Number: {incident.get("number")}
Short Description: {incident.get("short_description")}
Description: {incident.get("description")}
Priority: {incident.get("priority")}
Category: {incident.get("category")}
State: {incident.get("state")}
Created: {incident.get("sys_created_on")}

Return:
1. Incident summary
2. Business impact
3. Urgency explanation
4. First 3 troubleshooting steps
5. Suggested assignment group
"""

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert ServiceNow ITSM support analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "incident": incident,
        "ai_analysis": ai_response.choices[0].message.content
    }
@app.get("/ai-incident/{incident_number}")
def ai_incident_by_number(incident_number: str):
    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    url = (
        f"{instance_url}/api/now/table/incident"
        f"?sysparm_query=number={incident_number}"
        "&sysparm_limit=1"
        "&sysparm_fields=number,short_description,description,priority,category,state,sys_created_on"
    )

    response = requests.get(
        url,
        auth=(username, password),
        headers={"Accept": "application/json"}
    )

    data = response.json()

    if not data.get("result"):
        return {"error": f"Incident {incident_number} not found"}

    incident = data["result"][0]

    prompt = f"""
You are a ServiceNow ITSM AI Incident Copilot.

Analyze this ServiceNow incident:

Number: {incident.get("number")}
Short Description: {incident.get("short_description")}
Description: {incident.get("description")}
Priority: {incident.get("priority")}
Category: {incident.get("category")}
State: {incident.get("state")}
Created: {incident.get("sys_created_on")}

Return:
1. Incident summary
2. Business impact
3. Urgency explanation
4. First 3 troubleshooting steps
5. Suggested assignment group
"""

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert ServiceNow ITSM support analyst."},
            {"role": "user", "content": prompt}
        ]
    )

    return {
        "incident": incident,
        "ai_analysis": ai_response.choices[0].message.content
    }