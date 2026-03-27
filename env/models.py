from pydantic import BaseModel
from typing import List, Optional


class Patient(BaseModel):
    id: str
    symptoms: str
    urgency: str  


class Doctor(BaseModel):
    name: str
    specialization: str
    available_slots: List[str]


class Observation(BaseModel):
    patient: Patient
    doctors: List[Doctor]


class Action(BaseModel):
    doctor: str
    time: str
    priority: str


class Reward(BaseModel):
    score: float
    feedback: str