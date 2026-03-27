🏥 AI Healthcare Scheduling Environment (OpenEnv)

📌 Overview

This project implements a real-world simulation environment for training and evaluating AI agents on hospital appointment scheduling tasks.

The environment follows the OpenEnv specification and simulates how hospitals manage patient appointments under constraints like urgency, doctor specialization, and limited time slots.

Our goal is to provide a benchmark environment where AI agents can learn to make efficient, real-world scheduling decisions.

---

🎯 Problem Statement

Hospitals often struggle with:

- Managing high patient volume
- Prioritizing emergency cases
- Assigning the right specialist
- Minimizing patient wait times

This environment simulates these challenges and evaluates how well an AI agent performs in solving them.

---

🧠 Environment Design

The environment is built around a hospital scheduling workflow.

👀 Observation Space

At each step, the agent receives:

- Patient request:
  
  - Symptoms / issue description
  - Urgency level (low, medium, emergency)

- Doctor availability:
  
  - Name
  - Specialization
  - Available time slots

- Current schedule state

---

🎮 Action Space

The agent must output:

{
  "doctor": "Dr. Sharma",
  "time": "10:00 AM",
  "priority": "high"
}

---

🏆 Reward Function

The reward is designed to reflect real-world scheduling quality:

Factor| Score
Emergency handled correctly| +0.4
Correct doctor specialization| +0.2
Efficient time allocation| +0.2
Reduced wait time| +0.2

❌ Penalties:

- Delayed emergency → -0.5
- Wrong specialization → -0.3
- Double booking → -0.3

This ensures continuous feedback and encourages optimal decision-making.

---

🧩 Tasks

We provide 3 levels of difficulty:

🟢 Easy

- Single patient
- Basic scheduling
- No conflicts

🟡 Medium

- Multiple patients
- Priority handling required

🔴 Hard

- Multiple patients
- Conflicting schedules
- Emergency interruptions
- Optimization required

---

⚙️ OpenEnv API

The environment implements:

- "reset()" → Initializes a new scheduling scenario
- "step(action)" → Evaluates agent action
- "state()" → Returns current environment state

---

🤖 Baseline Agent

We provide a baseline script using the OpenAI API.

The agent:

- Reads the current scenario
- Generates scheduling decisions
- Interacts with the environment

Example Prompt:

You are a hospital scheduling assistant.
Prioritize emergency cases and assign the correct doctor specialization.
Return output in JSON format.

---

📊 Baseline Results

Task| Score
Easy| 0.92
Medium| 0.81
Hard| 0.67

(Scores may vary slightly depending on model and randomness)

---

🛠️ Setup Instructions

1. Clone the repository

git clone <your-repo-link>
cd healthcare-openenv

2. Install dependencies

pip install -r requirements.txt

3. Set API key

export OPENAI_API_KEY=your_api_key

4. Run baseline

python scripts/baseline.py

---

🐳 Docker Setup

docker build -t healthcare-env .
docker run healthcare-env

---

☁️ Deployment

This project is deployed as a containerized environment on Hugging Face Spaces with the "openenv" tag.

---

💡 Key Features

- Real-world hospital scheduling simulation
- Multi-patient and multi-doctor scenarios
- Priority-aware decision making
- Continuous reward system
- Fully OpenEnv compliant

---

🚀 Future Improvements

- No-show handling
- Rescheduling optimization
- Multi-day scheduling
- Patient satisfaction modeling

---

👥 Team

- Environment Architect
- AI Integration Engineer
- Grader & Simulation Engineer

---

📜 License

MIT License

---