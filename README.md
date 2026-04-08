---
title: Healthcare AI Agent
emoji: 🏥
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# 🏥 Healthcare AI Agent – OpenEnv Competition

An AI-powered hospital scheduling system that intelligently assigns doctors to patients in a simulated healthcare environment using LLM reasoning and reward-based optimization.

---

## 🚀 Overview

Hospitals often face challenges in efficiently assigning doctors to patients under time pressure. This project simulates a real-time healthcare system where an AI agent must:

* Prioritize high-severity patients
* Minimize patient waiting time
* Match doctor specialties
* Optimize overall hospital efficiency

---

## ⚙️ System Architecture

Frontend Dashboard (HTML + Tailwind)
↓
FastAPI Backend (API + Agent Loop)
↓
Healthcare Environment (Simulation Engine)
↓
AI Agent (LLM + Fallback Policy)


---

## 🤖 Agent Strategy

The AI agent operates in a loop:
1. Observes hospital state
2. Decides action: `assign(patient_id, doctor_id)` or `wait()`
3. Executes action in environment
4. Receives reward

---

## 🖥️ Features

* 🎯 Real-time hospital simulation
* 📊 Live dashboard UI
* 🔁 Autonomous AI agent loop
* ⚡ Async FastAPI backend
* 🐳 Docker deployment support

---

## 🔑 Environment Variables

To run the LLM, you must add your token to the Space Secrets:
`HF_TOKEN` = your_huggingface_token

---

## 👨‍💻 Author
**Prashant Kumar**
GitHub: [dev-prashant-kumar](https://github.com/dev-prashant-kumar)