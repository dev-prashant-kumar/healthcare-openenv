from fastapi import FastAPI
from env.environment import HealthcareEnv
from env.models import Action

app = FastAPI()

# Global env instance
env = None


@app.get("/")
def root():
    return {"message": "Healthcare Scheduling Environment API is running"}

# -----------------------------
# RESET
# -----------------------------
@app.post("/reset")
def reset(task: str = "easy"):
    global env
    env = HealthcareEnv(task_type=task)
    state = env.reset()
    return state


# -----------------------------
# STEP
# -----------------------------
@app.post("/step")
def step(action: Action):
    global env

    if env is None:
        return {"error": "Environment not initialized. Call /reset first."}

    result = env.step(action)
    return result


# -----------------------------
# STATE
# -----------------------------
@app.get("/state")
def get_state():
    global env

    if env is None:
        return {"error": "Environment not initialized. Call /reset first."}

    return env.get_state()