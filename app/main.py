import re
from fastapi import FastAPI, Request
from env.environment import HealthcareEnv
from env.models import Action

app = FastAPI()
env = None

def parse_action(action_str: str):
    """Extracts action details from LLM strings like assign('p1', 'd1')"""
    action_str = action_str.strip().lower()
    match = re.search(r"assign\(['\"](.+?)['\"],\s*['\"](.+?)['\"]\)", action_str)
    if match:
        return {"action_type": "assign", "patient_id": match.group(1), "doctor_id": match.group(2)}
    if "wait" in action_str:
        return {"action_type": "wait"}
    return {"action_type": "wait"} # Fallback to wait if AI mumbles

@app.post("/reset")
async def reset(request: Request):
    global env
    data = await request.json()
    task = data.get("task", "easy")
    env = HealthcareEnv(task_type=task)
    state = env.reset()
    return {"state": state}

@app.post("/step")
async def step(request: Request):
    global env
    if env is None:
        return {"error": "Env not initialized"}
    
    data = await request.json()
    raw_action = data.get("action", "wait()")
    
    # FIX: Convert dict to Action object so env.step(action.action_type) works
    action_dict = parse_action(raw_action)
    structured_action = Action(**action_dict) 
    
    result = env.step(structured_action)
    return result