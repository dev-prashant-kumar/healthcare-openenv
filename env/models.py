from pydantic import BaseModel
from typing import List, Optional, Literal


# -----------------------------
# Patient Model
# -----------------------------
class Patient(BaseModel):
    id: str
    age: int
    severity: int
    condition: str
    symptoms: str
    wait_time: int
    deadline: int


# -----------------------------
# Doctor Model
# -----------------------------
class Doctor(BaseModel):
    id: str
    name: str
    specialty: str
    experience: int
    available: bool
    busy_until: int


# -----------------------------
# State (Observation)
# -----------------------------
class State(BaseModel):
    time: int
    patients_waiting: List[Patient]
    doctors: List[Doctor]
    rooms_available: int
    treated_patients: List[Patient]


# -----------------------------
# Action Model
# -----------------------------
class Action(BaseModel):
    action_type: Literal["assign", "wait"]
    patient_id: Optional[str] = None
    doctor_id: Optional[str] = None


# -----------------------------
# Step Response (CRITICAL)
# -----------------------------
class StepResponse(BaseModel):
    state: State
    reward: float
    done: bool
    info: dict