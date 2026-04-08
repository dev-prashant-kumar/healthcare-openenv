import json
import os
import random
from typing import List, Dict

from env.models import State, Patient, Doctor, Action, StepResponse


class HealthcareEnv:

    # -----------------------------
    # LOAD DATASET
    # -----------------------------
    def _load_patients(self):
        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "data", "patients.json")

        with open(file_path) as f:
            return json.load(f)

    def _load_doctors(self):
        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "data", "doctors.json")

        with open(file_path) as f:
            return json.load(f)

    # -----------------------------
    # INIT
    # -----------------------------
    def __init__(self, task_type: str = "easy"):
        self.task_type = task_type
        self.state: State = None

        # 🔥 FIX: match agent loop
        self.max_steps = 10
        self.current_step = 0

        self.history = {
            "treated_patients": [],
            "missed_deadlines": 0,
            "total_patients": 0
        }

    # -----------------------------
    # RESET
    # -----------------------------
    def reset(self) -> State:
        self.current_step = 0

        if self.task_type == "easy":
            self.state = self._init_easy()
        elif self.task_type == "medium":
            self.state = self._init_medium()
        else:
            self.state = self._init_hard()

        self.history = {
            "treated_patients": [],
            "missed_deadlines": 0,
            "total_patients": len(self.state.patients_waiting)
        }

        return self.state

    # -----------------------------
    def get_state(self) -> State:
        return self.state

    # -----------------------------
    # STEP
    # -----------------------------
    def step(self, action: Action) -> StepResponse:
        reward = 0.0
        info = {}

        self.current_step += 1
        self.state.time += 1

        # -----------------------------
        # UPDATE DOCTORS
        # -----------------------------
        for doc in self.state.doctors:
            if not doc.available and self.state.time >= doc.busy_until:
                doc.available = True

        # -----------------------------
        # UPDATE PATIENTS
        # -----------------------------
        for p in self.state.patients_waiting:
            p.wait_time += 1

            if p.wait_time > 2:
                p.severity = min(10, p.severity + 1)

            # 🔥 FIXED balanced penalty
            if p.severity >= 8:
                reward -= 0.4
            else:
                reward -= 0.05

        # -----------------------------
        # APPLY ACTION
        # -----------------------------
        if action.action_type == "assign":
            reward += 0.1  # 🔥 anti-wait bonus
            reward += self._handle_assign(action)

        elif action.action_type == "wait":
            reward -= 0.2

        # -----------------------------
        # CHECK DEADLINES
        # -----------------------------
        remaining_patients = []
        for p in self.state.patients_waiting:
            if p.wait_time > p.deadline:
                reward -= 0.5  # 🔥 reduced penalty
                self.history["missed_deadlines"] += 1
            else:
                remaining_patients.append(p)

        self.state.patients_waiting = remaining_patients

        # -----------------------------
        # NEW PATIENTS (LESS RANDOM)
        # -----------------------------
        if self.task_type in ["medium", "hard"]:
            if random.random() < 0.25:
                self._add_random_patient()

        # -----------------------------
        # DONE CONDITION
        # -----------------------------
        done = (
            self.current_step >= self.max_steps
            or len(self.state.patients_waiting) == 0
        )

        info["history"] = self.history

        return StepResponse(
            state=self.state,
            reward=reward,
            done=done,
            info=info
        )

    # -----------------------------
    # HANDLE ASSIGN
    # -----------------------------
    def _handle_assign(self, action: Action) -> float:
        reward = 0.0

        patient = next(
            (p for p in self.state.patients_waiting if p.id == action.patient_id),
            None
        )
        doctor = next(
            (d for d in self.state.doctors if d.id == action.doctor_id),
            None
        )

        # 🔥 STRONG penalty for invalid action
        if not patient or not doctor or not doctor.available:
            return -1.0

        # -----------------------------
        # DOCTOR BUSY TIME (DYNAMIC)
        # -----------------------------
        doctor.available = False
        doctor.busy_until = self.state.time + (1 if patient.severity < 7 else 2)

        # -----------------------------
        # REWARD CALCULATION
        # -----------------------------
        if patient.severity >= 9:
            reward += 1.2
        elif patient.severity >= 7:
            reward += 0.8
        else:
            reward += 0.4

        # specialty match
        if doctor.specialty == patient.condition:
            reward += 0.4
        else:
            reward += 0.1

        # age priority
        if patient.age >= 60:
            reward += 0.2

        # experienced doctor bonus
        if doctor.experience >= 8:
            reward += 0.2

        # 🔥 urgency bonus
        if patient.wait_time >= patient.deadline - 1:
            reward += 0.5

        # -----------------------------
        # COMPLETE TREATMENT
        # -----------------------------
        self.state.treated_patients.append(patient)
        self.state.patients_waiting.remove(patient)

        self.history["treated_patients"].append(patient.dict())

        # 🔥 completion bonus
        if len(self.state.patients_waiting) == 0:
            reward += 1.5

        return reward

    # -----------------------------
    # RANDOM PATIENT
    # -----------------------------
    def _add_random_patient(self):
        new_patient = Patient(
            id=f"p{random.randint(100,999)}",
            age=random.randint(20, 80),
            severity=random.randint(3, 10),
            condition=random.choice(["cardiac", "general"]),
            symptoms="random case",
            wait_time=0,
            deadline=random.randint(3, 6)
        )
        self.state.patients_waiting.append(new_patient)

    # -----------------------------
    # TASK INITIALIZATIONS
    # -----------------------------
    def _init_easy(self) -> State:
        patients_data = self._load_patients()
        doctors_data = self._load_doctors()

        random.shuffle(patients_data)
        random.shuffle(doctors_data)

        patients_data = patients_data[:2]
        doctors_data = doctors_data[:2]

        patients = [Patient(**p, wait_time=0) for p in patients_data]
        doctors = [Doctor(**d, available=True, busy_until=0) for d in doctors_data]

        return State(time=0, patients_waiting=patients, doctors=doctors, rooms_available=2, treated_patients=[])

    def _init_medium(self) -> State:
        patients_data = self._load_patients()
        doctors_data = self._load_doctors()

        random.shuffle(patients_data)
        random.shuffle(doctors_data)

        patients_data = patients_data[:4]
        doctors_data = doctors_data[:3]

        patients = [Patient(**p, wait_time=0) for p in patients_data]

        doctors = [
            Doctor(**d, available=(i < 2), busy_until=(2 if i == 2 else 0))
            for i, d in enumerate(doctors_data)
        ]

        return State(time=0, patients_waiting=patients, doctors=doctors, rooms_available=2, treated_patients=[])

    def _init_hard(self) -> State:
        patients_data = self._load_patients()
        doctors_data = self._load_doctors()

        random.shuffle(patients_data)
        random.shuffle(doctors_data)

        patients = [Patient(**p, wait_time=0) for p in patients_data]

        doctors = [
            Doctor(**d, available=(i % 2 == 0), busy_until=(3 if i % 2 else 0))
            for i, d in enumerate(doctors_data)
        ]

        return State(time=0, patients_waiting=patients, doctors=doctors, rooms_available=1, treated_patients=[])