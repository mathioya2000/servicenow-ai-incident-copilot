# ServiceNow AI Incident Copilot

## Overview
AI-powered ServiceNow Incident Management assistant that analyzes incidents and writes structured guidance into Work Notes.

This project integrates:

- ServiceNow Incident Management
- FastAPI backend
- OpenAI API
- Render cloud deployment
- ServiceNow UI Action
- GlideAjax Script Include
- Knowledge Base retrieval
- Major incident assessment

## Business Use Case
Service desk and ITSM teams spend time manually reviewing incidents, identifying impact, recommending troubleshooting steps, and deciding escalation paths.

This assistant accelerates incident triage by generating:

- incident summary
- business impact
- urgency explanation
- troubleshooting steps
- assignment group recommendation
- major incident assessment
- knowledge article recommendations
- resolution notes draft

---

## Architecture

ServiceNow Incident Record  
↓  
UI Action: Analyze with AI  
↓  
GlideAjax Script Include  
↓  
FastAPI REST API on Render  
↓  
ServiceNow Incident + Knowledge API  
↓  
OpenAI Analysis Engine  
↓  
Structured JSON Response  
↓  
ServiceNow Work Notes  

---

## API Endpoints

### Health Check
GET /

### Exact Incident AI Analysis
GET /ai-incident/{incident_number}

Example:

/ai-incident/INC0010034

Returns structured AI analysis for a specific ServiceNow incident.

---

## Key Features

- Exact incident lookup
- Priority-aware analysis
- Major incident detection for Priority 1
- Knowledge article retrieval foundation
- Clean Work Notes formatting
- Cloud-hosted backend
- Secure environment variables

---

## Tech Stack

- Python
- FastAPI
- OpenAI API
- ServiceNow REST API
- GlideAjax
- RESTMessageV2
- Render
- GitHub

---

## ServiceNow Components

### UI Action
Incident [incident]

Button:

Analyze with AI

### Script Include
AIIncidentCopilotAjax

### Output
Writes AI analysis into Incident Work Notes.

---

## Deployment

Hosted on Render.

Environment variables:

OPENAI_API_KEY  
SERVICENOW_INSTANCE_URL  
SERVICENOW_USERNAME  
SERVICENOW_PASSWORD  

---

## Portfolio Value

Demonstrates:

- ServiceNow development
- ITSM automation
- AI integration
- major incident intelligence
- REST API development
- cloud deployment
- enterprise workflow automation

---

## Author

Joseph Mwangi