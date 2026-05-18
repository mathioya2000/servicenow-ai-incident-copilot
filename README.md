\# ServiceNow AI Incident Copilot



An AI-powered ITSM assistant that connects to ServiceNow incidents, sends incident details to OpenAI, and returns a clear support analysis for IT teams.



\## What It Does



\- Connects to a ServiceNow Personal Developer Instance

\- Retrieves the latest incident from the Incident table

\- Uses OpenAI to analyze the incident

\- Returns:

&#x20; - Incident summary

&#x20; - Business impact

&#x20; - Urgency explanation

&#x20; - Troubleshooting steps

&#x20; - Suggested assignment group



\## Tech Stack



\- Python

\- FastAPI

\- OpenAI API

\- ServiceNow REST API

\- Swagger UI

\- Git / GitHub



\## Current MVP Features



\- `/check-env` — verifies API key loading

\- `/ai-test` — tests OpenAI connection

\- `/summarize-incident` — summarizes a sample incident

\- `/test-servicenow` — tests ServiceNow REST connection

\- `/latest-incident` — retrieves latest ServiceNow incident

\- `/ai-latest-incident` — analyzes latest ServiceNow incident with AI



\## Security



Secrets are stored in `.env` and excluded from GitHub using `.gitignore`.



Example `.env`:



```env

OPENAI\_API\_KEY=your\_key\_here

SERVICENOW\_INSTANCE\_URL=https://your-instance.service-now.com

SERVICENOW\_USERNAME=your\_username

SERVICENOW\_PASSWORD=your\_password

