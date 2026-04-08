from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any


# -----------------------------
# Patient Model
# -----------------------------
class Patient(BaseModel):
    id: str
    age: int
    severity: int = Field(ge=0, le=10)   
    condition: str
    symptoms: str
    wait_time: int = Field(ge=0)
    deadline: int = Field(ge=1)


# -----------------------------
# Doctor Model
# -----------------------------
class Doctor(BaseModel):
    id: str
    name: str
    specialty: str
    experience: int = Field(ge=0, le=20)  
    available: bool
    busy_until: int = Field(ge=0)


# -----------------------------
# State (Observation)
# -----------------------------
class State(BaseModel):
    time: int = Field(ge=0)
    patients_waiting: List[Patient]
    doctors: List[Doctor]
    rooms_available: int = Field(ge=0)
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
    info: Dict[str, Any] = {}   