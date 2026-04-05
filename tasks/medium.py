from env.environment import HealthcareEnv


def create_medium_env():
    return HealthcareEnv(task_type="medium")