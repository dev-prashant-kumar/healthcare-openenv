from env.environment import HealthcareEnv


def create_hard_env():
    return HealthcareEnv(task_type="hard")