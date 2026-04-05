from env.environment import HealthcareEnv


def create_easy_env():
    return HealthcareEnv(task_type="easy")