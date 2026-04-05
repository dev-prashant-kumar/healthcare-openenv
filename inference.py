import os
import requests

# ENV VARIABLES (MANDATORY)
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")


# -----------------------------
# SIMPLE AGENT POLICY
# -----------------------------
def agent_policy(state):
    patients = state.get("patients_waiting", [])
    doctors = state.get("doctors", [])

    # Sort by severity + wait_time
    patients = sorted(
        patients,
        key=lambda x: (-x["severity"], -x["wait_time"])
    )

    for p in patients:
        # Prefer matching specialty
        for d in doctors:
            if d["available"] and d["specialty"] == p["condition"]:
                return {
                    "action_type": "assign",
                    "patient_id": p["id"],
                    "doctor_id": d["id"]
                }

        # fallback: any available doctor
        for d in doctors:
            if d["available"]:
                return {
                    "action_type": "assign",
                    "patient_id": p["id"],
                    "doctor_id": d["id"]
                }

    return {"action_type": "wait"}


# -----------------------------
# RUN EPISODE
# -----------------------------
def run_episode(task="easy"):
    print("[START]")

    # Reset environment
    response = requests.post(
        f"{API_BASE_URL}/reset",
        json={"task": task}
    )
    state = response.json()

    done = False
    step_count = 0

    while not done:
        action = agent_policy(state)

        result = requests.post(
            f"{API_BASE_URL}/step",
            json=action
        ).json()

        reward = result.get("reward", 0)
        done = result.get("done", False)
        state = result.get("state", {})

        print(f"[STEP] {step_count} | action={action} | reward={reward}")

        step_count += 1

    print("[END]")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    # Run all tasks
    for task in ["easy", "medium", "hard"]:
        run_episode(task)