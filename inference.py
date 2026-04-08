import os
import requests
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")

ENV_URL = os.getenv("ENV_URL", "http://127.0.0.1:7860")

client = None
if HF_TOKEN:
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
else:
    print("⚠️ No HF_TOKEN found → running fallback mode")

# -----------------------------
# FALLBACK POLICY (SMART)
# -----------------------------
def fallback_policy(state):
    patients = state.get("patients_waiting", [])
    doctors = state.get("doctors", [])

    best_score = -1
    best_action = "wait()"

    for p in patients:
        for d in doctors:
            if not d.get("available", False):
                continue

            severity = p.get("severity", 1)
            wait_time = p.get("waiting_time", 1)

            score = severity * 2 + wait_time

            if score > best_score:
                best_score = score
                best_action = f"assign({p['id']},{d['id']})"

    return best_action

# -----------------------------
# RUN TASK
# -----------------------------
def run_task(task_name):
    print(f"[START] task={task_name} env=healthcare model={MODEL_NAME}")

    try:
        res = requests.post(f"{ENV_URL}/reset", json={"task": task_name}).json()
        state = res.get("state", {})
    except Exception as e:
        print(f"[END] success=false steps=0 score=0.00 rewards= error={e}")
        return

    done = False
    step_idx = 1
    rewards = []

    while not done and step_idx <= 10:
        try:
            # -----------------------------
            # CHOOSE ACTION (LLM OR FALLBACK)
            # -----------------------------
            if client is not None:
                prompt = f"""
                You are an expert hospital scheduler.

                Patients: {state.get("patients_waiting", [])}
                Doctors: {state.get("doctors", [])}

                Choose BEST assignment.

                Reply ONLY:
                assign(p1, d2)
                OR
                wait()
                """

                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=20,
                    timeout=10
                )

                action_str = response.choices[0].message.content.strip().lower()

                # 🔥 SAFETY CHECK
                if "assign" not in action_str and "wait" not in action_str:
                    action_str = fallback_policy(state)

            else:
                action_str = fallback_policy(state)

            # -----------------------------
            # STEP ENV
            # -----------------------------
            res = requests.post(
                f"{ENV_URL}/step",
                json={"action": action_str}
            ).json()

            reward = float(res.get("reward", 0.0))
            done = res.get("done", False)
            state = res.get("state", {})

            rewards.append(reward)

            print(f"[STEP] step={step_idx} action={action_str} reward={reward:.2f} done={str(done).lower()} error=null")

        except Exception as e:
            print(f"[STEP] step={step_idx} action=wait() reward=0.00 done=true error={str(e)}")
            break

        step_idx += 1

    # -----------------------------
    # FINAL SCORE
    # -----------------------------
    total_reward = sum(rewards)
    success = "true" if total_reward > 0 else "false"
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(f"[END] success={success} steps={step_idx-1} score={total_reward:.2f} rewards={rewards_str}")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run_task(t)