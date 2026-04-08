import os
import re
import asyncio
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from openai import OpenAI

from env.environment import HealthcareEnv
from env.models import Action

# -----------------------------
# CONFIG (LLM)
# -----------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

client = None
if HF_TOKEN:
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI()
env = None
templates = Jinja2Templates(directory="templates")

# -----------------------------
# AGENT STATUS (GLOBAL)
# -----------------------------
agent_status = {
    "is_running": False,
    "final_score": 0.0,
    "total_reward": 0.0
}

# -----------------------------
# DASHBOARD
# -----------------------------
@app.get("/", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        request=request
    )

# -----------------------------
# ACTION PARSER
# -----------------------------
def parse_action(action_str: str):
    match = re.search(
        r"assign\(['\"]?(.+?)['\"]?,\s*['\"]?(.+?)['\"]?\)",
        action_str.lower()
    )
    if match:
        return {
            "action_type": "assign",
            "patient_id": match.group(1),
            "doctor_id": match.group(2)
        }
    return {"action_type": "wait"}

# -----------------------------
# STEP
# -----------------------------
@app.post("/step")
async def step(request: Request):
    global env
    if env is None:
        return {"error": "Reset first"}

    data = await request.json()
    action_str = data.get("action", "wait()")

    action = Action(**parse_action(action_str))
    return env.step(action)

# -----------------------------
# RESET
# -----------------------------
@app.post("/reset")
async def reset(request: Request):
    global env
    data = await request.json()
    env = HealthcareEnv(task_type=data.get("task", "easy"))
    return {"state": env.reset()}

# -----------------------------
# FALLBACK POLICY
# -----------------------------
def fallback_policy(state):
    patients = sorted(state.patients_waiting, key=lambda p: p.severity, reverse=True)

    for p in patients:
        for d in state.doctors:
            if d.available:
                return Action(
                    action_type="assign",
                    patient_id=p.id,
                    doctor_id=d.id
                )

    return Action(action_type="wait")

# -----------------------------
# AGENT LOOP
# -----------------------------
async def run_inference_loop(task_type: str):
    global env, agent_status

    agent_status["is_running"] = True
    agent_status["total_reward"] = 0.0
    agent_status["final_score"] = 0.0

    env = HealthcareEnv(task_type=task_type)
    state = env.reset()

    is_done = False
    step_count = 0
    rewards = []

    while not is_done and step_count < 10:
        try:
            # -----------------------------
            # LLM OR FALLBACK
            # -----------------------------
            if client:
                prompt = f"""
                Hospital State: {state}

                Reply ONLY:
                assign(p_id, d_id)
                OR
                wait()
                """

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=20
                )

                action_str = response.choices[0].message.content.strip()
                action = Action(**parse_action(action_str))

            else:
                action = fallback_policy(state)

            # -----------------------------
            # STEP
            # -----------------------------
            result = env.step(action)

            reward = result.reward
            state = result.state
            is_done = result.done

            rewards.append(reward)
            agent_status["total_reward"] += reward

        except Exception as e:
            print("❌ ERROR:", e)
            break

        step_count += 1
        await asyncio.sleep(2)

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    if rewards:
        agent_status["final_score"] = sum(rewards) / len(rewards)

    agent_status["is_running"] = False
    print("🏁 Finished")

# -----------------------------
# STATE (🔥 FIXED)
# -----------------------------
@app.get("/state")
async def get_state():
    global env, agent_status

    if env is None:
        return {
            "time": 0,
            "task": "none",
            "patients_waiting": [],
            "doctors": [],
            "treated_patients": [],
            "agent": agent_status
        }

    state = env.get_state()

    return {
        "time": state.time,
        "task": env.task_type,   # 🔥 IMPORTANT FIX
        "patients_waiting": [p.dict() for p in state.patients_waiting],
        "doctors": [d.dict() for d in state.doctors],
        "treated_patients": [p.dict() for p in state.treated_patients],
        "agent": agent_status
    }

# -----------------------------
# RUN AGENT
# -----------------------------
@app.post("/run-agent")
async def run_agent(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    task = data.get("task", "easy")

    background_tasks.add_task(run_inference_loop, task)

    return {"message": f"AI Agent started on {task}"}