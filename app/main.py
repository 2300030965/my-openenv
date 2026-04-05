from fastapi import FastAPI
from app.env import SmartSupportDeskEnv
from app.models import EnvAction

app = FastAPI()

ENV = SmartSupportDeskEnv()

@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/reset")
def reset(task_name: str = "ticket_triage_easy"):
    return ENV.reset(task_name).model_dump()

@app.get("/state")
def state():
    return ENV.state().model_dump()

@app.post("/step")
def step(action: EnvAction):
    return ENV.step(action).model_dump()