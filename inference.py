import os
import requests
from openai import OpenAI

# Competition Standard Variables
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
# Use getenv for security; local fallback only for your final test
HF_TOKEN = os.getenv("HF_TOKEN")

# The internal URL for Docker/HF Spaces
ENV_URL = "http://127.0.0.1:8000" 

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

def run_task(task_name):
    # [START] Tag is required
    print(f"[START] task={task_name} env=healthcare model={MODEL_NAME}")
    
    try:
        res = requests.post(f"{ENV_URL}/reset", json={"task": task_name}).json()
        state = res.get("state", {})
    except:
        return

    done = False
    step_idx = 1
    rewards = []

    while not done and step_idx <= 10:
        prompt = f"Hospital State: {state}. Which patient should go to which doctor? Reply ONLY with assign('p_id', 'd_id') or wait()."
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20
        )
        action_str = response.choices[0].message.content.strip()

        try:
            res = requests.post(f"{ENV_URL}/step", json={"action": action_str}).json()
            reward = float(res.get("reward", 0.0))
            done = res.get("done", False)
            state = res.get("state", {})
            rewards.append(reward)
            
            # [STEP] Tag is required
            print(f"[STEP] step={step_idx} action={action_str} reward={reward:.2f} done={str(done).lower()} error=null")
        except Exception as e:
            print(f"[STEP] step={step_idx} action={action_str} reward=0.00 done=true error={str(e)}")
            break
        
        step_idx += 1

    # [END] Tag calculation
    score = sum(rewards) / len(rewards) if rewards else 0.0
    success = "true" if score > 0.1 else "false"
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])
    print(f"[END] success={success} steps={step_idx-1} score={score:.2f} rewards={rewards_str}")

if __name__ == "__main__":
    for t in ["easy", "medium", "hard"]:
        run_task(t)