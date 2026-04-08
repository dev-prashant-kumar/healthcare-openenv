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

This project solves that by building an **AI agent that learns to make optimal scheduling decisions step-by-step**.

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
5. Updates strategy

### 🔥 Decision Logic

* Uses **LLM (Qwen 72B via HuggingFace Router)** when available
* Falls back to **smart heuristic policy** if API fails

### 🧮 Reward System

Rewards are based on:

* Patient severity (higher = higher reward)
* Waiting time penalty
* Doctor specialty match bonus
* Doctor experience bonus
* Penalty for missed deadlines

---

## 🖥️ Features

* 🎯 Real-time hospital simulation
* 📊 Live dashboard with environment state
* 🔁 Auto-running AI agent loop
* ⚡ Async FastAPI backend
* 🧪 Deterministic evaluation system
* 🐳 Docker support

---

## 📸 Demo

> Add screenshots here for maximum impact

```
/assets/dashboard.png
/assets/running.png
```

---

## 🚀 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/dev-prashant-kumar/healthcare-openenv.git
cd healthcare-openenv
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
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

### Build image

```bash
docker build -t healthcare-ai .
```

### Run container

```bash
docker run -p 8000:8000 healthcare-ai
```

---

## 🤗 Deploy on Hugging Face Spaces

* Create a new Space
* Select **Docker** runtime
* Push your repo

### Important:

* Expose port: `7860`
* Update Dockerfile:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

---

## 🔑 Environment Variables

Set your HuggingFace API key:

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

The agent follows the required evaluation format:

```
[START] task=easy env=healthcare model=Qwen
[STEP] step=1 action=assign(p1,d1) reward=0.80 done=false
...
[END] success=true steps=10 score=0.65
```

---

## 🧪 Tech Stack

* **Backend:** FastAPI
* **AI:** OpenAI SDK (HF Router)
* **Frontend:** HTML + Tailwind CSS
* **Environment:** Custom RL-style simulation
* **Containerization:** Docker
* **Language:** Python

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

It highlights:

* Decision-making under constraints
* Hybrid AI systems (LLM + rules)
* Real-time simulation control

---

## 👨‍💻 Author

**Prashant Kumar**
GitHub: https://github.com/dev-prashant-kumar

---

## ⭐ If you like this project

Give it a star ⭐ and share your feedback!
