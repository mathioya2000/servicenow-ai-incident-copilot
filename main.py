from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os
import requests
import json

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
    return {
        "openai_key_loaded": bool(os.getenv("OPENAI_API_KEY")),
        "servicenow_url_loaded": bool(os.getenv("SERVICENOW_INSTANCE_URL")),
        "servicenow_username_loaded": bool(os.getenv("SERVICENOW_USERNAME")),
        "servicenow_password_loaded": bool(os.getenv("SERVICENOW_PASSWORD")),
    }


@app.get("/ai-test")
def ai_test():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an IT support assistant."},
            {"role": "user", "content": "Summarize what an incident copilot should do in one sentence."},
        ],
    )

    return {"ai_response": response.choices[0].message.content}


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
        headers={"Accept": "application/json"},
        timeout=30,
    )

    data = response.json()

    if not data.get("result"):
        return {"error": f"Incident {incident_number} not found"}

    incident = data["result"][0]
    kb_articles = search_knowledge_articles(incident)

    return analyze_incident_with_ai(incident, kb_articles)


def search_knowledge_articles(incident: dict):
    instance_url = os.getenv("SERVICENOW_INSTANCE_URL")
    username = os.getenv("SERVICENOW_USERNAME")
    password = os.getenv("SERVICENOW_PASSWORD")

    search_text = incident.get("short_description") or incident.get("category") or ""

    url = (
        f"{instance_url}/api/now/table/kb_knowledge"
        f"?sysparm_query=workflow_state=published^short_descriptionLIKE{search_text}"
        "&sysparm_limit=3"
        "&sysparm_fields=number,short_description"
    )

    response = requests.get(
        url,
        auth=(username, password),
        headers={"Accept": "application/json"},
        timeout=30,
    )

    data = response.json()
    return data.get("result", [])


def analyze_incident_with_ai(incident: dict, kb_articles=None):
    if kb_articles is None:
        kb_articles = []

    prompt = f"""
You are a ServiceNow ITSM AI Incident Copilot.

Analyze this ServiceNow incident.

Incident:
Number: {incident.get("number")}
Short Description: {incident.get("short_description")}
Description: {incident.get("description")}
Priority: {incident.get("priority")}
Category: {incident.get("category")}
State: {incident.get("state")}
Created: {incident.get("sys_created_on")}

ServiceNow Knowledge Articles Found:
{kb_articles}

Return STRICT JSON only:
{{
  "incident_summary": "...",
  "business_impact": "...",
  "urgency_explanation": "...",
  "troubleshooting_steps": ["...", "...", "..."],
  "assignment_group": "...",
  "resolution_notes": "...",
  "major_incident_assessment": "...",
  "knowledge_articles": ["...", "...", "..."]
}}

Rules:
- If Priority = 1, treat as major incident candidate.
- Include escalation guidance.
- Include communication recommendations.
- Use real KB articles if found.
- Return JSON only, no markdown.
"""

    ai_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an expert ServiceNow ITSM support analyst. Always return valid JSON."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    ai_text = ai_response.choices[0].message.content

    try:
        parsed = json.loads(ai_text)
    except:
        parsed = {
            "incident_summary": ai_text,
            "business_impact": "",
            "urgency_explanation": "",
            "troubleshooting_steps": [],
            "assignment_group": "",
            "resolution_notes": "",
            "major_incident_assessment": "",
            "knowledge_articles": []
        }

    return {
        "incident": incident,
        "kb_articles_found": kb_articles,
        "structured_ai": parsed
    }