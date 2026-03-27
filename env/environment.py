import json
from env.models import Observation, Patient, Doctor, Action, Reward


class HealthcareEnv:
    def __init__(self):
        self.patient = None
        self.doctors = []
        self.done = False

    def reset(self):
        with open("data/patients.json") as f:
            patient_data = json.load(f)[0]

        with open("data/doctors.json") as f:
            doctors_data = json.load(f)

        self.patient = Patient(**patient_data)
        self.doctors = [Doctor(**d) for d in doctors_data]
        self.done = False

        return self._get_observation()

    def step(self, action: Action):
        score = 0.0
        feedback = ""

        # simple rule: cardiology needed for chest pain
        if "chest" in self.patient.symptoms.lower():
            if action.doctor == "Dr. Sharma":
                score += 0.5
                feedback += "Correct doctor. "

        if action.priority == "high":
            score += 0.5
            feedback += "Correct priority."

        self.done = True

        return self._get_observation(), Reward(score=score, feedback=feedback), self.done, {}

    def state(self):
        return {
            "patient": self.patient,
            "doctors": self.doctors
        }

    def _get_observation(self):
        return Observation(
            patient=self.patient,
            doctors=self.doctors
        )