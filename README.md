
````markdown
# Smart Support Desk OpenEnv

A real-world OpenEnv environment where an AI agent triages IT/helpdesk tickets.

## Features
- Real-world support workflow
- Typed models
- step() / reset() / state()
- Three tasks: easy, medium, hard
- Reward with partial progress
- Baseline inference script
- Dockerized deployment
- Hugging Face Space compatible

## Tasks

### 1. ticket_triage_easy
Classify priority and assign correct team for straightforward tickets.

### 2. ticket_triage_medium
Classify, assign, collect missing info, and propose a valid fix.

### 3. ticket_triage_hard
Handle security or production incidents with correct severity, routing, evidence gathering, and remediation.

## Action Space
JSON action:
{
  "action_type": "classify",
  "payload": {
    "priority": "high"
  }
}
````

Supported action types:

* classify
* assign
* request_info
* propose_fix
* resolve

## Observation Space

Returns ticket metadata, missing info, known info, history, step count, and last action error.

## Reward Design

* Correct priority: +0.20
* Correct team: +0.20
* Request relevant missing info: +0.15
* Good remediation proposal: +0.20
* Final graded completion: up to +1.00
* Incorrect or malformed actions get penalties

All rewards are clamped to 0.0–1.0.

## Run locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 7860

Then in another terminal:

python inference.py

## Validate

openenv validate

## API

* POST /reset
* GET /state
* POST /step

## Deployment

This project can be deployed to Hugging Face Spaces using Docker.

````

---