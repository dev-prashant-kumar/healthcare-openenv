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
    try:
        client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
        print("✅ LLM Connected")
    except Exception as e:
        print("❌ LLM Init Failed:", e)
        client = None

# -----------------------------
# APP INIT
# -----------------------------
app = FastAPI()
env = None
templates = Jinja2Templates(directory="templates")

# -----------------------------
# AGENT STATUS
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
# RESET
# -----------------------------
@app.post("/reset")
async def reset_env(request: Request):
    global env, agent_status
    data = await request.json()
    task = data.get("task", "easy")

    env = HealthcareEnv(task_type=task)
    env.reset()

    agent_status = {
        "is_running": False,
        "total_reward": 0.0,
        "final_score": 0.0
    }

    return {"status": "success"}
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
    result = env.step(action)

    return {
        "reward": result.reward,
        "done": result.done,
        "state": result.state.dict() if hasattr(result.state, "dict") else result.state
    }

# -----------------------------
# FALLBACK POLICY (SMART)
# -----------------------------
def fallback_policy(state):
    patients = state.patients_waiting
    doctors = state.doctors

    best_score = -1
    best_action = None

    for p in patients:
        for d in doctors:
            if not d.available:
                continue

            severity_score = p.severity * 2
            wait_score = getattr(p, "waiting_time", 1)
            specialty_bonus = 2 if getattr(d, "specialty", None) == getattr(p, "condition", None) else 0

            score = severity_score + wait_score + specialty_bonus

            if score > best_score:
                best_score = score
                best_action = Action(
                    action_type="assign",
                    patient_id=p.id,
                    doctor_id=d.id
                )

    return best_action if best_action else Action(action_type="wait")

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
                You are a hospital scheduler.

                Patients: {state.patients_waiting}
                Doctors: {state.doctors}

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
        await asyncio.sleep(1)  # faster UI

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    if rewards:
        agent_status["final_score"] = sum(rewards) / len(rewards)

    agent_status["is_running"] = False
    print("🏁 Agent Finished")

# -----------------------------
# STATE (FOR UI + JUDGE)
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
        "task": env.task_type,
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

    # Prevent double run
    if agent_status["is_running"]:
        return {"message": "Agent already running"}

    background_tasks.add_task(run_inference_loop, task)

    return {"message": f"AI Agent started on {task}"}

