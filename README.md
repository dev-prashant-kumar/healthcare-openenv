---

title: Healthcare AI Agent
emoji: 🏥
colorFrom: blue
colorTo: indigo
sdk: docker
app_file: app/main.py
pinned: false
-------------

# 🏥 Healthcare AI Agent – OpenEnv Competition

An AI-powered hospital scheduling system that intelligently assigns doctors to patients in a simulated healthcare environment using LLM reasoning and reward-based optimization.

---

## 🚀 Overview

Hospitals often face challenges in efficiently assigning doctors to patients under time pressure. This project simulates a real-time healthcare system where an AI agent must:

* Prioritize high-severity patients
* Minimize patient waiting time
* Match doctor specialties
* Optimize overall hospital efficiency

The system combines:

* 🤖 Large Language Model (LLM) decision-making
* ⚙️ Rule-based fallback policy
* 📊 Reward-driven environment simulation

---

## 🧠 Problem Statement

In real-world hospitals:

* Critical patients may not get immediate attention
* Doctors may be underutilized or mismatched
* Delays can significantly impact outcomes

This project solves this by building an **AI agent that makes optimal scheduling decisions step-by-step**.

---

## ⚙️ System Architecture

```
Frontend Dashboard (HTML + Tailwind)
            ↓
FastAPI Backend (API + Agent Loop)
            ↓
Healthcare Environment (Simulation Engine)
            ↓
AI Agent (LLM + Fallback Policy)
```

---

## 🤖 Agent Strategy

The AI agent operates in a loop:

1. Observes hospital state
2. Decides action:

   * `assign(patient_id, doctor_id)`
   * `wait()`
3. Executes action in environment
4. Receives reward
5. Updates decisions

### 🔥 Decision Logic

* Uses **LLM (Qwen 72B via HuggingFace Router)** when available
* Falls back to a **smart heuristic policy** if API is unavailable

### 🧮 Reward System

Rewards are based on:

* Patient severity (higher = higher reward)
* Waiting time penalties
* Doctor specialty match bonus
* Doctor experience bonus
* Deadline penalties

---

## 🖥️ Features

* 🎯 Real-time hospital simulation
* 📊 Live dashboard UI
* 🔁 Autonomous AI agent loop
* ⚡ Async FastAPI backend
* 🧪 Evaluation-ready output format
* 🐳 Docker deployment support


---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/dev-prashant-kumar/healthcare-openenv.git
cd healthcare-openenv
```

### 2. Setup environment

```bash
python -m venv venv
venv\Scripts\activate      # Windows
# OR
source venv/bin/activate   # Linux/Mac
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run server

```bash
uvicorn app.main:app --reload
```

Open:
👉 http://localhost:8000

---

## 🐳 Run with Docker

### Build

```bash
docker build -t healthcare-ai .
```

### Run

```bash
docker run -p 8000:8000 healthcare-ai
```

---

## 🤗 Deploy on Hugging Face Spaces

* Create a new Space
* Select **Docker** runtime
* Connect your GitHub repo

### ⚠️ Important

Ensure your Dockerfile runs:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## 🔑 Environment Variables

```bash
HF_TOKEN=your_api_key_here
```

Optional:

```bash
API_BASE_URL=https://router.huggingface.co/v1
MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
```

---

## 📊 Evaluation Output Format

```
[START] task=easy env=healthcare model=Qwen
[STEP] step=1 action=assign(p1,d1) reward=0.80 done=false
...
[END] success=true steps=10 score=0.65
```

---

## 🧪 Tech Stack

* FastAPI
* OpenAI SDK (HF Router)
* Tailwind CSS
* Docker
* Python (Pydantic, Async)

---

## 📁 Project Structure

```
app/
 ├── main.py
env/
 ├── environment.py
 ├── models.py
data/
templates/
 ├── index.html
Dockerfile
requirements.txt
```

---

## 🏁 Conclusion

This project demonstrates how LLMs can be integrated with structured simulation environments to solve real-world optimization problems like healthcare scheduling.

---

## 👨‍💻 Author

**Prashant Kumar**
GitHub: https://github.com/dev-prashant-kumar

---

## ⭐ Support

If you like this project, give it a ⭐ and share feedback!
